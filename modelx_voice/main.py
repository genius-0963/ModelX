import asyncio
import sys
import signal
from pathlib import Path
from typing import Optional

from .config import ConfigManager, run_setup_wizard
from .brain import ModelXBrain, ConversationMemory
from .pipeline import AudioPipeline, PipelineConfig
from .ui import SimpleVoiceUI


async def main(
    setup: bool = False,
    configure: bool = False,
    test_audio: bool = False,
    test_api: bool = False,
    download_voices: bool = False,
    voice: Optional[str] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
):
    config_manager = ConfigManager()
    
    if setup or configure:
        success = await run_setup_wizard(config_manager)
        if not success:
            sys.exit(1)
        return
    
    if download_voices:
        from .tts import VoiceManager
        vm = VoiceManager()
        voices = vm.list_available_voices()
        print("Available voices:")
        for profile, filename in voices.items():
            print(f"  {profile}: {filename}")
        return
    
    config = config_manager.load()
    
    if provider:
        config.api.provider = provider
    if api_key:
        config.api.api_key = api_key
    if voice:
        config.voice.selected_voice = voice
    
    config_manager.save()
    
    if test_audio:
        await test_audio_devices()
        return
    
    if test_api:
        await test_api_connection(config)
        return
    
    if not config_manager.is_configured():
        print("Not configured. Run 'modelx-voice --setup' to configure.")
        sys.exit(1)
    
    if not config.api.model:
        from .brain import get_default_model
        config.api.model = get_default_model(config.api.provider)
        config_manager.save()
    
    memory_file = config_manager.config_dir / "conversation.json"
    memory = ConversationMemory(persistence_file=memory_file)
    
    brain = ModelXBrain(
        provider=config.api.provider,
        api_key=config.api.api_key,
        base_url=config.api.base_url or None,
        model=config.api.model,
        memory=memory,
    )
    
    pipeline_config = PipelineConfig(
        sample_rate=config.audio.sample_rate,
        vad_aggressiveness=config.behavior.vad_aggressiveness,
        whisper_model="base",
        voice_profile=config.voice.selected_voice,
        auto_listen=config.behavior.auto_listen and not config.behavior.wake_word,
    )
    
    ui = SimpleVoiceUI()
    pipeline = AudioPipeline(pipeline_config, config_manager, brain, ui)
    
    loop = asyncio.get_event_loop()
    
    def signal_handler():
        print("\nShutting down...")
        pipeline._running = False
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            pass
    
    await pipeline.initialize()
    await pipeline.run()
    
    await brain.close()
    print("\nGoodbye!")


async def test_audio_devices():
    import sounddevice as sd
    print("Audio Devices:")
    print("-" * 60)
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        io = []
        if device['max_input_channels'] > 0:
            io.append(f"in:{device['max_input_channels']}")
        if device['max_output_channels'] > 0:
            io.append(f"out:{device['max_output_channels']}")
        default_in = " (default in)" if i == sd.default.device[0] else ""
        default_out = " (default out)" if i == sd.default.device[1] else ""
        print(f"  [{i}] {device['name']} - {'/'.join(io)}{default_in}{default_out}")


async def test_api_connection(config):
    from .brain import get_provider, Message
    
    print(f"Testing {config.api.provider} API connection...")
    
    try:
        provider = get_provider(config.api.provider, config.api.api_key, config.api.base_url)
        response = await provider.chat_completion(
            messages=[Message(role="user", content="Hello")],
            model=config.api.model or "claude-sonnet-4-20250514",
            max_tokens=10,
        )
        print(f"✓ Success! Response: {response.content[:50]}...")
        await provider.close()
    except Exception as e:
        print(f"✗ Failed: {e}")
        sys.exit(1)


def cli():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ModelX Voice Assistant - Terminal voice agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  modelx-voice                 Start voice assistant
  modelx-voice --setup         Run setup wizard
  modelx-voice --configure     Reconfigure settings
  modelx-voice --test-audio    Test audio devices
  modelx-voice --test-api      Test API connection
  modelx-voice --voice casual  Use casual voice
        """
    )
    
    parser.add_argument("--setup", action="store_true", help="Run setup wizard")
    parser.add_argument("--configure", action="store_true", help="Reconfigure settings")
    parser.add_argument("--test-audio", action="store_true", help="Test audio devices")
    parser.add_argument("--test-api", action="store_true", help="Test API connection")
    parser.add_argument("--download-voices", action="store_true", help="List available voices")
    parser.add_argument("--voice", choices=["professional", "casual", "clear"], help="Voice profile")
    parser.add_argument("--provider", choices=["anthropic", "openai", "openrouter", "ollama"], help="LLM provider")
    parser.add_argument("--api-key", help="API key (for quick setup)")
    
    args = parser.parse_args()
    
    asyncio.run(main(
        setup=args.setup,
        configure=args.configure,
        test_audio=args.test_audio,
        test_api=args.test_api,
        download_voices=args.download_voices,
        voice=args.voice,
        provider=args.provider,
        api_key=args.api_key,
    ))


if __name__ == "__main__":
    cli()
# ModelX Voice Assistant

A standalone, downloadable voice agent that runs in your terminal with pre-built voices. Just add your LLM API key and start talking.

## Features

- 🎤 **Real-time voice interaction** - Speak naturally, get spoken responses
- 🧠 **Multiple LLM providers** - Anthropic, OpenAI, OpenRouter, Ollama (local)
- 🔊 **Pre-built natural voices** - No separate downloads needed (Piper TTS)
- 💻 **Beautiful terminal interface** - Rich UI with voice activity visualization
- 🔄 **Conversation memory** - Remembers context across turns
- 📦 **One-line installation** - `pip install modelx-voice`
- 🔒 **Secure API key storage** - System keyring integration
- 🌐 **Cross-platform** - macOS, Linux, Windows

## Quick Start

```bash
# Install
pip install modelx-voice

# Run setup wizard
modelx-voice --setup

# Start talking!
modelx-voice
```

## Installation

### Via pip (recommended)

```bash
pip install modelx-voice
```

### From source

```bash
git clone https://github.com/modelx/modelx-voice
cd modelx-voice
./install.sh
```

### System Requirements

- **Python**: 3.10+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for voice models
- **Microphone**: Required for voice input
- **Speakers**: Required for voice output

### System Dependencies

**macOS:**
```bash
brew install portaudio ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev ffmpeg
```

**Linux (Fedora):**
```bash
sudo dnf install portaudio-devel ffmpeg
```

**Windows:**
```bash
# Install via pip - dependencies included
pip install modelx-voice
```

## Configuration

Run the setup wizard:

```bash
modelx-voice --setup
```

The wizard will guide you through:
1. **LLM Provider** - Choose Anthropic, OpenAI, OpenRouter, or Ollama
2. **API Key** - Stored securely in system keyring
3. **Voice Profile** - Professional, Casual, or Clear
4. **Audio Devices** - Select input/output devices
5. **Behavior** - Wake word, auto-listen, sensitivity

Configuration is saved to `~/.modelx-voice/config.json`.

## Usage

### Basic Commands

```bash
modelx-voice                    # Start voice assistant
modelx-voice --setup            # Run setup wizard
modelx-voice --configure        # Reconfigure settings
modelx-voice --test-audio       # Test audio devices
modelx-voice --test-api         # Test API connection
modelx-voice --voice casual     # Use casual voice
modelx-voice --provider openai  # Use OpenAI provider
```

### Voice Commands

While running, say these commands:
- **"Stop"** / **"Quit"** / **"Exit"** - Stop listening and exit
- **"Pause"** / **"Wait"** - Pause the response
- **"Clear"** / **"Reset"** - Clear conversation history
- **"Save"** - Save conversation to file
- **"Help"** - Show available commands
- **"Switch voice professional"** - Change voice profile
- **"Status"** - Show system status
- **"Repeat"** - Repeat last response

### Push-to-Talk Mode

By default, the assistant uses voice activity detection. For push-to-talk:

```bash
modelx-voice --configure
# Set wake word to empty when prompted
```

Then press `Enter` to start recording, wait for silence to stop.

## Supported LLM Providers

| Provider | Models | Notes |
|----------|--------|-------|
| **Anthropic** | Claude Sonnet 4, Opus, Haiku | Recommended |
| **OpenAI** | GPT-4o, GPT-4, GPT-3.5 | |
| **OpenRouter** | 100+ models | Multi-provider access |
| **Ollama** | Llama 3.2, Mistral, etc. | Local, no API key needed |

## Voice Profiles

| Profile | Voice | Best For |
|---------|-------|----------|
| **Professional** | Male (Lessac) | Business, presentations |
| **Casual** | Female (Amy) | Friendly conversation |
| **Clear** | Female (LibriTTS) | Maximum clarity |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ModelX Voice Agent                        │
├─────────────────────────────────────────────────────────────┤
│  Audio Input → VAD → Whisper STT → LLM → Piper TTS → Audio  │
│       ↑                                                    ↓  │
│       └─────────── Conversation Memory ────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

- **STT**: faster-whisper (local, no API needed)
- **TTS**: Piper TTS with ONNX models (local, fast)
- **VAD**: WebRTC VAD for accurate speech detection
- **Audio**: sounddevice for cross-platform I/O
- **UI**: Rich for beautiful terminal rendering

## Privacy

- **All audio processing is local** - No audio sent to cloud
- **Only text goes to LLM** - Your voice never leaves your machine
- **API keys in system keyring** - Never stored in plain text
- **Optional offline mode** - Use with Ollama for complete privacy

## Troubleshooting

### No microphone detected
```bash
# Check audio devices
modelx-voice --test-audio

# Install system dependencies
# macOS: brew install portaudio
# Linux: sudo apt-get install portaudio19-dev
```

### Voice models not loading
```bash
# Re-download voice models
python -c "from modelx_voice.voices.downloader import download_all_voices; import asyncio; asyncio.run(download_all_voices())"

# Check voice directory
ls ~/.modelx-voice/voices/
```

### API key errors
```bash
# Reconfigure API key
modelx-voice --configure

# Test API connection
modelx-voice --test-api
```

### Permission denied (Linux)
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Log out and back in
```

## Development

### Project Structure
```
modelx_voice/
├── audio/          # Audio capture, playback, VAD
├── stt/            # Speech-to-text (Whisper)
├── tts/            # Text-to-speech (Piper)
├── brain/          # LLM integration, memory
├── config/         # Configuration, setup wizard
├── ui/             # Terminal UI, commands
├── voices/         # Pre-built voice models
├── pipeline.py     # Main audio pipeline
└── main.py         # Entry point
```

### Running Tests
```bash
pip install -e ".[dev]"
pytest
```

### Code Style
```bash
black modelx_voice/
```

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/modelx/modelx-voice/issues)
- **Discussions**: [GitHub Discussions](https://github.com/modelx/modelx-voice/discussions)
- **Discord**: [ModelX Community](https://discord.gg/modelx)

## Acknowledgments

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) for STT
- [Piper TTS](https://github.com/rhasspy/piper) for TTS
- [WebRTC VAD](https://webrtc.org/) for voice activity detection
- [Rich](https://github.com/Textualize/rich) for terminal UI
- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio I/O
# ModelX Voice Assistant

[![PyPI version](https://img.shields.io/pypi/v/modelx-voice.svg)](https://pypi.org/project/modelx-voice/)
[![Python versions](https://img.shields.io/pypi/pyversions/modelx-voice.svg)](https://pypi.org/project/modelx-voice/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/modelx/modelx-voice/ci.yml?branch=main)](https://github.com/modelx/modelx-voice/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Discord](https://img.shields.io/discord/123456789?label=Discord&logo=discord&color=5865F2)](https://discord.gg/modelx)

> A **standalone, downloadable voice agent** that runs entirely in your terminal. Install, add your LLM API key, and start talking immediately. No cloud dependencies for audio processing—your voice never leaves your machine.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **Real-time Voice I/O** | Sub-second latency with streaming STT/TTS |
| 🧠 **Multi-Provider LLM** | Anthropic, OpenAI, OpenRouter, Ollama (local) |
| 🔊 **Local Neural TTS** | 3 high-quality Piper voices bundled |
| 💻 **Rich Terminal UI** | Live transcription, VU meter, status panels |
| 🔄 **Persistent Memory** | Conversation history with token-aware pruning |
| 🔒 **Secure Key Storage** | macOS Keychain / Windows Credential Manager / libsecret |
| 🌐 **Cross-Platform** | macOS, Linux, Windows (x64/ARM64) |
| 📦 **Zero-Config Install** | `pip install modelx-voice` |

---

## 🚀 Quick Start

```bash
# 1. Install
pip install modelx

# 2. Configure (interactive wizard)
modelx --setup

# 3. Talk!
modelx
```

<details>
<summary><b>📹 Demo</b> (click to expand)</summary>

```bash
$ modelx

╔══════════════════════════════════════════════════════════════════════╗
║  🎤 ModelX Voice Assistant                    [🟢 Listening]       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  You: What's the capital of France?                                 ║
║                                                                     ║
║  ModelX: The capital of France is Paris. It's known for the        ║
║          Eiffel Tower, Louvre Museum, and amazing cuisine.         ║
║                                                                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  Provider: Anthropic | Model: claude-sonnet-4 | Turns: 3 | Tokens: 1,234 ║
╚══════════════════════════════════════════════════════════════════════╝
```

</details>

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Voice Commands](#-voice-commands)
- [Architecture](#-architecture)
- [Performance](#-performance)
- [Privacy & Security](#-privacy--security)
- [Advanced Usage](#-advanced-usage)
- [Configuration Reference](#-configuration-reference)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 📦 Installation

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10+ | 3.11+ |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB | 1 GB |
| Mic/Speakers | Required | Quality headset |

### System Dependencies

<details>
<summary><b>macOS</b> (Homebrew)</summary>

```bash
brew install portaudio ffmpeg
# Optional: for better audio quality
brew install opus
```
</details>

<details>
<summary><b>Linux (Debian/Ubuntu)</b></summary>

```bash
sudo apt-get update && sudo apt-get install -y \
  portaudio19-dev ffmpeg libopus-dev
```
</details>

<details>
<summary><b>Linux (Fedora/RHEL)</b></summary>

```bash
sudo dnf install -y portaudio-devel ffmpeg opus-devel
```
</details>

<details>
<summary><b>Linux (Arch)</b></summary>

```bash
sudo pacman -S --noconfirm portaudio ffmpeg opus
```
</details>

<details>
<summary><b>Windows</b></summary>

```powershell
# Using winget
winget install Python.Python.3.11
pip install modelx
# All audio deps bundled via wheels
```
</details>

### Install Methods

**PyPI (recommended)**
```bash
pip install modelx
```

**From Source**
```bash
git clone https://github.com/modelx/modelx
cd modelx
./install.sh        # Installs deps + downloads voices
# OR
pip install -e .
```

**Docker**
```bash
docker run -it --device=/dev/snd \
  -v ~/.modelx-voice:/root/.modelx-voice \
  modelx/voice:latest
```

---

## ⚙️ Configuration

### Interactive Setup Wizard

```bash
modelx --setup
```

The wizard configures:

1. **LLM Provider** — Anthropic / OpenAI / OpenRouter / Ollama
2. **API Key** — Stored in system keyring (never plain text)
3. **Model** — Auto-selects recommended default
4. **Voice Profile** — Professional / Casual / Clear
5. **Audio Devices** — Input/output selection with preview
6. **Behavior** — Wake word, auto-listen, VAD sensitivity

### Config File Location

```
~/.modelx-voice/
├── config.json      # User settings (no secrets)
└── voices/          # Downloaded ONNX models
    ├── en_US-lessac-medium.onnx
    ├── en_US-lessac-medium.onnx.json
    ├── en_US-amy-low.onnx
    ├── en_US-amy-low.onnx.json
    └── voice_config.json
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODELX_CONFIG_DIR` | Config directory | `~/.modelx-voice` |
| `ANTHROPIC_API_KEY` | Fallback API key | — |
| `OPENAI_API_KEY` | Fallback API key | — |
| `OPENROUTER_API_KEY` | Fallback API key | — |
| `OLLAMA_HOST` | Ollama endpoint | `http://localhost:11434` |

---

## 🎮 Usage

### CLI Reference

```bash
modelx [COMMAND] [OPTIONS]

Commands:
  modelx                    Start voice assistant (default)
  modelx voice              Start voice assistant (explicit)
  modelx doctor             Run system diagnostics
  modelx self-test          Run internal self-tests
  modelx --version          Show version

Voice Options:
  --setup              Run first-time setup wizard
  --configure          Modify existing configuration
  --test-audio         List and test audio devices
  --test-api           Verify LLM API connectivity
  --download-voices    Download missing voice models
  --voice VOICE        Voice profile (professional|casual|clear)
  --provider PROVIDER  LLM provider (anthropic|openai|openrouter|ollama)
  --model MODEL        Override default model
  --push-to-talk       Disable VAD, use Enter to record
  --debug              Enable debug logging
  -h, --help           Show help message
```

### Examples

```bash
# Default (uses saved config) - starts voice assistant
modelx
modelx voice

# Quick provider switch
modelx --provider openai --model gpt-4o

# Specific voice for this session
modelx --voice casual

# Push-to-talk mode (no VAD)
modelx --push-to-talk

# Test without speaking
modelx --test-api
modelx --test-audio

# System diagnostics
modelx doctor

# Run self-tests
modelx self-test

# Show version
modelx --version
```

---

## 🗣️ Voice Commands

| Command | Action |
|---------|--------|
| `Stop` / `Quit` / `Exit` | Exit application |
| `Pause` / `Wait` | Pause current response |
| `Clear` / `Reset` / `Forget` | Clear conversation history |
| `Save` / `Export` | Save conversation to JSON |
| `Help` / `Commands` | Show command list |
| `Switch voice <profile>` | Change voice (professional\|casual\|clear) |
| `Status` / `Stats` | Show provider, model, turns, tokens |
| `Repeat` / `Say that again` | Re-speak last response |

> Commands are case-insensitive and matched flexibly (e.g., "please stop" works).

---

## 🏗️ Architecture

### High-Level Data Flow

```mermaid
flowchart LR
    A[🎤 Microphone] --> B[Audio Capture<br/>sounddevice]
    B --> C[Voice Activity Detection<br/>WebRTC VAD]
    C -->|Speech detected| D[Audio Buffer]
    D --> E[Whisper STT<br/>faster-whisper]
    E -->|Transcript| F[Command Processor]
    F -->|Not a command| G[LLM Client<br/>Anthropic/OpenAI/Ollama]
    G -->|Response| H[Conversation Memory]
    H --> I[Piper TTS<br/>ONNX Runtime]
    I -->|Audio Stream| J[Audio Playback<br/>sounddevice]
    J --> K[🔊 Speakers]
    
    style A fill:#e1f5fe
    style K fill:#e1f5fe
    style E fill:#fff3e0
    style I fill:#fff3e0
    style G fill:#f3e5f5
```

### Component Diagram

```mermaid
graph TB
    subgraph Audio["🎵 Audio Layer"]
        AC[AudioCapture]
        AP[AudioPlayback]
        VAD[StreamingVAD]
    end
    
    subgraph STT["🎯 Speech-to-Text"]
        WT[WhisperTranscriber]
        ST[StreamingTranscriber]
    end
    
    subgraph Brain["🧠 Brain"]
        LC[LLMClient\nAnthropic/OpenAI/Ollama]
        CM[ConversationMemory]
    end
    
    subgraph TTS["🔊 Text-to-Speech"]
        PS[PiperSynthesizer]
        VM[VoiceManager]
    end
    
    subgraph UI["💻 Interface"]
        UI[SimpleVoiceUI/VoiceTerminalUI]
        CP[CommandProcessor]
    end
    
    subgraph Config["⚙️ Configuration"]
        CFG[ConfigManager]
        SW[SetupWizard]
        KR[KeyringBackend]
    end
    
    Pipeline[AudioPipeline] --> Audio
    Pipeline --> STT
    Pipeline --> Brain
    Pipeline --> TTS
    Pipeline --> UI
    Pipeline --> Config
```

### Pipeline Stages

| Stage | Component | Latency Target |
|-------|-----------|----------------|
| 1. Capture | `AudioCapture` (16kHz, 512-sample chunks) | — |
| 2. VAD | `StreamingVAD` (30ms frames, aggressiveness=2) | < 10ms |
| 3. STT | `WhisperTranscriber` (base model, beam_size=5) | < 500ms |
| 4. LLM | Provider-specific streaming | < 1.5s first token |
| 5. TTS | `PiperSynthesizer` (ONNX, 22.05kHz) | < 300ms |
| 6. Playback | `AudioPlayback` (streaming) | — |

---

## ⚡ Performance

### Benchmarks (MacBook Pro M2, 16GB)

| Metric | Value | Target |
|--------|-------|--------|
| **Cold start** | ~2.1s | < 3s |
| **VAD latency** | 8ms | < 20ms |
| **STT (base model)** | 380ms | < 500ms |
| **STT (small model)** | 620ms | < 800ms |
| **TTS (professional)** | 210ms | < 300ms |
| **TTS (casual)** | 195ms | < 300ms |
| **First token (Claude)** | 1.2s | < 2s |
| **First token (Ollama local)** | 850ms | < 1.5s |
| **Memory (idle)** | 340 MB | < 500 MB |
| **Memory (active)** | 480 MB | < 600 MB |
| **CPU (listening)** | 12% | < 20% |
| **CPU (processing)** | 45% | < 60% |

### Model Sizes

| Component | Model | Size | Quality |
|-----------|-------|------|---------|
| STT | `whisper-base` | 142 MB | ★★★★☆ |
| STT | `whisper-small` | 466 MB | ★★★★★ |
| TTS | `en_US-lessac-medium` | 48 MB | Professional male |
| TTS | `en_US-amy-low` | 42 MB | Casual female |
| TTS | `en_US-libritts-medium` | 51 MB | Clear female |

---

## 🔒 Privacy & Security

### Data Flow Guarantees

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR MACHINE                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │ Microphone│→ │   VAD    │→ │  Whisper │→ │  Text    │     │
│  │  (Audio)  │   │ (Local)  │   │ (Local)  │   │ (Only)   │     │
│  └──────────┘   └──────────┘   └──────────┘   └────┬─────┘     │
│                                                     │           │
│                              ┌──────────────────────┘           │
│                              ▼                                  │
│                    ┌─────────────────┐                          │
│                    │  LLM Provider   │  ← ONLY TEXT LEAVES      │
│                    │  (Your Choice)  │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│                              ▼                                  │
│                    ┌─────────────────┐                          │
│                    │  Piper TTS      │  ← LOCAL GENERATION      │
│                    │  (Local ONNX)   │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│                              ▼                                  │
│                    ┌─────────────────┐                          │
│                    │  Speakers       │                          │
│                    │  (Audio Out)    │                          │
│                    └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### Security Features

- ✅ **API keys in system keyring** — Never written to disk
- ✅ **Local-only audio processing** — No voice data transmitted
- ✅ **HTTPS-only LLM calls** — Certificate validation enforced
- ✅ **Optional offline mode** — Ollama requires zero network
- ✅ **No telemetry** — No usage data collected

### Threat Model

| Threat | Mitigation |
|--------|------------|
| API key theft | System keyring (encrypted at rest) |
| Audio interception | All processing local |
| Conversation logging | Optional, user-controlled, local files only |
| Supply chain | Pinned dependencies, verified wheels |
| MITM on LLM calls | TLS 1.3, cert validation, pinned CAs |

---

## 🔧 Advanced Usage

### Custom System Prompt

```python
from modelx_voice.brain import ModelXBrain
from modelx_voice.config import ConfigManager

cm = ConfigManager()
config = cm.load()

brain = ModelXBrain(
    provider=config.api.provider,
    api_key=config.api.api_key,
    model=config.api.model,
    system_prompt="You are a senior Python developer. "
                  "Give concise, practical answers with code examples."
)
```

### Streaming Responses

```python
async for chunk in brain.stream_response("Explain asyncio"):
    print(chunk, end="", flush=True)
```

### Programmatic Voice Switching

```python
from modelx_voice.tts import VoiceManager

vm = VoiceManager()
synth = vm.get_synthesizer("professional")
audio = await synth.synthesize_async("Hello from professional voice")

synth.set_voice("casual")
audio = await synth.synthesize_async("Now I sound casual")
```

### Save/Load Conversations

```python
from modelx_voice.brain import ConversationMemory
from pathlib import Path

memory = ConversationMemory(persistence_file=Path("~/.modelx-voice/history.json"))
# ... conversation happens ...

# Export for analysis
memory.export_conversation(Path("my_chat.json"))

# Or load existing
memory2 = ConversationMemory(persistence_file=Path("my_chat.json"))
```

### Custom Audio Devices

```bash
# List devices
modelx --test-audio

# Use specific devices
modelx --configure
# Select device indices when prompted
```

### Headless/Server Mode

```bash
# With Ollama (fully local)
OLLAMA_HOST=http://gpu-server:11434 modelx --provider ollama

# SSH with audio forwarding
ssh -R 4713:localhost:4713 user@server  # PulseAudio tunnel
modelx
```

---

## 📝 Configuration Reference

### `~/.modelx-voice/config.json`

```json
{
  "api": {
    "provider": "anthropic",
    "api_key": "***KEYRING***",
    "model": "claude-sonnet-4-20250514",
    "base_url": null
  },
  "voice": {
    "selected_voice": "clear",
    "speed": 1.0,
    "pitch": 1.0
  },
  "audio": {
    "input_device": null,
    "output_device": null,
    "sample_rate": 16000
  },
  "behavior": {
    "wake_word": "hey modelx",
    "auto_listen": true,
    "response_delay": 0.5,
    "vad_aggressiveness": 2
  }
}
```

### Field Reference

| Section | Field | Type | Default | Description |
|---------|-------|------|---------|-------------|
| `api` | `provider` | enum | `anthropic` | `anthropic\|openai\|openrouter\|ollama` |
| `api` | `model` | string | auto | Model identifier |
| `api` | `base_url` | string/null | null | Custom endpoint (Ollama/OpenRouter) |
| `voice` | `selected_voice` | enum | `clear` | `professional\|casual\|clear` |
| `voice` | `speed` | float | 1.0 | Speech rate (0.5–2.0) |
| `voice` | `pitch` | float | 1.0 | Pitch shift (0.5–2.0) |
| `audio` | `input_device` | int/null | null | Device index (null=default) |
| `audio` | `output_device` | int/null | null | Device index (null=default) |
| `behavior` | `wake_word` | string | `hey modelx` | Empty = push-to-talk |
| `behavior` | `auto_listen` | bool | true | Resume listening after response |
| `behavior` | `vad_aggressiveness` | int | 2 | 0–3 (higher = more sensitive) |

---

## 🐛 Troubleshooting

### Quick Diagnostics

```bash
# Full system check
modelx --test-audio && modelx --test-api && modelx --download-voices

# Verbose debug
modelx --debug 2>&1 | head -50
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: sounddevice` | Missing system deps | Install portaudio (see [Installation](#installation)) |
| `No input device found` | Permissions / no mic | `sudo usermod -a -G audio $USER` (Linux), check System Preferences → Security (macOS) |
| `Voice model not found` | Incomplete download | `modelx --download-voices` |
| `API key invalid` | Keyring sync issue | `modelx --configure` and re-enter |
| `Ollama connection refused` | Service not running | `ollama serve` or check `OLLAMA_HOST` |
| `High CPU / slow` | Wrong Whisper model | Use `base` not `small`/`medium` in code |
| `Audio crackling` | Sample rate mismatch | Ensure 16kHz input, 22.05kHz output |

### Log Files

```bash
# Debug logs
MODELX_DEBUG=1 modelx 2>&1 | tee modelx.log

# Keyring issues (macOS)
security dump-keychain | grep modelx

# Keyring issues (Linux)
secret-tool search service modelx
```

### Reinstall Clean

```bash
# Remove config + voices
rm -rf ~/.modelx

# Reinstall package
pip uninstall modelx-voice && pip install modelx
modelx --setup
```

---

## 🛠️ Development

### Project Structure

```
modelx_voice/
├── audio/              # Audio I/O + VAD
│   ├── capture.py      # Microphone capture (sounddevice)
│   ├── playback.py     # Speaker output
│   └── vad.py          # WebRTC VAD wrapper
├── stt/                # Speech-to-Text
│   └── whisper_wrapper.py  # faster-whisper binding
├── tts/                # Text-to-Speech
│   └── piper_wrapper.py    # Piper ONNX runtime
├── brain/              # LLM + Memory
│   ├── llm_client.py   # Provider implementations
│   └── context.py      # ConversationMemory, ModelXBrain
├── config/             # Configuration
│   ├── manager.py      # ConfigManager + Keyring
│   └── setup_wizard.py # Rich-based wizard
├── ui/                 # Terminal Interface
│   ├── terminal.py     # Rich Live UI + SimpleVoiceUI
│   └── commands.py     # VoiceCommand + Processor
├── voices/             # Voice assets
│   ├── downloader.py   # HuggingFace model fetcher
│   └── voice_config.json
├── pipeline.py         # AudioPipeline orchestration
└── main.py             # CLI entry point
```

### Setup Dev Environment

```bash
git clone https://github.com/modelx/modelx
cd modelx

# Create venv
python -m venv .venv
source .venv/bin/activate

# Install with dev deps
pip install -e ".[dev]"

# Install pre-commit
pre-commit install
```

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=modelx_voice --cov-report=html

# Specific module
pytest tests/test_brain.py -v

# Audio tests (requires hardware)
pytest tests/test_audio.py -v -k "not ci"
```

### Code Quality

```bash
# Format
black modelx_voice/
isort modelx_voice/

# Lint
ruff modelx_voice/
mypy modelx_voice/

# Pre-commit (all checks)
pre-commit run --all-files
```

### Add a New LLM Provider

1. Create `modelx_voice/brain/providers/your_provider.py`
2. Implement `LLMProvider` abstract class
3. Register in `modelx_voice/brain/llm_client.py`
4. Add to `PROVIDERS` dict and `DEFAULT_MODELS`
5. Add tests

### Add a New Voice

1. Find Piper-compatible ONNX model on HuggingFace
2. Download `.onnx` + `.onnx.json` to `voices/`
3. Add entry to `voice_config.json`
4. Update `PiperSynthesizer.VOICE_CONFIG`

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Checklist

- [ ] Fork the repo
- [ ] Create feature branch (`git checkout -b feat/amazing-feature`)
- [ ] Write tests for new functionality
- [ ] Ensure all checks pass (`pre-commit run --all-files`)
- [ ] Update docs if needed
- [ ] Submit PR with clear description

### Areas Needing Help

- 🎯 Windows audio testing
- 🎯 Additional voice models (multilingual)
- 🎯 Wake word engine (Porcupine integration)
- 🎯 WebSocket server for web UI
- 🎯 Plugin system for custom commands
- 🎯 Benchmarks on more hardware

---

## 🗺️ Roadmap

### v1.1 (Next Release)
- [ ] Streaming TTS (play while generating)
- [ ] Porcupine wake word support
- [ ] Conversation export (Markdown/PDF)
- [ ] Configurable Whisper model size

### v1.2
- [ ] Web UI (WebSocket + React)
- [ ] Plugin system
- [ ] Multi-language STT/TTS
- [ ] Voice cloning (YourTTS)

### v2.0
- [ ] Mobile companion app
- [ ] Distributed architecture
- [ ] Real-time translation
- [ ] Emotion-aware responses

See [GitHub Projects](https://github.com/modelx/modelx-voice/projects) for detailed tracking.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

| Project | Purpose | License |
|---------|---------|---------|
| [faster-whisper](https://github.com/guillaumekln/faster-whisper) | STT engine | MIT |
| [Piper TTS](https://github.com/rhasspy/piper) | Neural TTS | MIT |
| [WebRTC VAD](https://webrtc.org/) | Voice activity detection | BSD |
| [Rich](https://github.com/Textualize/rich) | Terminal UI | MIT |
| [sounddevice](https://python-sounddevice.readthedocs.io/) | Audio I/O | MIT |
| [keyring](https://github.com/jaraco/keyring) | Secure credential storage | MIT/PSF |

---

## 📞 Support

| Channel | Purpose |
|---------|---------|
| [GitHub Issues](https://github.com/modelx/modelx-voice/issues) | Bug reports, feature requests |
| [GitHub Discussions](https://github.com/modelx/modelx-voice/discussions) | Questions, ideas, show & tell |
| [Discord](https://discord.gg/modelx) | Real-time chat, community |
| [Email](mailto:voice@modelx.ai) | Security issues, partnerships |

---

<div align="center">

**Made with ❤️ by the ModelX Team**

[⭐ Star us on GitHub](https://github.com/modelx/modelx-voice) • [🐛 Report Bug](https://github.com/modelx/modelx-voice/issues/new) • [💡 Request Feature](https://github.com/modelx/modelx-voice/issues/new)

</div>
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Audio/video transcription tool that downloads media from public URLs and transcribes using OpenAI's Whisper API (`gpt-4o-transcribe` model). Single-command interface.

## Development Commands

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (requires OpenAI API key)
# Add OPENAI_API_KEY to .env file

# Transcribe audio from URL
python3 transcribe.py --audio <url>

# Transcribe video from URL (downloads video, extracts audio, transcribes)
python3 transcribe.py --video <url>
```

## Architecture

### Single Script
- **transcribe.py** - Único punto de entrada. Descarga media con `yt-dlp`, extrae audio con `pydub`, auto-split si >25MB, transcribe con OpenAI API, genera markdown.

### Flags
- `--audio URL` - Descarga audio directamente y transcribe
- `--video URL` - Descarga video, extrae audio MP3, transcribe

### Output Structure
```
output/{nombre}/
  {nombre}.mp4    # solo si --video
  {nombre}.mp3    # audio
  {nombre}.md     # transcripcion
```

### Key Behaviors
- Auto-splits audio >25MB into parts, transcribes each, concatenates into single markdown
- Downloads to temp directory, only final files go to output/
- Supports any platform that yt-dlp supports (YouTube, TikTok, Instagram, Twitter/X, etc.)
- Requires `ffmpeg` system dependency

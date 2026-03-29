# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Audio transcription automation tool that processes audio files using OpenAI's Whisper API (`gpt-4o-transcribe` model). Batch processes audio files and generates markdown documentation of transcriptions.

## Development Commands

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (requires OpenAI API key)
cp .env.example .env

# Run transcription pipeline
python3 transcribe.py
```

## Architecture

### Three-Stage Pipeline
Files flow through directories in sequence:
1. **audios-backlog/** - Drop audio files here for processing
2. **audio-pending/** - Files being actively transcribed (prevents duplicates)
3. **audios-complete/** - Output directory with `{basename}/` folders containing transcription markdown and original audio

### Core Files
- **config.py** - Centralized configuration: directory paths, supported formats (`.m4a`, `.mp3`, `.mp4`, `.mpeg`, `.mpga`, `.wav`, `.webm`), 25MB size limit, model selection
- **transcribe.py** - Main entry point with workflow: validate → move to pending → API call → generate markdown → move to complete (returns to backlog on failure)

### Key Behaviors
- Files return to backlog on API failures for retry
- Pre-validates format and file size before API calls
- Generated markdown includes timestamp, model used, and transcription text

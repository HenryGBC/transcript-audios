#!/usr/bin/env python3
"""Descarga y transcribe audio/video desde URLs publicas usando OpenAI Whisper."""

import argparse
import math
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import yt_dlp
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

load_dotenv()

# Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-transcribe"
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25MB
OUTPUT_DIR = Path(__file__).parent / "output"


def download_media(url, output_dir, format_type):
    """Descarga media de una URL usando yt-dlp. Retorna el path del archivo."""
    if format_type == "video":
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": str(output_dir / "%(title)s_%(id)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
        }
    else:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": str(output_dir / "%(title)s_%(id)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = Path(ydl.prepare_filename(info))

        # Para audio, yt-dlp cambia la extension despues del postprocesador
        if format_type == "audio":
            filename = filename.with_suffix(".mp3")

    return filename


def extract_audio(video_path, output_dir):
    """Extrae audio MP3 de un archivo de video."""
    print("  Extrayendo audio del video...")
    audio = AudioSegment.from_file(str(video_path))
    audio_path = output_dir / f"{video_path.stem}.mp3"
    audio.export(str(audio_path), format="mp3", bitrate="192k")
    print(f"  Audio extraido: {audio_path.name}")
    return audio_path


def split_audio(audio_path, temp_dir):
    """Divide audio en partes de <25MB. Retorna lista de paths."""
    file_size = audio_path.stat().st_size
    num_parts = math.ceil(file_size / MAX_FILE_SIZE_BYTES)

    print(f"  Archivo grande ({file_size / (1024*1024):.1f}MB), dividiendo en {num_parts} partes...")

    audio = AudioSegment.from_file(str(audio_path))
    part_length = len(audio) // num_parts

    parts = []
    for i in range(num_parts):
        start = i * part_length
        end = len(audio) if i == num_parts - 1 else (i + 1) * part_length
        part = audio[start:end]
        part_path = Path(temp_dir) / f"{audio_path.stem}_part{i + 1}.mp3"
        part.export(str(part_path), format="mp3", bitrate="192k")
        print(f"    Parte {i + 1}/{num_parts} creada")
        parts.append(part_path)

    return parts


def transcribe_audio(client, audio_path):
    """Transcribe un archivo de audio con la API de OpenAI."""
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=MODEL,
            file=audio_file,
        )
    return transcription.text


def transcribe_with_split(client, audio_path):
    """Transcribe un audio, dividiendolo si excede 25MB."""
    file_size = audio_path.stat().st_size

    if file_size <= MAX_FILE_SIZE_BYTES:
        print("  Transcribiendo...")
        text = transcribe_audio(client, audio_path)
        print(f"  Transcripcion completada ({len(text)} caracteres)")
        return text

    # Dividir y transcribir cada parte
    with tempfile.TemporaryDirectory() as temp_dir:
        parts = split_audio(audio_path, temp_dir)
        all_text = []
        for i, part_path in enumerate(parts, 1):
            print(f"  Transcribiendo parte {i}/{len(parts)}...")
            text = transcribe_audio(client, part_path)
            print(f"    Completada ({len(text)} caracteres)")
            all_text.append(text)

    return " ".join(all_text)


def generate_markdown(filename, transcription):
    """Genera contenido Markdown con la transcripcion."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Transcripcion: {filename}

## Metadatos
- **Archivo original:** {filename}
- **Fecha de transcripcion:** {timestamp}
- **Modelo utilizado:** {MODEL}

---

## Transcripcion

{transcription}

---

*Generado automaticamente con OpenAI API*
"""


def process_url(url, mode):
    """Pipeline completo: descarga -> (extrae audio) -> transcribe -> markdown."""
    if not OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY no configurada. Agrega tu key al archivo .env")
        return

    client = OpenAI(api_key=OPENAI_API_KEY)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 1. Descargar
        print(f"Descargando {mode} de: {url}")
        media_path = download_media(url, temp_path, mode)
        print(f"Descargado: {media_path.name}")

        # 2. Extraer audio si es video
        if mode == "video":
            audio_path = extract_audio(media_path, temp_path)
        else:
            audio_path = media_path

        # 3. Preparar carpeta de salida
        base_name = audio_path.stem
        output_folder = OUTPUT_DIR / base_name
        output_folder.mkdir(parents=True, exist_ok=True)

        # 4. Transcribir
        transcription = transcribe_with_split(client, audio_path)

        # 5. Generar markdown
        markdown = generate_markdown(base_name, transcription)
        md_path = output_folder / f"{base_name}.md"
        md_path.write_text(markdown, encoding="utf-8")
        print(f"  Markdown guardado: {md_path}")

        # 6. Mover archivos finales a output
        final_audio = output_folder / f"{base_name}.mp3"
        shutil.copy2(str(audio_path), str(final_audio))

        if mode == "video":
            final_video = output_folder / f"{base_name}{media_path.suffix}"
            shutil.copy2(str(media_path), str(final_video))
            print(f"  Video guardado: {final_video}")

        print(f"  Audio guardado: {final_audio}")

    print(f"\n[OK] Completado: {output_folder}/")


def main():
    parser = argparse.ArgumentParser(
        description="Descarga y transcribe audio/video desde URLs publicas."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audio", metavar="URL", help="URL de audio para descargar y transcribir")
    group.add_argument("--video", metavar="URL", help="URL de video para descargar, extraer audio y transcribir")

    args = parser.parse_args()

    if args.audio:
        url = args.audio
        mode = "audio"
    else:
        url = args.video
        mode = "video"

    print("=" * 50)
    print("Transcriptor de Audio/Video")
    print("=" * 50)

    try:
        process_url(url, mode)
    except Exception as e:
        print(f"\n[ERROR] {e}")

    print("=" * 50)


if __name__ == "__main__":
    main()

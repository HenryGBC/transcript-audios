#!/usr/bin/env python3
"""Script principal para transcribir archivos de audio usando OpenAI Whisper."""

import shutil
from datetime import datetime
from pathlib import Path

from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    BACKLOG_DIR,
    PENDING_DIR,
    COMPLETE_DIR,
    TRANSCRIPTION_MODEL,
    SUPPORTED_FORMATS,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    ensure_directories,
    validate_config,
)


def get_audio_files(directory: Path) -> list[Path]:
    """Obtiene la lista de archivos de audio en el directorio."""
    audio_files = []
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            audio_files.append(file_path)
    return sorted(audio_files)


def validate_file(file_path: Path) -> tuple[bool, str]:
    """Valida que el archivo sea procesable."""
    # Verificar formato
    if file_path.suffix.lower() not in SUPPORTED_FORMATS:
        return False, f"Formato no soportado: {file_path.suffix}"

    # Verificar tamano
    file_size = file_path.stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        return False, f"Archivo muy grande: {size_mb:.1f}MB (maximo: {MAX_FILE_SIZE_MB}MB)"

    return True, "OK"


def transcribe_audio(client: OpenAI, audio_path: Path) -> str:
    """Transcribe un archivo de audio usando la API de OpenAI."""
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=TRANSCRIPTION_MODEL,
            file=audio_file,
        )
    return transcription.text


def generate_markdown(filename: str, transcription: str) -> str:
    """Genera el contenido Markdown con la transcripcion."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown = f"""# Transcripcion: {filename}

## Metadatos
- **Archivo original:** {filename}
- **Fecha de transcripcion:** {timestamp}
- **Modelo utilizado:** {TRANSCRIPTION_MODEL}

---

## Transcripcion

{transcription}

---

*Generado automaticamente con OpenAI API*
"""
    return markdown


def process_audio(client: OpenAI, audio_path: Path) -> bool:
    """Procesa un archivo de audio completo."""
    filename = audio_path.name
    base_name = audio_path.stem

    print(f"  Procesando: {filename}")

    # Validar archivo
    is_valid, message = validate_file(audio_path)
    if not is_valid:
        print(f"    [SKIP] {message}")
        return False

    # Mover a pending
    pending_path = PENDING_DIR / filename
    shutil.move(str(audio_path), str(pending_path))
    print(f"    Movido a pending...")

    try:
        # Transcribir
        print(f"    Transcribiendo...")
        transcription = transcribe_audio(client, pending_path)
        print(f"    Transcripcion completada ({len(transcription)} caracteres)")

        # Crear carpeta de salida
        output_dir = COMPLETE_DIR / base_name
        output_dir.mkdir(exist_ok=True)

        # Generar y guardar Markdown
        markdown_content = generate_markdown(filename, transcription)
        markdown_path = output_dir / f"{base_name}.md"
        markdown_path.write_text(markdown_content, encoding="utf-8")
        print(f"    Markdown guardado: {markdown_path.name}")

        # Mover audio a complete
        final_audio_path = output_dir / filename
        shutil.move(str(pending_path), str(final_audio_path))
        print(f"    [OK] Completado: {output_dir.name}/")

        return True

    except Exception as e:
        # En caso de error, devolver a backlog
        print(f"    [ERROR] {e}")
        if pending_path.exists():
            shutil.move(str(pending_path), str(BACKLOG_DIR / filename))
            print(f"    Devuelto a backlog")
        return False


def main():
    """Funcion principal."""
    print("=" * 50)
    print("Transcriptor de Audio con OpenAI Whisper")
    print("=" * 50)

    # Validar configuracion
    try:
        validate_config()
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        return

    # Crear directorios
    ensure_directories()

    # Inicializar cliente de OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Obtener archivos a procesar
    audio_files = get_audio_files(BACKLOG_DIR)

    if not audio_files:
        print(f"\nNo hay archivos de audio en: {BACKLOG_DIR}/")
        print(f"Formatos soportados: {', '.join(sorted(SUPPORTED_FORMATS))}")
        return

    print(f"\nArchivos encontrados: {len(audio_files)}")
    print("-" * 50)

    # Procesar cada archivo
    successful = 0
    failed = 0

    for audio_path in audio_files:
        if process_audio(client, audio_path):
            successful += 1
        else:
            failed += 1
        print()

    # Resumen
    print("=" * 50)
    print(f"Completados: {successful}")
    print(f"Fallidos/Saltados: {failed}")
    print("=" * 50)


if __name__ == "__main__":
    main()

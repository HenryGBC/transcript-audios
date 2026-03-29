"""Configuracion centralizada para el script de transcripcion."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# API Key de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent

# Rutas de carpetas
BACKLOG_DIR = BASE_DIR / "audios-backlog"
PENDING_DIR = BASE_DIR / "audio-pending"
COMPLETE_DIR = BASE_DIR / "audios-complete"

# Configuracion de transcripcion
# gpt-4o-transcribe: Mejor precision (8.9% WER), mejor con acentos y ruido
TRANSCRIPTION_MODEL = "gpt-4o-transcribe"
SUPPORTED_FORMATS = {".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".ogg", ".wav", ".webm"}
MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # 25MB en bytes


def ensure_directories():
    """Crea las carpetas necesarias si no existen."""
    BACKLOG_DIR.mkdir(exist_ok=True)
    PENDING_DIR.mkdir(exist_ok=True)
    COMPLETE_DIR.mkdir(exist_ok=True)


def validate_config():
    """Valida que la configuracion sea correcta."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY no configurada. "
            "Crea un archivo .env con tu API key de OpenAI."
        )

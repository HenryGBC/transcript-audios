import sys
import os
from pydub import AudioSegment

FORMAT_MAP = {"m4a": "ipod"}

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 split_audio.py <archivo_audio> <numero_partes>")
        sys.exit(1)

    audio_path = sys.argv[1]
    num_parts = int(sys.argv[2])

    if not os.path.isfile(audio_path):
        print(f"Error: no se encontro el archivo '{audio_path}'")
        sys.exit(1)

    if num_parts < 2:
        print("Error: el numero de partes debe ser al menos 2")
        sys.exit(1)

    basename = os.path.splitext(os.path.basename(audio_path))[0]
    ext = os.path.splitext(audio_path)[1].lstrip(".")

    audio = AudioSegment.from_file(audio_path)
    part_length = len(audio) // num_parts

    backlog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios-backlog")
    os.makedirs(backlog_dir, exist_ok=True)

    for i in range(num_parts):
        start = i * part_length
        end = len(audio) if i == num_parts - 1 else (i + 1) * part_length
        part = audio[start:end]
        output_path = os.path.join(backlog_dir, f"{basename}_part{i + 1}.{ext}")
        part.export(output_path, format=FORMAT_MAP.get(ext, ext))
        print(f"Creado: {output_path}")

    print(f"\n{num_parts} partes guardadas en {backlog_dir}")

if __name__ == "__main__":
    main()

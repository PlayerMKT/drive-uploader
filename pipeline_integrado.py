# pipeline_integrado.py
#!/usr/bin/env python3

"""
Pipeline Integrado: YouTube Automation + Drive Uploader

Este script executa seu pipeline de criação de vídeos (youtube-automation)
e em seguida faz upload automático de TODOS os assets gerados para o
Google Drive, organizando-os em pastas hierárquicas por data e tipo.
"""

import os
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Carrega credenciais do .env
load_dotenv()

# Credenciais Drive Uploader
DRIVE_CLIENT_ID     = os.getenv("DRIVE_CLIENT_ID")
DRIVE_CLIENT_SECRET = os.getenv("DRIVE_CLIENT_SECRET")
DRIVE_PROJECT_ID    = os.getenv("DRIVE_PROJECT_ID")         # drive-uploader-466418
CODESPACE_URL       = os.getenv("CODESPACE_URL")           # https://glowing-computing-machine-4jg6wwrp9qjphq5pq.github.dev

# Importa seu pipeline de vídeos
from youtube_automation.main import run_pipeline

# Importa o cliente Drive do módulo drive-uploader
from integrations.drive_uploader.backend.drive_client import DriveClient

def main():
    # 1. Executa pipeline de criação de vídeo
    #    Retorna a pasta raiz do projeto gerado, ex: Path("2025-07-20_Tema")
    project_folder: Path = run_pipeline(
        topic="Mistérios do Brasil"  # Exemplo de tema; ajuste conforme desejar
    )

    # 2. Inicializa cliente Drive
    drive = DriveClient(
        client_id    = DRIVE_CLIENT_ID,
        client_secret= DRIVE_CLIENT_SECRET,
        project_id   = DRIVE_PROJECT_ID,
        redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    )

    # 3. Cria pasta de projeto no Drive
    date_str = datetime.date.today().isoformat()
    drive_folder = f"{date_str}_{project_folder.name}"
    root_folder_id = drive.create_folder(drive_folder, parent_id=None)

    # 4. Envia cada subpasta e seus arquivos
    for sub in ("raw", "assets/audio", "assets/images", "assets/thumbnails", "final"):
        local_dir = project_folder / sub
        if not local_dir.exists():
            continue
        # cria subpasta no Drive
        sub_folder_id = drive.create_folder(sub, parent_id=root_folder_id)
        # faz upload de cada arquivo
        for file_path in local_dir.iterdir():
            if file_path.is_file():
                drive.upload_file(
                    local_path = str(file_path),
                    drive_folder_id = sub_folder_id
                )
                print(f"↑ {file_path.name} → {sub} (Drive)")

    print("✅ Pipeline integrado concluído com sucesso!")

if __name__ == "__main__":
    main()

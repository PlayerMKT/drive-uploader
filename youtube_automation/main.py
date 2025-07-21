import logging
import os
import datetime
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Módulos de geração e montagem
# ---------------------------------------------------------------------------
from youtube_automation.tts_module import synthesize_text
from youtube_automation.sdxl_module import generate_sdxl_images
from youtube_automation.imagen_module import generate_imagen4_images
from youtube_automation.assembly import VideoAssemblyModule
from youtube_automation.merge_audio import merge_wav_files

# ---------------------------------------------------------------------------
# Estrutura de dados para representar o vídeo
# ---------------------------------------------------------------------------
class VideoData:
    def __init__(self, title: str, scenes: List[str], audio_path: str):
        self.title = title
        self.scenes = scenes
        self.audio_path = audio_path

def _sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos para nomes de arquivos/pastas."""
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

# ---------------------------------------------------------------------------
# Função principal do Pipeline
# ---------------------------------------------------------------------------
def run_pipeline(topic: str) -> Path:
    """
    Executa o pipeline completo de geração de vídeo para um determinado tópico.

    Args:
        topic: O tema do vídeo a ser gerado.

    Returns:
        O caminho (Path) para a pasta do projeto contendo todos os assets e o vídeo final.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info(f"Iniciando pipeline para o tópico: {topic}")

    # --- 1. Criar estrutura de pastas do projeto ---
    date_str = datetime.date.today().isoformat()
    sanitized_topic = _sanitize_filename(topic).replace(' ', '_')
    project_name = f"{date_str}_{sanitized_topic}"
    
    # Usar um diretório 'output' na raiz do 'youtube_automation'
    base_output_dir = Path(__file__).parent / "output"
    project_folder = base_output_dir / project_name
    
    # Criação das pastas
    assets_dir = project_folder / "assets"
    sub_folders = {
        "raw": project_folder / "raw",
        "audio": assets_dir / "audio",
        "images": assets_dir / "images",
        "thumbnails": assets_dir / "thumbnails",
        "final": project_folder / "final"
    }
    for folder in sub_folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Estrutura de pastas criada em: {project_folder}")

    # --- 2. Geração de Roteiro e Cenas (Placeholder) ---
    # Em uma implementação real, aqui entraria a chamada para a IA gerar o roteiro
    scenes = [
        f"Cena 1 sobre {topic}: A introdução.",
        f"Cena 2 sobre {topic}: O desenvolvimento do mistério.",
        f"Cena 3 sobre {topic}: A conclusão surpreendente."
    ]
    
    # --- 3. Síntese de voz (TTS) para cada cena ---
    audio_paths = []
    for idx, scene_text in enumerate(scenes, start=1):
        wav_path = sub_folders["audio"] / f"scene_{idx}.wav"
        synthesize_text(scene_text, str(wav_path))
        audio_paths.append(str(wav_path))
    
    final_audio_path = sub_folders["audio"] / "final_audio.wav"
    merge_wav_files(audio_paths, str(final_audio_path))
    logging.info(f"Áudio final gerado em: {final_audio_path}")

    # --- 4. Geração de Imagens ---
    # Usando as cenas como prompts
    logging.info("Gerando imagens com Imagen 4 Ultra...")
    image_paths = generate_imagen4_images(scenes, out_dir=str(sub_folders["images"]), project="drive-uploader-466418")
    logging.info(f"{len(image_paths)} imagens geradas.")

    # --- 5. Montagem do Vídeo ---
    video_data = VideoData(
        title=topic,
        scenes=scenes,
        audio_path=str(final_audio_path)
    )
    video_assets = {
        "image_paths": image_paths,
        "audio_path": str(final_audio_path)
    }

    # O VideoAssemblyModule precisa saber onde salvar o vídeo final
    video_assembler = VideoAssemblyModule(service_manager=None)
    final_video_path = video_assembler.assemble_video_moviepy(
        video_data, 
        video_assets,
        output_dir=str(sub_folders["final"])
    )

    final_video_path_obj = Path(final_video_path)
    if final_video_path_obj and final_video_path_obj.exists():
        logging.info(f"Vídeo final gerado com sucesso em: {final_video_path_obj}")
    else:
        logging.error("Falha crítica: O vídeo final não foi gerado.")
        raise RuntimeError("Não foi possível criar o arquivo de vídeo final.")

    logging.info(f"Pipeline para '{topic}' concluído. Projeto em: {project_folder}")
    
    return project_folder

if __name__ == "__main__":
    # Exemplo de como executar o pipeline diretamente
    try:
        project_path = run_pipeline(topic="YT AUTOMATION DARK FACELESS Q EM ALTA NA GRINGA")
        print(f"\n✅ Execução de teste concluída. Projeto salvo em: {project_path}")
    except Exception as e:
        logging.error(f"Erro na execução de teste do pipeline: {e}", exc_info=True)
        print(f"\n❌ Erro durante a execução de teste: {e}")

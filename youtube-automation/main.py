import json
import logging
import time
import os
from typing import List, Dict

# ---------------------------------------------------------------------------
# Estrutura de dados para representar o vídeo
# ---------------------------------------------------------------------------
class VideoData:
    def __init__(self, title: str, scenes: List[str], audio_path: str):
        self.title = title
        self.scenes = scenes
        self.audio_path = audio_path

# ---------------------------------------------------------------------------
# Módulos de geração e montagem
# ---------------------------------------------------------------------------
from tts_module import synthesize_text
from sdxl_module import generate_sdxl_images
from imagen_module import generate_imagen4_images
from assembly import VideoAssemblyModule

# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Função main() iniciada.")

    # --- Criar pastas de assets e saída ---
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/videos", exist_ok=True)

    # --- 1. Síntese de voz TTS para cada cena ---
    scenes = [
        "Esta é a primeira cena do nosso vídeo.",
        "Aqui temos a segunda cena, mostrando mais detalhes.",
        "Por fim, a terceira cena com encerramento."
    ]
    audio_paths = []
    for idx, texto in enumerate(scenes, start=1):
        wav_path = f"assets/audio/scene_{idx}.wav"
        synthesize_text(texto, wav_path)
        audio_paths.append(wav_path)

    # --- 2. Combinar todos os WAVs num único arquivo ---
    # (opcional; se quiser usar áudios separados, pule esta parte)
    from merge_audio import merge_wav_files
    final_audio = "assets/audio/final_audio.wav"
    merge_wav_files(audio_paths, final_audio)

    # --- 3. Geração de imagens via SDXL e/ ou Imagen 4 Ultra ---
    prompts = scenes  # usamos as mesmas descrições como prompts
    logging.info("Gerando imagens SDXL...")
    sdxl_paths = generate_sdxl_images(prompts, out_dir="assets/images")
    logging.info("Gerando imagens Imagen 4 Ultra...")
    imagen_paths = generate_imagen4_images(prompts, out_dir="assets/images")

    # Escolha quais imagens usar (SDXL ou Imagen4)
    images_to_use = sdxl_paths  # ou imagen_paths

    # --- 4. Montagem do vídeo com MoviePy ---
    dummy_video_data = VideoData(
        title="Vídeo IA Automático",
        scenes=scenes,
        audio_path=final_audio
    )
    dummy_assets = {
        "image_paths": images_to_use,
        "audio_path": final_audio
    }

    video_assembler = VideoAssemblyModule(service_manager=None)
    logging.info("VideoAssemblyModule instanciado.")

    try:
        final_video_path = video_assembler.assemble_video_moviepy(dummy_video_data, dummy_assets)
        logging.info(f"Vídeo gerado em: {final_video_path}")
        if os.path.exists(final_video_path):
            logging.info("Processo concluído com sucesso.")
        else:
            logging.error("Falha: vídeo não encontrado após rendering.")
    except Exception as e:
        logging.error(f"Erro CRÍTICO na montagem do vídeo: {e}", exc_info=True)
        print("\n--- ERRO AO MONTAR O VÍDEO ---")
        print(f"Erro: {e}")

    logging.info("Script principal finalizado.")

if __name__ == "__main__":
    main()

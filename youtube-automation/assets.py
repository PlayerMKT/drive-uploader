from typing import Dict
from google.cloud import texttospeech
import time
import google.generativeai as genai

class AssetProductionModule:
    def __init__(self, service_manager):
        self.service_manager = service_manager
        self.tts_client = texttospeech.TextToSpeechClient()
    
    def generate_audio_tts(self, script: str, output_path: str) -> str:
        """
        Gera áudio com Google TTS (1M caracteres grátis/mês)
        """
        # Configuração para voz brasileira natural
        synthesis_input = texttospeech.SynthesisInput(text=script)
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name="pt-BR-Neural2-A",  # Voz feminina brasileira
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )
        
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        
        return output_path
    
    def generate_thumbnails_gemini(self, title: str) -> Dict[str, str]:
        """
        Gera thumbnails A/B usando Gemini 2.0 Flash Image Generation
        """
        thumbnails = {}
        
        prompts = {
            'A': f"""
            Crie uma thumbnail profissional de YouTube para "{title}".
            ESPECIFICAÇÕES:
            - Resolução: 1280x720 pixels
            - Pessoa com expressão de susto/surpresa
            - Cores vibrantes: vermelho, amarelo, contraste alto
            - Texto legível em português
            - Estilo: Realista, cinematográfico
            - Elementos: Sombras dramáticas, lighting profissional
            """,
            'B': f"""
            Crie uma thumbnail atmosférica de YouTube para "{title}".
            ESPECIFICAÇÕES:
            - Resolução: 1280x720 pixels
            - Ambiente misterioso, silhuetas
            - Cores escuras: azul profundo, roxo, preto
            - Texto com efeito de brilho
            - Estilo: Artístico, gótico
            - Elementos: Neblina, elementos sobrenaturais
            """
        }
        
        for version, prompt in prompts.items():
            response = genai.GenerativeModel('gemini-2.0-flash').generate_content(
                prompt,
                generation_config={
                    "response_modalities": ["IMAGE", "TEXT"],
                    "temperature": 0.7
                }
            )
            
            thumbnail_path = f"thumbnail_{version}_{int(time.time())}.jpg"
            if response.parts:
                for part in response.parts:
                    if part.inline_data:
                        with open(thumbnail_path, "wb") as f:
                            f.write(part.inline_data.data)
            
            thumbnails[version] = thumbnail_path
        
        return thumbnails
    
    def generate_scene_images(self, scenes: list) -> list:
        """
        Gera imagens para cenas do roteiro
        """
        scene_images = []
        for i, scene in enumerate(scenes):
            prompt = f"Crie imagem para cena de horror: {scene[:100]}"
            response = genai.GenerativeModel('gemini-2.0-flash').generate_content(prompt)
            image_path = f"scene_{i}_{int(time.time())}.jpg"
            # Salvar imagem (lógica similar ao thumbnail)
            scene_images.append(image_path)
        return scene_images

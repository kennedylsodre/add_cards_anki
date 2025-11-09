
from gtts import gTTS
import json 
import requests
import os
from pathlib import Path
import base64
import io 
from PIL import Image 
import dotenv
import time

class AddCardAnki:

    dotenv.load_dotenv()

    def __init__(self,text_path,audio_path,deck_name,payload_path): 
        self.anki_url = "http://localhost:8765" 
        self.path_folder_audio = audio_path
        self.path_folder_text = text_path 
        self.payload_path = 'payload_anki.json'
        self.deck_name = deck_name
        self.payload_path = payload_path 

    def read_file(self):

        with open(self.path_folder_text,'r', encoding='utf-8') as f:
            file = f.read()
            self.file = file

    def generate_json_deck(self): 

        dict_decks = {}

        for card, line in enumerate(self.file.splitlines()):
            front = line.split(';')[0]
            back = f'{line.split(";")[1]}<br><img src="card_{card}.png">'
            path_audio = f'{self.path_folder_audio}/card_{card}.mp3'
            path_img = f'{self.path_folder_audio}/card_{card}.png'
            img_prompt = line.split(";")[1]
            list_card = [front,back,path_audio,path_img,img_prompt]
            dict_decks[card] = list_card
        
        self.dict_decks = dict_decks


    def generate_audio(self,sentence,path_audio):

        tts = gTTS(str(sentence), lang='en')

        return tts.save(path_audio)
    
    def generate_image(self, sentence, path_image, tentativas=3):
        """
        Gera uma imagem a partir de uma frase (sentence) usando a API do Pollinations
        e salva o resultado no caminho path_image.
        """
        prompt = sentence.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{prompt}"
    
        for i in range(tentativas):
            try:
                print(f"🔹 Tentando gerar imagem ({i+1}/{tentativas}) para: {sentence}")
                response = requests.get(url, timeout=60)
                response.raise_for_status()
    
                # Salva o conteúdo da imagem no disco
                with open(path_image, "wb") as f:
                    f.write(response.content)
    
                print(f"✅ Imagem salva em: {path_image}")
                return path_image  # retorna o caminho do arquivo salvo
    
            except Exception as e:
                print(f"⚠️ Erro ao gerar imagem ({i+1}/{tentativas}): {e}")
                if i < tentativas - 1:
                    print("⏳ Aguardando 5s e tentando de novo...")
                    time.sleep(5)
                else:
                    print(f"❌ Falha ao gerar imagem para: {sentence}")
                    return None


    def convert_base64(self,type_file,path,sentence): 
        if type_file == 'audio':
            self.generate_audio(sentence, path)
            

            path_audio = os.path.abspath(path)

            with open(path_audio, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")
            
            return audio_base64
        
        elif type_file == 'img':
            self.generate_image(sentence, path)

            path_image = os.path.abspath(path)

            with open(path_image, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

            return image_base64
        
    def post_image(self, img,card):

        return requests.post(self.anki_url, json={
                "action": "storeMediaFile",
                "version": 6,
                "params": {
                    "filename": f"card_{card}.png",
                    "data": img
                    }
                }
                )

    def fill_payload(self,card):

        with open(self.payload_path,'r') as payload:
            payload = json.load(payload)

        front = self.dict_decks[card][0]
        back = self.dict_decks[card][1]
        path_audio = self.dict_decks[card][2]
        path_image = self.dict_decks[card][3] 
        prompt_image = self.dict_decks[card][4] 


        img_base_64 = self.convert_base64('img',path_image,prompt_image)

        self.post_image(img_base_64,card)

        payload['params']['note']['deckName'] = self.deck_name
        payload["params"]["note"]["fields"]["Front"] = front
        payload["params"]["note"]["fields"]["Back"] = back

        audio_base64 = self.convert_base64('audio',path_audio,front)   
        

        payload["params"]["note"]["audio"] = [
        {
            "filename":  os.path.basename(path_audio),
            'data' : audio_base64,
            "fields": ["Front"]
        }
        ]

        self.payload = payload


    def add_card(self, payload): 

        response = requests.post(self.anki_url,data = json.dumps(payload))
        print(response.json())

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
import uuid
import replicate

class AddCardAnki:

    dotenv.load_dotenv('../.env')

    def __init__(self,text_path,audio_path,deck_name,payload_path): 
        self.anki_url = "http://localhost:8765" 
        self.path_folder_audio = audio_path
        self.path_folder_text = text_path 
        self.payload_path = 'payload_anki.json'
        self.deck_name = deck_name
        self.payload_path = payload_path 
        self.token_replicate = os.getenv("ENGLISH_GENERATE") 
        os.environ['REPLICATE_API_TOKEN'] = self.token_replicate
        

    def read_file(self):

        with open(self.path_folder_text,'r', encoding='utf-8') as f:
            file = f.read()
            self.file = file

    def generate_json_deck(self): 

        dict_decks = {}

        for card, line in enumerate(self.file.splitlines()):
            
            id_img = uuid.uuid4()
            front = line.split(';')[0]
            back = f'{line.split(";")[1]}<br><img src="card_{card}_{id_img}.png">'
            path_audio = f'{self.path_folder_audio}/card_{card}.mp3'
            path_img = f'{self.path_folder_audio}/card_{card}_{id_img}.png'
            img_prompt = line.split(";")[2]
            audio_prompt = line.split(";")[3]
            list_card = [front,back,path_audio,path_img,img_prompt,audio_prompt]
            dict_decks[card] = list_card
        
        self.dict_decks = dict_decks


    def generate_audio(self,sentence,path_audio):

        tts = gTTS(str(sentence), lang='en')

        return tts.save(path_audio)
    


    def generate_image(self, sentence, path_image, tentativas=50):

        print(f'Gerando imagem para {sentence}')    
        prompt = sentence.replace(" ", "%20")

        output = replicate.run(
                    "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
            input={"prompt": prompt}
        )
        image_url = output[0]

        img = requests.get(image_url).content

        print(f'Imagem geranda, salvando imagaem em {path_image}')

        with open(path_image, "wb") as f:
            f.write(img)
        
        return path_image

        print("Imagem salva!")  


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
        
    def post_image(self, img,path_img):

        return requests.post(self.anki_url, json={
                "action": "storeMediaFile",
                "version": 6,
                "params": {
                    "filename":path_img,
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
        promppt_audio = self.dict_decks[card][5] 

        img_base_64 = self.convert_base64('img',path_image,prompt_image)

        self.post_image(img_base_64, path_image)

        payload['params']['note']['deckName'] = self.deck_name
        payload["params"]["note"]["fields"]["Front"] = front
        payload["params"]["note"]["fields"]["Back"] = back

        audio_base64 = self.convert_base64('audio',path_audio,promppt_audio)   
        

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

    def unsuspend_cards(self):
        payload = {
            "action": "findCards",
            "version": 6,
            "params": {
                "query": "is:suspended"
            }
        }

        response_unsespended = requests.post(
            self.anki_url,
            data=json.dumps(payload)
        ).json() 

        cards = response_unsespended.get('result', [])

        if len(cards) < 4:
            print("Nenhum card suspenso suficiente encontrado.")
            return

        cards = cards[:4]

        payload = {
            "action": "unsuspend",
            "version": 6,
            "params": {
                "cards": cards
            }
        }

        response_unsuspended = requests.post(
            self.anki_url,
            data=json.dumps(payload)
        ).json()

        print(response_unsuspended)




        

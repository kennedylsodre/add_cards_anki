#%%
from add_card import AddCardAnki
from tqdm import tqdm
import argparse
import json
# %%
def main(
        text_path
        ,audio_path
        ,deck_name 
):
    add = AddCardAnki(
        text_path=f'{text_path}',
        audio_path=f'{audio_path}',
        deck_name= deck_name,
        payload_path= 'payload_anki.json'
    )

    add.read_file() 
    add.generate_json_deck()

    for key in add.dict_decks.keys():
        
        add.fill_payload(card=key)
        #print(add.payload)
        add.add_card(add.payload)
        print(f'Card {key} adicionado com suceso')

def get_args_from_json(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
#%%
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='../config.json', help='Arquivo de configuração JSON')
    args_cli = parser.parse_args()

    cfg = get_args_from_json(args_cli.config)

    main(
        text_path=cfg['text_path'],
        audio_path=cfg['audio_path'],
        deck_name=cfg['deck_name']
    )

# %%

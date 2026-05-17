#%%
import requests
import json 

anki_url = "http://localhost:8765" 
payload = {
  "action": "findCards",
  "version": 6,
  "params": {
    "query": "deck:Mineração"
  }
}
response = requests.post(anki_url,data = json.dumps(payload))
print(response.json())
# %%

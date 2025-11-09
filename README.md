# 🧠 Automatizando Anki — Geração Automática de Cartões com Áudio e Imagem

> **Crie decks do Anki automaticamente a partir de frases em texto**, com áudio gerado por IA (gTTS), imagens automáticas (Pollinations AI) e integração direta com o **AnkiConnect API**.  
> Tudo com um único comando. 🔥  

---

## 🚀 Objetivo

O projeto **automatiza o processo de criação de flashcards para o Anki**, especialmente útil para quem:
- Estuda **idiomas**, **vocabulário técnico** ou **frases completas**;
- Quer criar **centenas de cartões multimídia** sem esforço manual;
- Deseja manter um **pipeline reprodutível e escalável** para gerar decks a partir de arquivos de texto.

💡 Em resumo: você fornece um arquivo com frases (ex: “inglês;tradução”), e o script:
1. Gera **áudio** da frase com *Google Text-to-Speech* (gTTS);
2. Gera **imagem** relacionada com *Pollinations AI*;
3. Converte tudo em Base64;
4. Envia diretamente para o seu Anki via **AnkiConnect**, adicionando cartões completos com imagem + áudio + texto.

---

## 🧩 Arquitetura do Projeto

```bash
automatizando_anki/
│
├── add_card.py          # Classe principal (AddCardAnki): gera e envia cartões ao Anki
├── main.py              # Script de orquestração (CLI)
├── sentences.txt        # Frases base (formato: inglês;tradução)
├── config.json          # Caminhos e nome do deck
├── payload_anki.json    # Modelo do payload padrão do AnkiConnect
├── requirements.txt     # Dependências do projeto
├── create_env.bat       # Criação do ambiente Conda
├── add_card.bat         # Execução simplificada (roda o pipeline)
└── README.md            # Este arquivo 🙂
```

### 🔧 Principais tecnologias usadas
| Biblioteca | Função |
|-------------|--------|
| **gTTS** | Gera áudio da frase (Text-to-Speech Google) |
| **Requests** | Comunicação com AnkiConnect e Pollinations |
| **Pillow** | Manipulação de imagens (armazenamento local) |
| **Pollinations API** | Gera imagens ilustrativas com base na frase |
| **AnkiConnect API** | Interface com o Anki Desktop para adicionar cards |
| **dotenv** | Carregamento de variáveis (opcional) |
| **tqdm** | Barra de progresso |

---

## ⚙️ Como funciona

### 1️⃣ Estrutura de entrada
Você fornece um arquivo `sentences.txt` com o seguinte formato:

```
I am learning English every day;Estou aprendendo inglês todos os dias
She likes to read books in the evening;Ela gosta de ler livros à noite
They went to the park yesterday;Eles foram ao parque ontem
```

Cada linha representa **um cartão**, sendo:
- antes do `;` → lado **Front** (ex: inglês)
- depois do `;` → lado **Back** (ex: tradução)

---

### 2️⃣ Execução

Existem duas formas de executar o projeto:

#### 🪄 Modo automático (Windows)
Basta rodar o script `.bat`:

```bash
add_card.bat
```

Isso cria o ambiente (caso necessário) e executa o pipeline completo.

#### 🧠 Modo manual (CLI)
Ative seu ambiente e execute o script Python:

```bash
conda activate anki
python main.py --config config.json
```

---

### 3️⃣ Arquivo de configuração (`config.json`)
Define as entradas e o deck de destino:

```json
{
    "text_path": "../sentences.txt",
    "audio_path": "../data/",
    "deck_name": "deck",
    "conda_env": "anki"
}
```

---

### 4️⃣ Pipeline resumido
```mermaid
flowchart TD
A[Sentences.txt] --> B[AddCardAnki.read_file()]
B --> C[generate_json_deck()]
C --> D[generate_audio()]
C --> E[generate_image()]
D & E --> F[convert_base64()]
F --> G[post_image()]
G --> H[fill_payload()]
H --> I[add_card() via AnkiConnect]
I --> J[Cartão criado com sucesso 🎉]
```

---

## 💡 Exemplo de cartão gerado

| Lado | Conteúdo |
|------|-----------|
| **Front** | I am learning English every day <br> 🎧 *[áudio gerado]* |
| **Back** | Estou aprendendo inglês todos os dias <br> 🖼️ *imagem gerada automaticamente* |

---

## 🧱 Principais componentes da classe `AddCardAnki`

| Método | Função |
|---------|--------|
| `read_file()` | Lê o arquivo `sentences.txt` |
| `generate_json_deck()` | Cria estrutura de dados com cada cartão |
| `generate_audio()` | Usa gTTS para gerar e salvar áudio |
| `generate_image()` | Chama API do Pollinations e salva imagem |
| `convert_base64()` | Converte áudio/imagem para Base64 |
| `post_image()` | Envia imagem para o Anki (storeMediaFile) |
| `fill_payload()` | Preenche o modelo do cartão (payload) |
| `add_card()` | Faz o POST final via AnkiConnect |

---

## 🧠 Como o Anki é integrado

O projeto usa o **AnkiConnect**, um *add-on* oficial do Anki Desktop.

1. Instale o AnkiConnect:  
   Abra o Anki → `Ferramentas > Complementos > Procurar e instalar` →  
   Cole o código: **2055492159**

2. Certifique-se de que o Anki está **aberto** antes de rodar o script.  
   O servidor padrão roda em `http://localhost:8765`.

---

## 🧩 Exemplo de payload enviado ao Anki
```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "MeuDeck",
      "modelName": "Basic",
      "fields": {
        "Front": "I am learning English every day",
        "Back": "Estou aprendendo inglês todos os dias"
      },
      "audio": [{
        "filename": "card_0.mp3",
        "data": "<base64>",
        "fields": ["Front"]
      }],
      "tags": []
    }
  }
}
```

---

## 🧰 Ambiente e dependências

### Instalar dependências
```bash
pip install -r requirements.txt
```
ou com Conda:
```bash
conda create --name anki python=3.11
conda activate anki
pip install -r requirements.txt
```

Principais pacotes:
```
gTTS
requests
python-dotenv
Pillow
tqdm
```

---

## ⚡ Melhores práticas e dicas

- ✅ Verifique se o **Anki Desktop** está aberto com **AnkiConnect** ativo.  
- ✅ Execute a partir do diretório raiz (onde está o `main.py`).  
- ✅ Verifique se as pastas de **áudio/imagem** existem (ou serão criadas automaticamente).  
- ✅ Evite frases muito longas (gTTS pode falhar).  
- ⚠️ O Pollinations pode retornar imagens abstratas; é ideal para **contextualização visual**, não precisão semântica.

---

## 📈 Roadmap de evolução

- [ ] Paralelizar geração de áudio e imagens (ThreadPool)
- [ ] Logging estruturado
- [ ] Interface web com Streamlit
- [ ] Upload automático de decks `.apkg`
- [ ] Templates de flashcards (Cloze, Image Occlusion, etc.)
- [ ] Suporte a múltiplos idiomas (lang='pt', 'es', etc.)

---

## 👨‍💻 Autor

**Kennedy Lacerda Sodré**  
📊 *Data Analyst & Machine Learning Enthusiast*  
💡 Focado em automação, IA aplicada e aprendizado contínuo.

🔗 [LinkedIn](https://www.linkedin.com/in/kennedylsodre)  
🐙 [GitHub](https://github.com/kennedylsodre)

---

## 🧩 Licença

Este projeto é distribuído sob a licença **MIT**, livre para uso, modificação e aprendizado.

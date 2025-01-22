# Chatbot:

This repository is a part data-driven and AI-related repos for the **BanditGames** project, focusing on integrating chatbot into a gaming platform.

Purpose of this chatbot: Assist players with game rules and platform navigation.  
The chatbot contains an endpoint from which a user can query questions and expect responses.

Example locally:
```
http://localhost:8080/chat
```

Rules come in form of a json object from a `new_rules_queue` RabbitMQ <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANoAAADnCAMAAABPJ7iaAAAAdVBMVEX/ZgD/////aQv/YwD/jF3/WAD/8uz/nXb/XAD/WwD/YAD/zbz/uKD/rY7/UwD/+PX/3ND/fUD/pID/1sf/cij/6eH/gUf/oXv/4tf/p4X/wKn/mW//xrH/vKP/bBj/spX/iVb/djH/y7j/sJH/hk//8+7/cCKVRWFuAAADsUlEQVR4nO3dW2/iMBCG4QnGxXEhIRAOgbbQE///J65Dt6jSljCD8NaTfu/FXo78QERX4DiUHZs2ywGdbVDN5pm4+arqmrmcTOUzJVH7z7q23pxfBZHx+UCIu6f80kz7vIhB+qyljYvONfxdSdFI5o7s5ZFh5iYSqy3QHjmrCFmBbZvzZhYPMWnrgreKsI577tQH5qsVZsa7JimrGVfjZ9ypzPcsZKp4tCn7BSbKX3hDHx1/pl1HozWevwwz5A2tBBeCn0SjLQXLIMMbKrgQyCyj0Tr+qv6bZc28k9BokAitvD3NgwYaaKCBBhpooIEW5/+QoIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmig/QdaDhpooIEGGmiggfajNAcaaKCBBhpooIEGGmig/QIabxmggQYaaL+RxvsRas0/SYW4XyVFp+Wsc0/GgpNUwssV6wgc4QW55cwUjYx3loqMxjquZiJ608LM9yRo5C9ePtyzq06ZJ9Z9w9FpZLtP9VoMpbJgc1FO0xLTyLntbrxre32dHGtCs9Bqta2t5KigLzP3o1u12s2vpbWnzTl/pqtgHzNvlsvN5lpa+tm33tLIV72lkZv0lkZF2Vuae+wtzQx7S6O6v7QBaAoDTWOgaQw0jYGmMdA0BprGQNMYaBoDTWOgaQw0jYGmMdA0BprGQNMYaBoDTWNp0Yz37puu29WWEM3kbjgZf1szdLlYlw7NLjufpDtfSreQpkIz/uIjgufCyzIRmqkZ24/LZ5EtDZp5YmwlDj1JbGnQ7B2PJrqjJQma2/FkWbYT3EKQBo0ryzJlND/j02b8Jw6nQMsFj4af82+ySoEmuafmnf9BkgSNL5M81DkFmujePF0XJGignQItaqCBdgq0qIEG2inQogYaaKdAixpooJ0CLWo9/kbLCs6/KXXR8imfNtV1QUpOm5ro+s6fDJ8m+O0wCZrrPuTpSxtlP0IFG/ODpJQcPpYGzVQ8WqXvt2zybxzZG/8zhJKhkT9cPDBucRDJkqGRsaNO3GJUCLcyJUMLb5ytm83L/XdtmtrK3jJKinY8MO5M12ytS4p220DTGGgaA01joGkMNI2BpjHQNAaaxkDTGGgaA01joGkMNI2BpjHQNAaaxkDTGGgaG9Dhp5cQqwPtr37QXdqZPe3Ee0105Md0V/z0IuJUvFO27eXb5lYZCU/MUZI/ZC2tPAifTJt+rj3hidodeY113vQm7+xxD/qRlpUPs2Fvmr18bKH8A65nY3pZpz/zAAAAAElFTkSuQmCC" alt="emoji" width="20" height="20"> queue

Message schema: [json-schema](#new-game-rules-event-schema)

## Requirements

* Docker
* Python >= 3.10
* Ollama
* Postgres

### Before running the application:

Prerequisites:   

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd chatbot/
docker compose up -d
```

⚠️ If you are planning on using `ollama`, install it locally or use docker compose.  

Local ollama:
```
ollama serve
```

Docker-compose built ollama: 
```
docker exec -it ollama ollama run llama2
```

File structure for environment variables (.env):
```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASSWORD=

GAMEPLATFORM_URL=

OPENAI_API_KEY=
```

## Running the application:

Current chatbot application presents ability to select different aspects of RAG:

* Search type (e.g Postgres vector database)
* Embedding generator (e.g Sentence transformer library)
* Large Language model (e.g. Local ollama)

Example running the application:
```
cd chatbot/
python -m app.main \
--search_type=pgvector \ 
--generator_type=sentence_transformer \
--model_type=ollama \ 
--secrets_type=local

```

Possible argument options:
* --search_type 
  * pgvector
* --secrets_type
  * local
* --model_type
  * ollama
  * openai (OPENAI_API_KEY env variable must be specified)


## Code and type checking during development

Run checking on Python code:
* `isort` organizes imports.
* `black` formats code.
* `mypy` performs static type checks.

```
cd chatbot/
python run_tools.py
```



### Logical flow:
1. Receive a query from the user via POST method
2. Embed the text in the query
3. Find category of the query
4. Find closest text of the query
5. IF category is rules -> Identify the game that the query is talking about
6. Construct a base prompt
7. Feed the prompt to LLM and send response to the user

## Chatbot additional information:

PG_vector utilizes cosine similarity to identify the related text


## JSON object structure:

### New game rules event schema 


```
{
  "type": "object",
  "properties": {
    "gameName": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "price": {
      "type": "number"
    },
    "currency": {
      "type": "string"
    },
    "maxLobbyPlayersAmount": {
      "type": "integer"
    },
    "frontendUrl": {
      "type": "string",
      "format": "uri"
    },
    "backendApiUrl": {
      "type": "string",
      "format": "uri"
    },
    "gameImageUrl": {
      "type": "string",
      "format": "uri"
    },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule": {
            "type": "string"
          },
          "description": {
            "type": "string"
          }
        },
        "required": ["rule", "description"],
        "additionalProperties": false
      }
    }
  },
  "required": [
    "gameName",
    "description",
    "price",
    "currency",
    "maxLobbyPlayersAmount",
    "frontendUrl",
    "backendApiUrl",
    "gameImageUrl",
    "rules"
  ],
  "additionalProperties": false
}

```

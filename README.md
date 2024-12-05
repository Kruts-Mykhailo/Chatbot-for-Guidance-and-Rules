# data_A_I

This repository contains data-driven and AI-related tasks for the BanditGames project, focusing on integrating predictive modeling and chatbot into a gaming platform.

- **Prediction System**  
  - Use machine learning to predict:
    - Player churn
    - Game engagement
    - Win probabilities
    - Player classification (e.g., novice, expert)

- **AI Chatbot**  
  - Assist players with game rules and platform navigation.


## Training models:

All models should be trained on information returned from file Statistics.csv 

## Chatbot:

### Run the application:

Prerequisites:   

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Before running the application:  

Current chatbot application presents ability to select different aspects of RAG:

* Search type (e.g Postgres vector database)
* Embedding generator (e.g Sentence transformer library)
* Large Language model (e.g. Local ollama)

⚠️ If you are planning on using `ollama`, install it locally (version: `llama2`).  

Start ollama
```
ollama serve
```

Example running the application:
```
cd chatbot/
python -m app.main \
--search_type=pgvector \ 
--generator_type=sentence_transformer \
--model_type=ollama

```

After writing code:

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

Things considering to add:
1. `pg_vector` cosine similarity 
2. extracting category of query using LLM
3. transforming a query using LLM for better retrieval

When observed, the distance to the closest embedded text, the distance is around 0.78 -> 0.9. Due to usage of pg_vector, the distance is calculated using euclidian metric.

The Cosine similarity may come in handy due to it being used for direction similarity, and not exactly word to word similarity.
This can be implemented in pg_vector retrieval solution.

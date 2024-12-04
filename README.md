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


## Chatbot information:

Possible problems:
- Identification of category of query.

When observed, the distance to the closest embedded text, the distance is around 0.78 -> 0.9.  
Due to usage of pg_vector, the distance is calculated using euclidian metric.

But the problem that distance is much about how similar the text is. 

The Cosine similarity may come in handy due to it being used for direction similarity, and not exactly word to word similarity.
This should be tried in pg_vector retrieval solution.
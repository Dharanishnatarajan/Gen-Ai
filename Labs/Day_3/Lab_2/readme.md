# Day 3 Lab 2: Signal Studio Router

## Overview
This lab implements a conditional LangGraph router that classifies a message, sends it down a positive, negative, or neutral branch, and returns a response suggestion. It uses Hugging Face's `distilbert-base-uncased-finetuned-sst-2-english` model and keeps an LLM fallback path through Groq or local Ollama.

## How to run
* Install dependencies via `pip install -r requirements.txt`.
* Create a `.env` file based on `.env.example` and set your `GROQ_API_KEY`.
* Ensure Ollama is running locally with the `mistral` model if you plan to rely on the fallback.
* Start the Flask application by running `python app.py`.
* Open `http://localhost:5000` to use the customized Signal Studio interface.

## Design notes
* **LangGraph Conditional Edges:** We define a single decision node `analyze_sentiment` which determines the transition `route_decision` dynamically. Edges connect from `analyze_sentiment` to `POSITIVE`, `NEGATIVE`, and `NEUTRAL` endpoints based on the sentiment output.
* **Thresholds:** A stricter confidence threshold of `0.72` is applied. Lower-confidence classifications fall back to `NEUTRAL`.
* **Response style:** Each branch now returns a practical suggested reply instead of only a sentiment breakdown.
* **State Management:** The Graph uses a strict `WorkflowState` object to store metrics, route data, the original query, and eventual NLP response.

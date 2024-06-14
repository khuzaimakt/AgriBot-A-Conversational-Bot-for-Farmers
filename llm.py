# Importing all the necessary libraries.
from googletrans import Translator
import json
import os
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import requests

# Checking the working directory.
os.getcwd()

class Chatbot:
  def __init__(self, preprompts, source_lang, dest_lang):
    self.preprompts = preprompts
    self.translator = Translator()

    self.source_lang = source_lang
    self.dest_lang = dest_lang

    self.load_model()

  def load_model(self):
    # Loading the Llama model from huggingface. This model is received for educational purposes only and hence is open source for non commercial usecases.
    self.model_name = "meta-llama/Llama-2-7b-chat-hf"

    self.url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
    self.auth_token = "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"

  def find_max_cosine_preprompt(self, query):
    # Create a TfidfVectorizer instance
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the preprompts and query
    tfidf_matrix = tfidf_vectorizer.fit_transform(self.preprompts + [query])

    # Calculate the cosine similarity between the query and all preprompts
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Find the index of the preprompt with the maximum cosine similarity
    max_cosine_index = cosine_similarities.argmax()

    # Return the preprompt with the maximum cosine similarity
    max_cosine_preprompt = self.preprompts[max_cosine_index]

    return max_cosine_preprompt

  def get_model_inference(self, query: str):
    max_cosine_preprompt = self.find_max_cosine_preprompt(query)
    print("Chosen preprompt for the given dataset: {}".format(max_cosine_preprompt.split('\n')[0]))

    inputs = "<s>[INST] <<SYS>>\nYou are a helpful chatbot that is trained on agricultural data. You will provide answers from the prompt given below. If something cannot be extracted from this prompt, then say that the answer is not in your knowledge base." + max_cosine_preprompt + "\n<</SYS>>\n" + query + "  [/INST]"
    response = requests.post(self.url, headers={
        "Authorization": f"Bearer {self.auth_token}"
    }, json={
        "inputs" : inputs
    })
    outputs = response.json()
    model_generation = outputs[0]["generated_text"]
    return model_generation, model_generation.split("[/INST]")[1].strip()

  def translate_text(self, text: str, src : str, dest : str):
    translation = self.translator.translate(text, src=src, dest=dest)
    return translation.text

  def execute_pipeline(self, query : str):
    # Translating the query into the model required language, usually English.
    translated_query = self.translate_text(query, self.source_lang, self.dest_lang)
    # Getting the inference on the model preferred language.
    model_generation, model_answer = self.get_model_inference(translated_query)
    # Translating the query back to the original language to maintain consistency.
    translated_answer = self.translate_text(model_answer, self.dest_lang, self.source_lang)
    # Returning both the model answer and the translated answer for debugging purposes.
    return model_answer, translated_answer

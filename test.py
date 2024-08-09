from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
print("libraries loaded")

import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# model = genai.GenerativeModel('gemini-1.0-pro-latest')
# model = genai.get_model('gemini-1.0-pro-latest')
# response = model.generate_content("The opposite of hot is")
genai.list_models()
# print(response.text)
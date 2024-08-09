from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

import streamlit as st
import os
import sqlite3
import pandas as pd


def read_sql(sql,db):
    connection=sqlite3.connect(db)
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()

    i=0
    for row in rows:
        print(row)
        i=i+1
        if i>=6:
            break
    return rows
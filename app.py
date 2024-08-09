from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

import streamlit as st
import os
import sqlite3
import pandas as pd

import google.generativeai as genai

# configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_gemini_response(questions,prompt):
    model=genai.GenerativeModel('gemini-pro')
    
    # model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
    response=model.generate_content([prompt[0],questions])
    return response.text

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

prompt=[
    """ 
You are an expert in converting English questions to SQL query and have access to the Chinook database schema. 
Given a description or prompt of a data query, generate the corresponding SQL query. 
The SQL query should be accurate, well-formatted, and adhere to the Chinook database schema. 
Below is an overview of the Chinook database schema:

Albums: AlbumId, Title, ArtistId
Artists: ArtistId, Name
Customers: CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId
Employees: EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email
Genres: GenreId, Name
Invoices: InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total
InvoiceLines: InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity
MediaTypes: MediaTypeId, Name
Playlists: PlaylistId, Name
PlaylistTrack: PlaylistId, TrackId
Tracks: TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice
Here are some examples of descriptions and their corresponding SQL queries:
Example 1:

Description: Retrieve the names of all tracks along with the name of their respective albums.
SQL Query:
SELECT Tracks.Name AS TrackName, Albums.Title AS AlbumName
FROM Tracks
JOIN Albums ON Tracks.AlbumId = Albums.AlbumId;
Example 2:

Description: Get the total sales amount (Total) for each customer, showing the customer's first name, last name, and the total amount spent.
SQL Query:
SELECT Customers.FirstName, Customers.LastName, SUM(Invoices.Total) AS TotalSpent
FROM Customers
JOIN Invoices ON Customers.CustomerId = Invoices.CustomerId
GROUP BY Customers.CustomerId, Customers.FirstName, Customers.LastName;
Example 3:

Description: List the names of employees who report to a manager with the first name "Andrew".
SQL Query:
SELECT E1.FirstName, E1.LastName
FROM Employees E1
JOIN Employees E2 ON E1.ReportsTo = E2.EmployeeId
WHERE E2.FirstName = 'Andrew';
Example 4:

Description: Find the titles of all albums by the artist "AC/DC".
SQL Query:
SELECT Albums.Title
FROM Albums
JOIN Artists ON Albums.ArtistId = Artists.ArtistId
WHERE Artists.Name = 'AC/DC';
Now, based on the given description, generate the SQL query also SQL Code should not have ''' in beginning or end and sql word in output
Description:
SQL Query:
"""
]

## streamlit app
st.set_page_config(page_title="I Can Retrive Any SQL Query from chinook DB")
st.header("Gemini App to Retrieve SQL Data")

questions=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")
if submit:
    response=get_gemini_response(questions=questions,prompt=prompt)
    print(response)
    data=read_sql(response,"chinook.db")
    st.subheader("The Response is")
    i=0
    for row in data:
        print(row)
        st.header(row)
        i=i+1
        if i>=6:
            break


# if submit:
#     while True:
#         response=get_gemini_response(questions,Prompt)
#         if response:
#             response=response.replace("'''","")

#             import sqlite3 as sql
#             conn=sql.connect("chinook.db")

#             try:
#                 response_df=pd.read_sql(response,conn)
#                 st.subheader("Result")
#                 st.write(response_df)
#                 break
#             except Exception as e:
#                 print("Error:",e)
#                 continue

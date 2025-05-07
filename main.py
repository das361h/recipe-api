# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List
import json

app = FastAPI()

# Allow requests from Android apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite connection
def get_db_connection():
    conn = sqlite3.connect("w2c.db")
    conn.row_factory = sqlite3.Row
    return conn

# Route to get recipes using only specified ingredients
@app.get("/recipes/search")
def search_recipes(ingredients: str = Query(...)):
    user_ingredients = set(i.strip().lower() for i in ingredients.split(",") if i.strip())
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recipedb"
    cursor.execute(query)
    all_recipes = cursor.fetchall()

    result = []

    for row in all_recipes:
        db_ingredients = set(i.strip().lower() for i in row["ringred"].split(",") if i.strip())

        if db_ingredients.issubset(user_ingredients):
            result.append({
                "rid": row["rid"],
                "rname": row["rname"],
                "ringred": row["ringred"],
                "rtype": row["rtype"],
                "rcuisine": row["rcuisine"],
                "roveralltime": row["roveralltime"],
                "rstep": row["rstep"],
                "imgurl": row["imgurl"]
            })

    conn.close()
    return result

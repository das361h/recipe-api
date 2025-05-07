from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List

app = FastAPI()

# CORS settings for Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "w2c.db"

@app.get("/recipes/by-ingredients/")
def get_recipes_by_ingredients(ingredients: List[str] = Query(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all recipes
    cursor.execute("SELECT * FROM recipedb")
    all_recipes = cursor.fetchall()

    result = []
    for row in all_recipes:
        rid, rname, ringred, rtype, rcuisine, roveralltime, rstep = row
        # Normalize ingredients
        recipe_ingredients = set(map(str.strip, ringred.lower().split(',')))
        input_ingredients = set(map(str.strip, map(str.lower, ingredients)))

        # Check if all recipe ingredients are within the user input
        if recipe_ingredients.issubset(input_ingredients):
            # Fetch image from imagedb
            cursor.execute("SELECT imgurl FROM imagedb WHERE imgid=?", (rid,))
            img_row = cursor.fetchone()
            imgurl = img_row[0] if img_row else ""

            result.append({
                "rid": rid,
                "rname": rname,
                "ringred": ringred,
                "rtype": rtype,
                "rcuisine": rcuisine,
                "roveralltime": roveralltime,
                "rstep": rstep,
                "imgurl": imgurl
            })

    conn.close()
    return result

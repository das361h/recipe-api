from fastapi import FastAPI
import sqlite3
from typing import List, Dict

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("w2c.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/recipes")
def get_all_recipes() -> List[Dict]:
    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM recipeTable").fetchall()
    conn.close()
    return [dict(row) for row in recipes]

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str) -> Dict:
    conn = get_db_connection()
    recipe = conn.execute("SELECT * FROM recipeTable WHERE id = ?", (recipe_id,)).fetchone()
    conn.close()
    if recipe:
        return dict(recipe)
    return {"error": "Recipe not found"}


@app.get("/recipes/search_exact")
def search_recipes_exact(ingredients: str):
    allowed_ingredients = set([i.strip().lower() for i in ingredients.split(",")])

    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM recipeTable").fetchall()
    conn.close()

    matching_recipes = []
    for row in recipes:
        recipe_ingredients = set(i.strip().lower() for i in row["ingredient"].split(","))
        if recipe_ingredients.issubset(allowed_ingredients):
            matching_recipes.append(dict(row))

    return matching_recipes

"""
Meal Planning LLM (via Hugging Face Inference API)
-------------------------------------------------
Generates meal plans using Hugging Face-hosted LLMs and MCP food data.
"""

import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2" 

client = InferenceClient(model=MODEL_ID, token=HF_API_KEY)

def generate_meal_plan_llm(target_calories, macros, wake_time, gym_time, food_data, meals_per_day=5, days=7):
    """
    Ask Hugging Face LLM to generate a meal plan using MCP food data.
    """

    prompt = f"""
    You are a professional nutrition planner. Create a {days}-day meal plan.

    - Target calories: {target_calories} kcal/day
    - Macros: {macros}
    - Meals per day: {meals_per_day}
    - Wake-up time: {wake_time}
    - Gym time: {gym_time}
    - Available foods with nutrition per 100g: {json.dumps(food_data, indent=2)}

    Output as JSON list with fields: Day, Time, Meal, Food, Quantity (g), Calories.
    Example:
    [
      {{"Day": "Day 1", "Time": "08:00", "Meal": "Breakfast", "Food": "Oats", "Quantity (g)": 50, "Calories": 190}}
    ]
    """

    response = client.text_generation(prompt, max_new_tokens=800, temperature=0.7)

    try:
        start = response.find("[")
        end = response.rfind("]") + 1
        return json.loads(response[start:end])
    except Exception as e:
        print("LLM parsing error:", e)
        return []

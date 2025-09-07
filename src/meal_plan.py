from mcp_clients.apify_client import get_food_info
from llm.meal_llm import generate_meal_plan_llm

def fetch_food_data(food_list, preferred_source="walmart"):
    """Fetch nutrition info for foods from Apify MCP (Costco or Walmart)."""
    results = {}
    for food in food_list:
        data = get_food_info(food, source=preferred_source)
        if data:
            results[food] = data
    return results

def build_meal_plan(target_calories, macros, wake_time, gym_time, food_list, preferred_source="walmart", days=7):
    """Integrate MCP + LLM to generate structured plan."""
    food_data = fetch_food_data(food_list, preferred_source=preferred_source)
    plan = generate_meal_plan_llm(
        target_calories, macros, wake_time, gym_time, food_data, days=days
    )
    return plan

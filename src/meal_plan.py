from mcp_clients import costco_client, walmart_client, wee_client
from llm.meal_llm import generate_meal_plan_llm

def fetch_food_data(food_list):
    """Fetch nutrition info for foods from MCP servers."""
    results = {}
    for food in food_list:
        for client in [costco_client, walmart_client, wee_client]:
            data = client.get_food_info(food)
            if data:
                results[food] = data
                break
    return results

def build_meal_plan(target_calories, macros, wake_time, gym_time, food_list, days=7):
    """Integrate MCP + LLM to generate structured plan."""
    food_data = fetch_food_data(food_list)
    plan = generate_meal_plan_llm(
        target_calories, macros, wake_time, gym_time, food_data, days=days
    )
    return plan

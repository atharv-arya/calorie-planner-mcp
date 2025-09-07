"""
Generic Apify MCP Client
------------------------
Handles querying Apify MCP servers (Costco, Walmart, etc.)
via the MCP remote gateway.
"""

import requests
import os

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
MCP_BASE_URL = "https://mcp.apify.com"

def query_apify(actor_id: str, params: dict):
    """
    Generic function to call an Apify actor via MCP gateway.
    
    Args:
        actor_id (str): The Apify actor (e.g., tri_angle/costco-fast-product-scraper).
        params (dict): Input params for the actor.
    
    Returns:
        list: Parsed dataset items from Apify.
    """
    url = f"{MCP_BASE_URL}/?actors={actor_id}"
    headers = {"Authorization": f"Bearer {APIFY_API_TOKEN}"}
    
    resp = requests.post(url, headers=headers, json=params)
    if resp.status_code != 200:
        print("Error:", resp.text)
        return []
    
    return resp.json().get("items", [])


def get_food_info(food_name: str, source: str = "walmart"):
    """
    Fetch product data (nutrition, price) for a food from Apify MCP.
    
    Args:
        food_name (str): Food to search for.
        source (str): 'walmart' or 'costco'.
    """
    actor_map = {
        "walmart": "epctex/walmart-scraper",
        "costco": "tri_angle/costco-fast-product-scraper"
    }
    
    actor_id = actor_map.get(source.lower())
    if not actor_id:
        raise ValueError("Invalid source. Choose 'walmart' or 'costco'")
    
    params = {
        "query": food_name,
        "maxItems": 5
    }
    
    items = query_apify(actor_id, params)
    if not items:
        return None
    
    item = items[0]
    return {
        "name": item.get("title") or item.get("name"),
        "price": item.get("price") or item.get("offerPrice") or item.get("listPrice"),
        "calories": item.get("calories", 0),
        "protein": item.get("protein", 0),
        "carbs": item.get("carbs", 0),
        "fat": item.get("fat", 0),
    }

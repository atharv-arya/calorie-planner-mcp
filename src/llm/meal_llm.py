import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def run_meal_chat(target_calories, macros):
    """
    Interactive chatbot for meal planning.
    Auto-uses TDEE + macros, asks user wake/gym times, fetches foods via MCP.
    """
    # Load environment
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Config file for Costco/Walmart MCP
    config_file_path = "mcp_config.json"

    # Init MCP + LLM
    mcp_client = MCPClient.from_config_file(config_file_path)
    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

    # Agent with memory enabled
    agent = MCPAgent(
        llm=llm,
        client=mcp_client,
        max_steps=20,
        memory_enabled=True,
    )

    print("\n------- Meal Planning Chatbot Started -------")
    print("I already know your target calories & macros.")
    print("I'll ask for wake-up time, gym time, and foods.")
    print("Type 'quit' to end the session.")
    print("Type 'clear' to reset memory.")
    print("------------------------------------------------")

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() == "quit":
                print("Chat session ending...")
                break
            if user_input.lower() == "clear":
                print("Conversation history cleared.")
                continue

            try:
                response = await agent.run(
                    f"""
                    Context:
                    - Target calories: {target_calories}
                    - Macros: {macros}
                    - You can query Costco/Walmart MCP servers for foods.
                    Task:
                    Continue this meal planning chat.
                    {user_input}
                    """
                )
                print("\nAssistant:", response)
            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if mcp_client and mcp_client.sessions:
            await mcp_client.close_all_sessions()

if __name__ == "__main__":
    # Example: pull from Streamlit session state later
    target_calories = 1800
    macros = {"Protein (g)": 135, "Carbs (g)": 180, "Fat (g)": 60}

    asyncio.run(run_meal_chat(target_calories, macros))

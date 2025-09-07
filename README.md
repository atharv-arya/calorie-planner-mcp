# Calorie Planner MCP 🥗💪

A Streamlit app that helps users:
1. Calculate maintenance and deficit calories.
2. Generate a 7-day meal plan with balanced macros.
3. Create a budget-optimized grocery list from Costco and Walmart.
4. Export both plans as styled PDFs.

## Features
- Input bodyweight, height, age, activity level.
- Macro-balanced meal planning with user foods.
- Grocery optimization under weekly budget.
- HuggingFace LLM integration.
- MCP servers for food data and prices.
- Streamlit web interface.
- Export to PDF.

## Tech Stack
- Python
- Streamlit
- HuggingFace Transformers
- WeasyPrint (PDF generation)
- MCP servers (Costco and Walmart)

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/calorie-planner-mcp.git
cd calorie-planner-mcp
pip install -r requirements.txt
streamlit run src/main.py

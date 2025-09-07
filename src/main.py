import streamlit as st

st.set_page_config(page_title="Calorie Planner", layout="wide")

st.title("🥗 Calorie Planner")
st.markdown("Welcome! This tool will help you calculate your calories, build meal plans, and optimize your grocery shopping.")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Calorie Calculator", "Meal Plan", "Grocery Plan"])

if page == "Home":
    st.write("👉 Start by selecting a page in the sidebar.")
elif page == "Calorie Calculator":
    st.write("🔢 Calorie calculator page")
elif page == "Meal Plan":
    st.write("📅 Meal plan page")
elif page == "Grocery Plan":
    st.write("🛒 Grocery plan page")

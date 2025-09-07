import streamlit as st

st.set_page_config(page_title="Calorie Planner", layout="wide")

st.title("🥗 Calorie Planner")
st.markdown("Welcome! This tool will help you calculate your calories, build meal plans, and optimize your grocery shopping.")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Calorie Calculator", "Meal Plan", "Grocery Plan"])

if page == "Home":
    st.write("👉 Start by selecting a page in the sidebar.")
elif page == "Calorie Calculator":
    st.header("🔢 Calorie calculator page")
    with st.form("calorie_form"):
        col1, col2 = st.columns(2)

        with col1:
            weight = st.number_input("Weight", min_value = 0.0, max_value=200.0, value=70.0, step=0.5)
            weight_unit = st.radio("Weight Unit", ["kg", "lbs"], horizontal=True)

            height = st.number_input("Height (cm)", min_value = 50.0, max_value=300.0, value=150.0, step=0.5)
            age = st.number_input("Age", min_value = 0, max_value=150, value=21, step=1)
            
        with col2:
            gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
            activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"])
            goal = st.radio("Goal", ["Maintain", "Deficit", "Surplus"], horizontal=True)
            deficit = st.slider("Calorie Adjustment (+/-)", 250, 1000, 500, step=50)

        submitted = st.form_submit_button("Calculate")   
    
    if submitted:
        # Convert lbs to kg if needed
        if weight_unit == "lbs":
            weight = weight * 0.453592

        from calorie_calc import calculate_tdee, calculate_target_calories, calculate_macros

        tdee = calculate_tdee(weight, height, age, gender, activity)
        target_calories = calculate_target_calories(tdee, goal, deficit)
        macros = calculate_macros(target_calories)

        st.subheader("Results")
        st.write(f"**Maintenance Calories (TDEE):** {tdee} kcal/day")
        st.write(f"**Target Calories:** {target_calories} kcal/day")
        st.table(macros) 


elif page == "Meal Plan":
    st.header("📅 Meal Plan Generator")

    with st.form("meal_plan_form"):
        wake_time = st.time_input("Wake-up Time")
        gym_time = st.time_input("Gym Time")
        food_list = st.text_area("Enter foods (comma separated)", "chicken, rice, oats, eggs, broccoli").split(",")
        generate_btn = st.form_submit_button("Generate Plan")

    if generate_btn:
        from calorie_calc import calculate_tdee, calculate_target_calories, calculate_macros
        from meal_plan import build_meal_plan

        # For now, let’s use static TDEE/macros from Phase 2 (later we’ll connect this directly)
        tdee = 2000
        target_calories = 1800
        macros = calculate_macros(target_calories)

        plan = build_meal_plan(
            target_calories, macros,
            wake_time.strftime("%H:%M"), gym_time.strftime("%H:%M"),
            [f.strip() for f in food_list]
        )

        if plan:
            st.subheader("Generated 7-Day Meal Plan")
            st.dataframe(plan)
        else:
            st.error("⚠️ Could not generate meal plan. Check MCP or LLM setup.")

elif page == "Grocery Plan":
    st.write("🛒 Grocery plan page")

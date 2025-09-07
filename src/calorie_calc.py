"""
Calorie Calculator 
---------------------
Uses Mifflin-St Jeor Equation for calorie needs.
"""

from typing import Dict

def calculate_tdee(weight: float, height: float, age: float, gender: str, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure (TDEE).
    
    Args:
        weight (float): Weight in kilograms.
        height (float): Height in centimeters.
        age (int): Age in years.
        gender (str): "male" or "female".
        activity_level (str): One of ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"].
    
    Returns:
        float: Estimated TDEE (maintenance calories).
    """

    # calculating BMR
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity multipliers
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)
    return round(bmr * multiplier, 2)

#####################
def calculate_macros(calories: float, protein_ratio: float = 0.3, carb_ratio: float = 0.4, fat_ratio: float = 0.3) -> Dict[str, float]:
    """
    Calculate daily macronutrient targets.
    
    Args:
        calories (float): Daily calorie target.
        protein_ratio (float): Fraction of calories from protein.
        carb_ratio (float): Fraction of calories from carbs.
        fat_ratio (float): Fraction of calories from fat.
    
    Returns:
        dict: Protein, Carbs, Fat in grams.
    """

    protein_cals = calories * protein_ratio
    carbs_cals = calories * carb_ratio
    fat_cals = calories * fat_ratio

    return{
        "Protein (g)" : round(protein_cals / 4, 1),
        "Carbs (g)" : round(carbs_cals / 4, 1),
        "Fats (g)" : round(fat_cals / 4, 1),
    }

#####################
def calculate_target_calories(tdee: float, goal: str, deficit: int = 500) -> float:
    """
    Adjust calories for deficit or surplus.
    
    Args:
        tdee (float): Maintenance calories.
        goal (str): "Maintain", "Deficit", or "Surplus".
        deficit (int): Adjustment value (default 500 kcal).
    
    Returns:
        float: Target calories based on goal.
    """
    if goal == "Deficit":
        return max(1200, tdee - deficit)  # 1200 cals is the safe level threshold for minimum amount of calories one should consume
    elif goal == "Surplus":
        return tdee + deficit
    return tdee

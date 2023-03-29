"""
Functions for the POC on Meal Recommendation System
This program is capable of recommending three meals based on
the amount of the daily intake on the three major nutrients.
"""

from random import randint
from typing import List, Tuple
from pandas import DataFrame

import pandas as pd
import math


DATA_SET = "./dataset/nutrients.csv"

MEAL_NUT_RATIO = {"breakfast": 3, "lunch": 4, "dinner": 3}
BF_NUT_RATIO = {"main": 7, "drink": 1, "dairy": 2}
DIN_NUT_RATIO = {"main": 8, "salad": 1, "fruit": 1}
LU_NUT_RATIO = {"main": 8, "salad": 2}
MEAL_WEIGHT = {
    "breakfast": 300,
    "lunch": 400,
    "dinner": 400,
}  # this number might need to be changed
PROTEIN = "Pro_100G"
CARB = "CHO_100G"
FAT = "Fat_100G"
CALORIE = "Cal_100G"
FOOD_GROUP = "Food Group"
MAIN = "Main"
DAIRY = "Dairy"
FRUIT = "Fruit"
DRINK = "Drink"
SALAD = "Salad"
VEGETARIAN_MAIN_GROUP = [
    "Vegetables A-E",
    "Vegetables F-P",
    "Vegetables R-Z",
]

VEGETARIAN_GROUP = [
    "Dairy products",
    "Vegetables A-E",
    "Vegetables F-P",
    "Vegetables R-Z",
    "Fruits A-F",
    "Fruits G-P",
    "Fruits R-Z",
    "Desserts, sweets",
    "Jams, Jellies",
    "Seeds and Nuts",
    "Drinks,Alcohol, Beverages",
]

MAIN_DISH_GROUP = [
    "Fats, Oils, Shortenings",
    "Meat, Poultry",
    "Fish, Seafood",
    "Breads, cereals, fastfood,grains",
    "Vegetables A-E",
    "Vegetables F-P",
    "Vegetables R-Z",
]
SALAD_GROUP = ["Vegetables A-E", "Vegetables F-P", "Vegetables R-Z"]
FRUIT_GROUP = ["Fruits G-P", "Fruits R-Z", "Fruits A-F"]
DRINK_GROUP = ["Soups", "Drinks,Alcohol, Beverages"]
DAIRY_GROUP = ["Dairy products"]


# def calculate_nutrient_percent(protein_g:int, carb_g:int, fat_g:int) -> Tuple[float]:
#   """
#   Calculate the percentage of the three major nutrient in a meal
#   protein_g: The amount of protein in grams
#   cab_g: The amount of carbonhydrate in grams
#   fat_g: The amount of fat in grams
#   returns: The percentage of protein, carbonhydrate, and fat in the
#   three major nutrients
#   """
#   total_g = protein_g + cab_g + fat_g
#   return (protein_g/total_g*100, cab_g/total_g*100, fat_g/total_g*100)


# def calculate_nutrient_each_meal(
#     meal_ratios: Tuple[int],
#     protein_g: float,
#     carb_g: float,
#     fat_g: float,
#     cal_cal: float,
# ) -> Tuple[float]:
#     """
#     Calculate the amount of nutrient intake of each meal based on the
#     meal_ratios.
#     meal_ratios: The ratio numbers on each meal for dividing the nutrient amount
#     protein_g: The amount of protein in grams
#     cab_g: The amount of carbonhydrate in grams
#     fat_g: The amount of fat in grams
#     returns: The amount of three major nutrients for each meal
#     ex. meal_ratios = (3,4,3) represents breakfast distributed 3 unit of
#     nutrients, lunch distributed 4 unit of nutrients, dinner distributed
#     3 unit of nutrients, while there will be 10 units in total. Then, the
#     function will calculate the three major nutrients for each meal based
#     on this ratio. It will return
#     [(meal1_protein,meal1_carb,meal1_fat),(meal2_protein,meal2_carb,meal2_fat)]
#     """
#     meal_nutrient_list = []
#     total_ratio = sum(meal_ratios)
#     for meal_ratio in meal_ratios:
#         nutrient_ratio = meal_ratio / total_ratio
#         meal_cal = cal_cal * nutrient_ratio
#         meal_protein = protein_g * nutrient_ratio
#         meal_carb = carb_g * nutrient_ratio
#         meal_fat = fat_g * nutrient_ratio
#         meal_nutrient_list.append((meal_protein, meal_carb, meal_fat, meal_cal))
#     return meal_nutrient_list
#
#
# def import_food_menu():  # function purely for testing dataframe purpose
#     allergens = ["milk", "bacon"]
#     dishes = pd.read_csv(DATA_SET, encoding="ISO-8859-1")
#     dishes = dishes[~dishes["Food"].isin(allergens)]
#     print(dishes)


def dish_generation(
    dishes: DataFrame, meal_max_weight: float, dish_ratio: float, calorie: float, is_drink: bool=False,
) -> dict:
    dish = dishes.iloc[randint(0, len(dishes) - 1)]
    if is_drink:
        dish_weight = calorie * (dish_ratio / 10) / (dish[CALORIE] / 100)
        if dish_weight > meal_max_weight * (dish_ratio / 10):
            dish_weight = meal_max_weight * (dish_ratio / 10)
    else:
        if dish[CALORIE] == 0:
            dish_weight = math.inf
        else:
            dish_weight = calorie * (dish_ratio / 10) / (dish[CALORIE] / 100)

        # if dish_weight > meal_max_weight * (dish_ratio / 10):
        #     dish_weight = meal_max_weight * (dish_ratio / 10)

        count = 0
        while dish_weight > meal_max_weight * (dish_ratio / 10):
            dish = dishes.iloc[randint(0, len(dishes) - 1)]
            if dish[CALORIE] == 0:
                dish_weight = math.inf
            else:
                dish_weight = calorie * (dish_ratio / 10) / (dish[CALORIE] / 100)

            if count > 100:
                dish_weight = meal_max_weight * (dish_ratio / 10)
                break
            count += 1


    dish_cal = round(dish_weight * dish[CALORIE] / 100, 2)
    dish_protein = round(dish_weight * dish[PROTEIN] / 100, 2)
    dish_carb = round(dish_weight * dish[CARB] / 100, 2)
    dish_fat = round(dish_weight * dish[FAT] / 100, 2)
    dish_weight = round(dish_weight, 2)

    return {"dish":{"name":dish.name, "amount":dish_weight}, "nutrient":{"Kcal":dish_cal, "protein":dish_protein, "fat":dish_fat, "carb":dish_carb}}
    #
    # (dish.name, dish_weight, dish_cal, dish_protein, dish_fat, dish_carb)

def sum_nutrient(
    dishes: List[dict]
) -> dict:  # update meal nutrient
    total_nutrient = {"Kcal":0, "protein":0, "fat":0, "carb":0}

    for dish in dishes:
        total_nutrient["Kcal"] += dish["nutrient"]["Kcal"]  # update calories
        total_nutrient["protein"] += dish["nutrient"]["protein"]  # update protein
        total_nutrient["fat"] += dish["nutrient"]["fat"]  # update fat
        total_nutrient["carb"] += dish["nutrient"]["carb"]  # update carb

    total_nutrient["Kcal"] = round(total_nutrient["Kcal"], 2)
    total_nutrient["protein"] = round(total_nutrient["protein"], 2)
    total_nutrient["fat"] = round(total_nutrient["fat"], 2)
    total_nutrient["carb"] = round(total_nutrient["carb"], 2)
    return total_nutrient


def remove_allergy(dishes: DataFrame, allergens: List[str]) -> DataFrame:
    Allergy = []
    for index, dish in dishes.iterrows():
        if any(allergen.lower() in index.lower() for allergen in allergens):
            Allergy.append(index)
    for i in Allergy:
        try:
            dishes = dishes.drop(i)
        except:
            pass
    return dishes


# def show_categories() -> List[str]:
#     dishes = pd.read_csv(DATA_SET, index_col=0, encoding="ISO-8859-1")
#
#     dish_category = dishes["Category"].unique()
#     return dish_category
#
#
# def concat_categories(categories: List[str]):
#     dishes = pd.read_csv(DATA_SET, index_col=0, encoding="ISO-8859-1")
#
#     frames = []
#     for catrgory in categories:
#         frames.append(dishes[dishes["Category"] == catrgory])
#
#     output = pd.concat(frames)
#     return output


def recom_bf(
    vegetarian: bool,
    allergens: List[str],
    real_calorie: float,
    real_protein: float,
    real_carbon: float,
    real_fat: float,
) -> dict:
    recom_bf = []
    bf_calorie = real_calorie * MEAL_NUT_RATIO["breakfast"] / 10
    bf_protein = real_protein * MEAL_NUT_RATIO["breakfast"] / 10
    bf_carbon = real_carbon * MEAL_NUT_RATIO["breakfast"] / 10
    bf_fat = real_fat * MEAL_NUT_RATIO["breakfast"] / 10

    dishes = pd.read_csv(DATA_SET, index_col=0, encoding="ISO-8859-1")
    if vegetarian:
        main_dish = dishes[dishes["Category"].isin(VEGETARIAN_MAIN_GROUP)]
    else:
        main_dish = dishes[dishes["Category"].isin(MAIN_DISH_GROUP)]
    drink_dish = dishes[dishes["Category"].isin(DRINK_GROUP)]
    dairy_dish = dishes[dishes["Category"].isin(DAIRY_GROUP)]
    main_dish = remove_allergy(main_dish, allergens)
    drink_dish = remove_allergy(drink_dish, allergens)
    dairy_dish = remove_allergy(dairy_dish, allergens)

    dish = dish_generation(
        main_dish, MEAL_WEIGHT["breakfast"], BF_NUT_RATIO["main"], bf_calorie
    )

    recom_bf.append(dish)
    dish = dish_generation(
        drink_dish, MEAL_WEIGHT["breakfast"], BF_NUT_RATIO["drink"], bf_calorie, is_drink=True
    )
    recom_bf.append(dish)

    dish = dish_generation(
        dairy_dish, MEAL_WEIGHT["breakfast"], BF_NUT_RATIO["dairy"], bf_calorie
    )
    recom_bf.append(dish)

    nutrient = sum_nutrient(recom_bf)
    return {"dishes":recom_bf,"nutrient":nutrient}


def recom_lu(
    vegetarian: bool,
    allergens: List[str],
    real_calorie: float,
    real_protein: float,
    real_carbon: float,
    real_fat: float,
) -> dict:
    recom_lu = []

    lu_calorie = real_calorie * MEAL_NUT_RATIO["lunch"] / 10
    lu_protein = real_protein * MEAL_NUT_RATIO["lunch"] / 10
    lu_carbon = real_carbon * MEAL_NUT_RATIO["lunch"] / 10
    lu_fat = real_fat * MEAL_NUT_RATIO["lunch"] / 10


    dishes = pd.read_csv(DATA_SET, index_col=0, encoding="ISO-8859-1")

    if vegetarian:
        main_dish = dishes[dishes["Category"].isin(VEGETARIAN_MAIN_GROUP)]
    else:
        main_dish = dishes[dishes["Category"].isin(MAIN_DISH_GROUP)]
    salad_dish = dishes[dishes["Category"].isin(SALAD_GROUP)]

    main_dish = remove_allergy(main_dish, allergens)
    salad_dish = remove_allergy(salad_dish, allergens)

    dish = dish_generation(
        main_dish, MEAL_WEIGHT["lunch"], LU_NUT_RATIO["main"], lu_calorie
    )
    recom_lu.append(dish)

    dish = dish_generation(
        salad_dish, MEAL_WEIGHT["lunch"], LU_NUT_RATIO["salad"], lu_calorie
    )
    recom_lu.append(dish)

    nutrient = sum_nutrient(recom_lu)
    return {"dishes": recom_lu, "nutrient": nutrient}

def recom_din(
    vegetarian: bool,
    allergens: List[str],
    real_calorie: float,
    real_protein: float,
    real_carbon: float,
    real_fat: float,
) -> dict:
    recom_din = []

    din_calorie = real_calorie * MEAL_NUT_RATIO["dinner"] / 10
    din_protein = real_protein * MEAL_NUT_RATIO["dinner"] / 10
    din_carbon = real_carbon * MEAL_NUT_RATIO["dinner"] / 10
    din_fat = real_fat * MEAL_NUT_RATIO["dinner"] / 10

    dishes = pd.read_csv(DATA_SET, index_col=0, encoding="ISO-8859-1")

    if vegetarian:
        main_dish = dishes[dishes["Category"].isin(VEGETARIAN_MAIN_GROUP)]
    else:
        main_dish = dishes[dishes["Category"].isin(MAIN_DISH_GROUP)]
    salad_dish = dishes[dishes["Category"].isin(SALAD_GROUP)]
    fruit_dish = dishes[dishes["Category"].isin(FRUIT_GROUP)]

    main_dish = remove_allergy(main_dish, allergens)
    salad_dish = remove_allergy(salad_dish, allergens)
    fruit_dish = remove_allergy(fruit_dish, allergens)

    dish = dish_generation(
        main_dish, MEAL_WEIGHT["dinner"], DIN_NUT_RATIO["main"], din_calorie
    )
    recom_din.append(dish)

    dish = dish_generation(
        salad_dish, MEAL_WEIGHT["dinner"], DIN_NUT_RATIO["salad"], din_calorie
    )
    recom_din.append(dish)

    dish = dish_generation(
        fruit_dish, MEAL_WEIGHT["dinner"], DIN_NUT_RATIO["fruit"], din_calorie
    )
    recom_din.append(dish)

    nutrient = sum_nutrient(recom_din)
    return {"dishes": recom_din, "nutrient": nutrient}


def make_recommendation(calories:float, vegetarian:bool=False, allergens:List[str]=[], protein_g:float=0, carb_g:float=0, fat_g:float=0):

    """
    Make meal recommendation.
    meal_ratios: The ratio numbers on each meal for dividing the nutrient amount
    protein_g: The amount of protein in grams
    cab_g: The amount of carbon hydrate in grams
    fat_g: The amount of fat in grams
    returns: It will return the recommended dishes and the amount to eat for three meals
    """
    menus_for_today = {}
    menus_for_today["breakfast"] = recom_bf(vegetarian, allergens, calories, protein_g, carb_g, fat_g)
    menus_for_today["lunch"] = recom_lu(vegetarian, allergens, calories, protein_g, carb_g, fat_g)
    menus_for_today["dinner"] = recom_din(vegetarian, allergens, calories, protein_g, carb_g, fat_g)

    # print(menus_for_today)
    # print("\n\n")
    total_nutrient = {"Kcal": 0, "protein": 0, "fat": 0, "carb": 0}
    for menu_for_each_meal in menus_for_today.values():
        total_nutrient["Kcal"] += menu_for_each_meal["nutrient"]["Kcal"] # update calories
        total_nutrient["protein"] += menu_for_each_meal["nutrient"]["protein"]  # update protein
        total_nutrient["fat"] += menu_for_each_meal["nutrient"]["fat"]  # update fat
        total_nutrient["carb"] += menu_for_each_meal["nutrient"]["carb"]  # update carb


    total_nutrient["Kcal"] = round(total_nutrient["Kcal"], 2)
    total_nutrient["protein"] = round(total_nutrient["protein"], 2)
    total_nutrient["fat"] = round(total_nutrient["fat"], 2)
    total_nutrient["carb"] = round(total_nutrient["carb"], 2)

    return {"menus": menus_for_today, "total_nutrient": total_nutrient}
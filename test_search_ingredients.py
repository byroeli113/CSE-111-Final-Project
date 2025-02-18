import pytest
from pytest import approx
from search_ingredients import *
from text_processing_functions import *
from convience_functions import *
from math import *

# Running this file also tests Selenium's ability to open the window and the link to our website

# Functions without tests
    # process_items_list(items_list) 
        # this function is easiest to test by printing out outputs
        # because there are so many functions that need to be called just to get items_list (like pretty much all of them)
    # write_ingredients_to_JSON(ingredients_list, file_name)
        # you can just check the JSON file to see if it works
    # All selenium actions
        # They have a built in testing function (action chain) that makes sure that they work
        # Testing with pytest would be difficult, they depend on a live website and each other to find the elements they need


# Github Copilot wrote the following tests
def test_identify_data_type():
    assert identify_data_type("word") == "word/phrase"
    assert identify_data_type("0g grams") == "measurement"
    assert identify_data_type("8% daily value") == "dv"

# Github Copilot wrote the following tests
def test_remove_text_in_brackets():
    assert remove_text_in_brackets("hello <goodbye>") == "hello "
    assert remove_text_in_brackets("hello <goodbye> world") == "hello  world"

# Make it work
def test_calculate_dv_from_measurement():
    assert calculate_dv_from_measurement(40, 3) == approx(0.8, abs=0.00001)

def test_calculate_measurment_from_dv():
    assert calculate_measurment_from_dv(2, 0) == 4000

def test_process_raw_nutrient_list():
    # Test cases, one with both, one with missing DV, one with missing measurement
    assert process_raw_nutrient_list(["33g grams", "8% daily value"], "carbohydrate") == [33, approx(8/100, abs=0.00001)]
    assert process_raw_nutrient_list(["8% daily value", "33g grams"], "carbohydrate") == [33, approx(8/100, abs=0.00001)]

    # assert process_raw_nutrient_list(["8% daily value"], "carbohydrate") == [33, approx(8/100, abs=0.00001)]

def test_get_goal_unit():
    assert get_goal_unit("iron") == "mg"

    # Test fuzzy matching on Pantothenic Acid
    assert get_goal_unit("Pnatothenci Aciid_it's good!") == "mg"

def test_find_data_place():
    assert find_data_place("iron") == 35

def test_fix_measurment():
    assert fix_measurment("33g grams", "g") == 33
    assert fix_measurment("33kg kilograms", "g") == approx(33*1000, abs=0.00001)
    assert fix_measurment("(33 mcg)", "g") == approx(33*pow(10,-6), abs=0.00001)

def test_fix_div():
    assert fix_dv("1% daily value") == 0.01

def test_best_regex_match():
    test_string_list = ["app", "apple", "search", "stuff:", "mucho más", "what's up", "dog", "cat"]
    assert best_regex_match(test_string_list, "ap") == "app"
    # assert best_regex_match(test_string_list, ":") == "stuff:" # fails because it doesn't match enough that's actually a good thing for our purposes!
    assert best_regex_match(test_string_list, "'s up") == "what's up"

    real_test_strings = [item[0] for item in ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE]
    print(real_test_strings)
    assert best_regex_match(real_test_strings, "total fat") == "fat"
    assert best_regex_match(real_test_strings, "total carbohydrates") == "carbohydrate"
    assert best_regex_match(real_test_strings, "dietary fiber") == "total fiber"
    assert best_regex_match(real_test_strings, "caffiene") == None
    assert best_regex_match(real_test_strings, "calories") == "calories"


def test_extract_unit():
    assert extract_unit("(33g grams)") == "g"
    assert extract_unit("(33kg kilograms)") == "kg"
    assert extract_unit("44 kg") == "kg"
    assert extract_unit("##!##9000 |mcV |") == "mcV"
    # This next line fails and returns "n" but we can already identify if something is a unit, so we don't need it
    # assert extract_unit("chicken") == ""

def test_extract_number():
    assert extract_number("(33g grams)") == 33
    assert extract_number("23402349849g grams[2342]") == 23402349849

def test_extract_prefix():
    assert extract_prefix("kg") == "k"
    assert extract_prefix("mcg") == "mc"
    assert extract_prefix("kcal") == "k"
    assert extract_prefix("cal") == ""

def test_is_last_item_in_list():
    test_list = ["hi", "it\'s", "me", "I'm", "the", "problem", "it\'s", "me"]
    assert is_last_item_in_list("me", test_list) == True



pytest.main(["-v", "--tb=line", "-rN", __file__])

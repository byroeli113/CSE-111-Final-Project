import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # For running the program headless

# PATH = r"chromedriver.exe"

PATH_TO_INGREDIENTS_CSV = ""

# Figuer out how to run headless sucessfully

CSERVICE = webdriver.ChromeService()
DRIVER = webdriver.Chrome(service=CSERVICE)

DRIVER.get("https://www.nutritionix.com/database")

LOAD_TIME = 2

## FUNCTIONS FOR nutritionix PROCESSING ##

def get_common_US_foods_link():
    """Go to common foods then get the link for US - English Food Directory. Go to that link"""

    try:
        element = DRIVER.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[3]/div[2]/p[5]/a")
        link = element.get_attribute("href")
        DRIVER.get(link)
        passed = True
    except:
        print("Couldn't find the element")
        link = None
        passed = False
    time.sleep(LOAD_TIME)
    return passed

def use_search_bar(user_search):
    """Find the search bar and input the keys given by the parameter user_search (str)"""
    time.sleep(1)
    try:
        element = DRIVER.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div/input")
        element.send_keys(user_search)
        element.send_keys(Keys.RETURN)
        passed = True
    except:
        print("Couldn't find the search bar")
        passed = False
    time.sleep(LOAD_TIME)
    return passed

def create_list_of_items():
    """Extract all the hrefs that show up with the search"""
    items_list = []
    try:
        elements = DRIVER.find_elements(By.CLASS_NAME, "item-row")
        for element in elements:
            items_list.append(element.get_attribute("href"))
    except:
        print("Couldn't find the item")
    
    time.sleep(LOAD_TIME)
    return items_list

##########################################

## FUNCTIONS FOR walmart PROCESSING ##

##########################################

## GENERAL FUNCTIONS ##
def chain_of_events(*args): # If only this was C++. Then I would be able to mandate that I pass functions that return booleans as parameters. Silly python
    """
    Ensures that functions are called and return true before running the next function
    Useful for functions that need to happen in a specific order.
    
    ARGS, should all be functions that return a boolean value
    Can also be fuction partials, that already have a few parameters attached
    """
    for arg in args:
        passed = arg()
        if not passed:
            print(f"{arg.__name__} failed and the rest of the chain wasn't exectuted :(")
            break

def try_and_wait(func):
    """
    Trys to run a function number_of_tries times. 
    Each time the function fails it waits for LOAD_TIME seconds.
    This is useful for selenium actions that may not work until the webpage loads."""
    number_of_tries = 25
    for i in range(number_of_tries):
        try:
            whatever_is_to_be_returned = func()
            if whatever_is_to_be_returned != None:
                return whatever_is_to_be_returned
        except:
            print(f"{func.__name__} failed, we're trying again.")
            time.sleep(LOAD_TIME)
    print(f"We tried {number_of_tries} times and failed every single time")

##########################################
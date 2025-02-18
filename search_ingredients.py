''''
NOTES:
    - Selenium is not a built in library but it is fairly common (and supported by pylance)
        - Selenium allows you to interact with a website based on it's HTML source code
            - You can see the code in Chrome using Inspect
                - This is how I found all the XPATHs that I use to find elements (it's proven to be the most surefire method)
        - pip install selenium
    - Webdrivers must be up to date for Selenium to work
        - They can be downloaded at: 
    - I'm using openpyxl to modify excel workbooks 
        - csv files were too difficult for this complex of a task
        - .xlsx files are more readable (Google Sheets or Excel)
'''

'''
CREDITS:
    - Thanks to https://www.nutritionix.com for the food data
    - Thanks to gemini and stackoverflow for contributing some code
    - Thanks to Github Copilot for helping me to make lists out of nonsense
'''

"""
!TO-DO!
Further Expansion:
    [] Run selenium headless if your not in debug mode
    [] Use Walmart.com to get prices
    [] Create nutrition score and then nutrition to price ratio
    [] Plan ingredients that optimize nutrition to price ratio
    [] Write ingredients to a .xlsx so they can be viewed
    [] Assemble dishes out of ingredients
    [] Assemble meals out of dishes
    [] Terminal App (UI)
        [] Allow users to make searches for ingredients
        [] Allow user to enter in budget to assemble the best possible meals (with nutrition score)
        [] Allow user to edit meal plans through the spreadsheet (recalculate nutrition score)
        [] Allow the user to make a weekly/monthly plan based and save that plan
        [] Allow user to search nutrition facts for food they already have, and factor that into the rest of the program
More Optional Expansions:
    [] Use: https://fdc.nal.usda.gov/food-search?type=Survey%20(FNDDS)&marketCountries=United%20States,Canada,New%20Zealand to fill in
    gaps in the data (average with data you currently have if point already exists)
    [] Have user enter in stuff that they already have, and have this help with planning
    [] Get recipies from AllRecipies and evaluate cook time in your week (and create dishes)
    [] Curve fit model that guesses information about ingredient based on limited data (enter in hypothetical marker into data set so you know this data isn't confirmed)

Ideas:
    [] Extract nutrition label from any webpage
        - Bring in entire webpage HTML and automatically detect (using text processing) nutrition labels and extract whatever data we can
        - Anything that provides nutrition information is extracted
    [] Image processing to extract nutrition information from pictures
    [] Package as a .exe using pyinstaller
    [] Make a GUI instead of displaying information in spreadsheets
"""

"""
Thoughts:
    [X] JSON files will probably be much faster and easier to write to than .csv files, you could use JSON as your database
"""



# Selenium stuff
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # For running the program headless, didn't work

import openpyxl # For spreadsheets, didn't end up using it in this version
import json

from functools import partial 
import time

import re # for ReGex (text processing with fancy patterns)

# Import my modules
from acceptable_standards import *
from text_processing_functions import *
from convience_functions import *
from selenium_actions import *


def process_items_list(items_list):
    """
    Extracts nutrition information from each of the pages in 
    items_list and returns a list of dictionaries with
    correctly formatted and acceptable data.

    Parameters:
        items_list (list): A list of partial links to nutrition information pages.

    Returns:
        list_of_dict_of_items (list): A list of dictionaries containing formated nutrition information
    """

    # Returns a list of dictionaries (one for each item) we can write to the excel file
    list_of_dict_of_items = []

    # dictonary format
    # chicken : {Serving Size: 300, Calories: 229, ...}

    # For each item in the items list (which is a list of links)
    for i in range(len(items_list)):

        # Get the item (pull up the webpage and extract the data)
        def get_item():
            # Open each item using the partial links in items list
            DRIVER.get("https://www.nutritionix.com/food" + items_list[i])
            time.sleep(LOAD_TIME) # Give it a second to load

            # Find the div that contains the nutrition label
            find_label = DRIVER.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/div/div/div/div")
        
            # Extract all the HTML that's contained in that div
            unprocessed_label = find_label.get_attribute("innerHTML")
            return unprocessed_label

        # If the webpage won't load, wait a second and try again
        unprocessed_label = try_and_wait(get_item)
        
        # Remove everything inside of <> HTML tags
        unprocessed_label = remove_text_in_brackets(unprocessed_label)
        # Remove any combination of \n and \t and replace it with a ,
        unprocessed_label = re.sub(r"[\n\t]+", ",", unprocessed_label) # CREDIT: Gemini 2.0 Flash
        # Remove the leading comma and the comma at the end
        unprocessed_label = unprocessed_label.strip(",")

        # Prints the raw string for debugging to see if you've remove all the nonsense
        # print(repr(unprocessed_label)[1:-1]) # slicing 1 and -1 to remove the qoutes

        # Break into a list based on the commas
        label_list = unprocessed_label.split(",")

        # Lower case the entire list
        # Uses a lambda function to map each element to the lower version of itself, then stores the remapped array back in label_list
        label_list = list(map(lambda x: x.lower(), label_list)) # CRED: https://stackoverflow.com/questions/1801668/convert-a-list-with-strings-all-to-lowercase-or-uppercase

        # At this point we have a list like the one below
        '''Typical label_list:
        ['nutrition facts', 'serving size:', 'oz', 
        '(85g grams)', 'chicken', 'amount per serving', 
        'calories', '187', '% daily value*', 
        'total fat', '11g grams', '14% daily value', 
        'saturated fat', '3.1g grams', '16% daily value', 
        'polyunsaturated fat', '2.4g grams', 
        'monounsaturated fat', '4.4g grams', 'cholesterol', 
        '80mg milligrams', '27% daily value', 'sodium', '60mg milligrams', 
        '3% daily value', 'total carbohydrates', '0g grams', '0% daily value', 
        'dietary fiber', '0g grams', '0% daily value', 'protein', '20g grams', 
        'calcium', '11mg milligrams', '1% daily value', 'iron', '1.4mg milligrams', 
        '8% daily value', 'potassium', '173.4mg milligrams', '4% daily value', 
        'the % daily value (dv) tells you how much a nutrient in a serving of food contributes to a daily diet. 2000 calories a day is used for general nutrition advice.', 
        'data not available']'''

        # pop out values we don't like
        label_list.pop(label_list.index("data not available"))
        label_list.pop(label_list.index("nutrition facts"))
        label_list.pop(label_list.index("the % daily value (dv) tells you how much a nutrient in a serving of food contributes to a daily diet. 2000 calories a day is used for general nutrition advice."))
        label_list.pop(label_list.index("% daily value*"))
        label_list.pop(label_list.index("amount per serving"))
       
        print(label_list)

        # Convert serving size into our standard units

        # We go from serving size until we hit calories
        # Then we go from calories until we hit another word/phrase
        # If % daily recommended value is missing, add it
        # key_list = []
        # value_list = []
        everything_in_it_serving_size_list = []

        # This loop get's us the serving size information 
        # Because it doesn't follow the same pattern as the others

        # A lot of the data goes something like this 
        # 'serving size:'
        # 'cutlet'
        # '(128g grams)
        # 'oz'
        # This little if statement just gets rid of that useless information that I can't store
        # and prevents it from messing up the loop following it
        label_list_copy = label_list.copy()
        for c in range(len(label_list_copy)):
            if label_list_copy[c] == "serving size:":
                if identify_data_type(label_list_copy[c+1]) == "word/phrase":
                    label_list.pop(c+1)
                    if identify_data_type(label_list_copy[c+2]) == "word/phrase":
                        label_list.pop(c+2)


        for c in range(len(label_list)):
        # Find serving size
            if label_list[c] == "serving size:":
                # Append everything after serving size (until you hit a new word/phrase)
                # Starts at the index after "serving size:" and goes until we hit a word/phrase
                for n in range(c+1, len(label_list)):
                    if identify_data_type(label_list[n]) == "word/phrase":
                        title = label_list[n] # Title is something like 'rotisserie chicken'
                        title_index = n
                        break
                    everything_in_it_serving_size_list.append(label_list[n]) # appends all that information for processing
    
        for item in everything_in_it_serving_size_list:
            if identify_data_type(item) == "measurement":
                serving_size_official = fix_measurment(item, "g")
                break
        
        
        print(title)

        # Start at one element after the title (should be calories in our example)
        b = title_index+1
        item_data_dict = {ACCEPTABLE_INGREDIENTS_DATA_W_UNITS[0][0]: serving_size_official}
        big_dict = {title: item_data_dict}
        while b < len(label_list): # Make sure that we are within our list
            if identify_data_type(label_list[b]) == "word/phrase": # If we find a word/phrase (like "calories")
                nutrient_name = label_list[b] # store the name of the nutrient
                raw_list = []
                index_we_left_on = b 
                for n in range(index_we_left_on+1, len(label_list)): # Go one forward from the nutrient_name and iterate through the rest of the list
                    if identify_data_type(label_list[n]) == "word/phrase": # until we hit another word/phrase
                        b = n # move the iterator forward (to this new nutrient label)
                        break # break out of this smaller loop
                    else: # if it's not a word/phrase it must be a measurement or DV
                        raw_list.append(label_list[n]) # so we put it in a list
                        if is_last_item_in_list(label_list[n], label_list): # if we are on the last item in our entire list
                            b = n+1 # Make sure that we go over the index to break out of the while loop
                            break # break out of this smaller loop

            try:
                data_place = find_data_place(nutrient_name)
                processed_list = process_raw_nutrient_list(raw_list, nutrient_name)
                print(data_place)
                print(processed_list)
                item_data_dict[ACCEPTABLE_INGREDIENTS_DATA_W_UNITS[data_place][0]] = processed_list
            except:
                print(f"Couldn\'t find a place for the data {nutrient_name}")

            if data_place != None:
                pass

        #     item_data_dict[nutrient_name] = process_raw_nutrient_list(raw_list, nutrient_name)
        list_of_dict_of_items.append(big_dict)

    print(list_of_dict_of_items)
    return list_of_dict_of_items

# CRED: Gemini Flash 2.0    
def write_ingredients_to_json(list_of_dict_items, filename):
    """
    CREDITS: Gemini Flash 2.0

    Dumps a list of dictionaries to a JSON file, skipping dictionaries
    with duplicate top-level keys, including those already present in the file.

    Parameters:
        list_of_dicts: A list of dictionaries.
        filename: The name of the JSON file to write to.
    
    Returns:
        None
    """

    existing_data = []
    seen_keys = set()

    # Load existing data from the file if it exists
    with open(filename, 'r') as f:
        try:  # Handle cases where the file might be empty or corrupted
            existing_data = json.load(f)
            for d in existing_data:  # Add pre-existing keys to the set
                top_level_key = list(d.keys())[0] if d else None
                if top_level_key: # Only add if the key is not None
                    seen_keys.add(top_level_key)
        except json.JSONDecodeError:
            print(f"Warning: File '{filename}' is not valid JSON. Starting with empty data.")


    unique_dicts = existing_data[:] # Start with existing data, then add new unique ones

    for d in list_of_dict_items:
        top_level_key = list(d.keys())[0] if d else None
        if top_level_key not in seen_keys:
            unique_dicts.append(d)
            seen_keys.add(top_level_key)

    with open(filename, 'w') as f:
        json.dump(unique_dicts, f, indent=4)


def main():
    # The use of partial below allow me to pass parameters into a function without calling it
    # You can use it to fill out part of the parameters, or all of the them
    chain_of_events(get_common_US_foods_link, partial(use_search_bar, "beef")) 
    # First we get the link to the common_foods page
    # Then we go to the link's page
    # Then we find the search bar and input the keys
    
    # Get a list of all the items that pop up when you make the search (this is a list of partial links)
    items_list = create_list_of_items()

    # Use list of partial links to open each food item's page and extract all the nutrition lables into a list of dictionaries
    data = process_items_list(items_list)

    # Let Selenium quit and close out the window we're using to scrape
    DRIVER.quit()

    # Dump the list of dictionaries into a .json file (making sure entries are unique)
    write_ingredients_to_json(data, "data.json")
    print("Finished dumping data!")

if __name__ == "__main__":
    main()
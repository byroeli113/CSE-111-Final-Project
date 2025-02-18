# Time Spent
I spent at least 17 hours on this project. It was significantly more complicated than I anticipated, especially as I tried to add more flexibility to the system. Because of this difficultly, I learned a lot, but also ran out of time to create a lot of the functionality I originally had planned.

One of my biggest problems was flexibility in my code. My text processing algorithms needed to process a lot of different cases while still performing exactly as expected, every time. My biggest struggle was definelty the function `best_regex_match(string_list, target_string, fuzzy_threshold=60)`. It was difficult to understand what the algorithm was doing, and why it kept failing on certain assertions. Between me, Gemini, and GitHub Copilot, we wrote at least 100 interations of the function to try to get to to pass all its tests. 

Interacting with a webpage (without low level control of sending and recieving requests) was also frustrating because based on the webpage's responsiveness, my code behaved differently. 

# What I read
I read a lot of explainations from Gemini and Copilot about using ReGex and fuzzywuzzy (for fuzzy matching) because before this project I had never even heard of either module. 

I read a few StackOverflow posts but there actually wasn't a lot of my specific cases.
# What I accomplished
- [-] Wrote test functions for all functions [decribe all you functions here]
    - [-] Tested Selenium Actions
    - [-] Tested text processing functions
    - [-] Tested convience functions
    - [-] Tested my two big functions
        - [-] `process_items_list(items_list)`
        - [-] `write_ingredients_to_json(list_of_dict_items, filename)`
- [-] Wrote docstrings that explain all my functions really well
- [-] Commented up all my code so I can understand it and so that anyone reading it can understand it
- [-] Published project as public repository in GitHub
- [x] Scraped a webpage and successfully navigatited through several elements, inlcuding a search bar
- [x] Extracted all displayed results from a search 
- [x] Used the above mentioned results to get pages with nutrition information
- [x] Used text processing to extract information that matched data I wanted to put in my data base 
    - [x] Used functions (with some text processing) to fix every value I extracted to the data base standard
- [x] Dumped data into a JSON file
    - [x] Ensured that there are no duplicate values in my data base when I'm dumping

> **Note:** 
> See function docstrings and comments within the functions for a decription of what they do
from acceptable_standards import UNIT_LIST_COMPARABLE, UNIT_PREFIXES_W_VALUE
import re
from fuzzywuzzy import fuzz

# TO-DO: Add comments explaining each ReGex pattern 

def identify_data_type(a_string):
    ''''
    Uses Regex patterns to find whether or not a string is:
        - A word/phrase like "chicken" or "Vitamin A"
        - A measurement like "0g grams" 
        - A daily recommended value percetage like 8% daily value"
    Only takes lowercase strings
    RETURN: one of three strings:
        - "word/phrase"
        - "measurment"
        - "dv"
    '''
    if "%" in a_string:
        return "dv"
    elif bool(re.search(r"\d+", a_string)): # Checks for digits
        return "measurement"
    elif a_string in UNIT_LIST_COMPARABLE:
        return "unit"
    else:
        return "word/phrase"
    
def remove_text_in_brackets(text):
    """
    CREDIT: Gemini 2.0 Flash
    Removes any text contained like so: <text_that_will_be_removed>
    It also removes the <>
    """

    pattern = r"<[^>]*>"
    return re.sub(pattern, "", text)

# CRED: Gemmini 2.0 Flash helped a lot with this function
# It took at least 100 iteration though and a lot of testing
def best_regex_match(string_list, target_string, fuzzy_threshold=60):  # Added threshold parameter
    """
    CREDIT: Gemini 2.0 Flash
    Gemini helped a lot, but it took many iterations, with me fixing things inbetween

    Parameters:
        - string_list: A list of strings to match
        - target_string: the string we are matching against
        - fuzzy_threshold: The minimum score for fuzzy matching (default is 60)
    Returns:
        - The best match from the list, or None if no match above the fuzzy theshold is found

    Finds the closest match, handling "total" prefixes, using regex/fuzzy,
    and filtering matches below a fuzzy threshold.
    """
    # Removes the word "total" from matching criteria. This fixed so much
    # because if you have something like "total fat" it matches much better with "total water" than "fat"
    # by almost every metric (that does not bias the score completely to matching the ends of words [which breaks other values btw])
    target_string = target_string.lower()
    target_string = re.sub(r"^total\s+", "", target_string).strip()

    best_match = None
    highest_score = 0

    for candidate_string in string_list:
        # Lower case our canidate string (we're ignoring case)
        candidate_string = candidate_string.lower()
        # Remove those pesky "total"s
        candidate_string = re.sub(r"^total\s+", "", candidate_string).strip()

        # 1. Exact Regex Match
        # This is the easiest way to find a string, if it exactly matches
        regex_match = re.fullmatch(re.escape(target_string), candidate_string, re.IGNORECASE)
        if regex_match:
            # Skip all that scoring nonsense, we have the string we want
            return candidate_string


        # 2. Partial Regex Match (Beginning of String)
        regex_match = re.match(re.escape(target_string), candidate_string, re.IGNORECASE)
        if regex_match: # Checks if anything matched
            score = len(target_string) # Scores based on the length of the match we got
            if score > highest_score: # As this loops through we end up with the best score and the best match
                highest_score = score
                best_match = candidate_string

    # We found our best match and we can return it
    if best_match: 
        return best_match

    # 3. Fuzzy Matching (only if there is no regex match)
    # Fuzzy matching (using fuzzywuzzy) allows us to match strings using more complicated algorithms
    best_fuzzy_match = None
    highest_fuzzy_score = 0

    for candidate_string in string_list:
        # This uses Levenshtein Distance (see README what I learned) to output a number between 0 and 100 
        # that indicates how much something matches
        fuzz_ratio = fuzz.ratio(target_string, candidate_string)
        if fuzz_ratio > highest_fuzzy_score:
            highest_fuzzy_score = fuzz_ratio
            best_fuzzy_match = candidate_string

    if best_fuzzy_match and highest_fuzzy_score >= fuzzy_threshold:  # Check against threshold
        return best_fuzzy_match
    else:
        return None  # Return None if below threshold or no match

# CRED: Gemini Flash 2.0
def extract_unit(raw_value):
    """
    CRED: Gemini 2.0 Flash
    Extracts the unit from a string like "128g grams" <- raw_value looks like that
    """

    match = re.search(r"([a-zA-Z]+)", raw_value) # Matches a single letter followed by a word boundary

    if match:
        # Match group one is where regex stores the unit from the search
        unit = match.group(1)
        return unit
    else:
        print(f"Couldn't find a unit in {raw_value}")
        return ""

def extract_number(raw_value):
    """Extracts the number from a string like "128g grams" <- raw_value looks like that"""
    match = re.search(r"\d+", raw_value)

    if match:
        number = int(match.group(0))
        return number
    else:
        return None

def extract_prefix(raw_unit):

    '''
    Extracts something that comes before a letter or set of letters "g" or "Hz"
    That's in the dictionary UNIT_PREFIXES_W_VALUE
    '''
    
    for key in UNIT_PREFIXES_W_VALUE.keys():
        if key in raw_unit:
            return key

    # regexafied_goal_unit = re.escape(goal_unit)
    # # CRED: Gemini 2.0 for the ReGex pattern
    # match = re.search(rf"(^.*?)(?={regexafied_goal_unit}\b)", raw_unit) 

    # if match:
    #     return match.group(0)
    # else:
    #     return ""

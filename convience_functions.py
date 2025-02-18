from acceptable_standards import *
from text_processing_functions import *

def calculate_dv_from_measurement(measurment, place):
    """Returns the daily value of a given measurement as stored in DAILY_RECOMMENDED_VALUES. 
    It then divides the measurement by the daily value to get a percentage."""
    dv_measure = DAILY_RECOMMENDED_VALUES[place][1]
    return measurment / dv_measure

def calculate_measurment_from_dv(dv, place):
    """Reverses the calculate_dv_from_measurement from measurment function (see above)"""
    dv_measure = DAILY_RECOMMENDED_VALUES[place][1]
    return dv * dv_measure

def process_raw_nutrient_list(raw_list, place_your_trying_to_put_it):
    """
    Use other functions to turn a raw_list into a processed list

    Input:
        a list of nutrients like so ["33g grams", "8% daily value"]
        raw_list can also look like this ["8% daily value"] and then we fill in the missing value
    
    Output:
        a list of nutrients like so [33, 0.08]. This data is converted to its proper units and is ready to be dumped
    """
    place = find_data_place(place_your_trying_to_put_it)
    # Returns a processed list
    fixed_measurement = None
    fixed_dv = None
    for item in raw_list:
        match identify_data_type(item):
            case "measurement":
                fixed_measurement = fix_measurment(item, get_goal_unit(place_your_trying_to_put_it))
            case "dv":
                fixed_dv = fix_dv(item)

    if fixed_dv == None:
        fixed_dv = calculate_dv_from_measurement(fixed_measurement, place)
    elif fixed_measurement == None:
        fixed_measurement = calculate_measurment_from_dv(fixed_dv,place)

    return [fixed_measurement, fixed_dv]

def is_last_item_in_list(item, alist):
    """Check if an item is the last item in a list"""
    return alist[-1] == item

def find_data_place(place_your_trying_to_put_it):
    """Gets the index of the data place in ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE
    Uses best_regex_match to find the best match in the labels of the list.
    """
    all_labels = []
    for label_and_unit_list in ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE:
        all_labels.append(label_and_unit_list[0])
    exact_label = best_regex_match(all_labels, place_your_trying_to_put_it)

    for index in range(len(ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE)):
        if exact_label == ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE[index][0]:
            return index

def get_goal_unit(place_your_trying_to_put_it):
    """Finds the place your trying to put your data and then extracts the required units for that place."""
    place_index = find_data_place(place_your_trying_to_put_it)
    goal_unit = ACCEPTABLE_INGREDIENTS_DATA_W_UNITS_COMPARABLE[place_index][1]
    return goal_unit

def fix_measurment(raw_measure, goal_unit):
    """Converts a raw measurment into a unit that matches our standards"""
    number = extract_number(raw_measure)
    unit = extract_unit(raw_measure)

    if unit != None:
        prefix = extract_prefix(unit)
        goal_prefix = extract_prefix(goal_unit)

        current_mulitplier = UNIT_PREFIXES_W_VALUE[prefix]
        target_multiplier = UNIT_PREFIXES_W_VALUE[goal_prefix]

        # Take value to base unit
        value = number * current_mulitplier
        # Then convert it to the goal unit
        value = value / target_multiplier

    return value

def fix_dv(raw_dv):
    """Converts a raw daily value (string) into a decimal representation of the percetage"""
    search = re.search(r"\d+", raw_dv)
    return float(search.group(0))/100
    

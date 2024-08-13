from assumptions import my_assumptions_names, my_assumptions_rate_card


def find_key(key1, my_assumption_names_param, my_assumptions_rate_card_param):
    for key, value in my_assumption_names_param.items():
        if value == key1:
            return my_assumptions_rate_card_param[key]


#print(find_key("EPF", my_assumptions_names, my_assumptions_rate_card))

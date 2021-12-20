import re

BUILDING_PERIODS = [
            'before_1941',
            'between_1941_1977',
            'between_1977_1990',
            'between_1990_2000',
            'between_2000_2010',
            'not_finished',
            'not_started'
]


def get_eur_price(input_string, price_pattern=r'\d+\.\d+\.?[0-9]*'):
    if '€' in input_string:
        final_string = input_string[:input_string.find('€')]
    if 'EUR' in input_string:
        final_string = input_string[:input_string.find('EUR')]
    return int(re.findall(price_pattern, final_string)[-1].replace('.', ''))


def translate_building_year_values(input_val):
    dict_of_values = {
        'Înainte de 1941': 'before_1941',
        'Între 1941 şi 1977': 'between_1941_1977',
        'Între 1977 şi 1990': 'between_1977_1990',
        'Între 1990 şi 2000': 'between_1990_2000',
        'Între 2000 şi 2010': 'between_2000_2010'
    }
    if input_val in dict_of_values:
        return dict_of_values[input_val]
    return input_val.strip()


def get_building_year_category(
        input_val,
        year_categories=BUILDING_PERIODS
):
    if input_val in year_categories:
        return input_val
    if int(input_val) < 1941:
        return 'before_1941'
    if int(input_val) < 1977:
        return 'between_1941_1977'
    if int(input_val) < 1990:
        return 'between_1977_1990'
    if int(input_val) < 2000:
        return 'between_1990_2000'
    if int(input_val) < 2010:
        return 'between_2000_2010'
    return 'after_2010'

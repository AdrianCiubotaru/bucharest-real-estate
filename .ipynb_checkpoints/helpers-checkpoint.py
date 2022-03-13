import re
import pandas as pd
import boto3
from io import BytesIO

BUILDING_PERIODS = [
            'before_1941',
            'between_1941_1977',
            'between_1977_1990',
            'between_1990_2000',
            'between_2000_2010',
            'after_2010',
            'not_finished',
            'not_started'
]

BUCHAREST_AREAS = [
    '1_mai_area',
    'agronomie_area',
    'aviatiei_area',
    'aviatorilor_area',
    'banu_manta_area',
    'chibrit_area',
    'domenii_area',
    'dristor_area',
    'stefan_cel_mare_area',
    'titulescu_area',
    'turda_area'
]

FLOOR_CATEGORIES = [
    'first_floor', 
    'last_floor', 
    'middle_floor'
]

BUILDING_STRUCTURES = [
    'concrete_building_structure', 
    'unknown_building_structure',
    'other_building_structure'
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


def create_dict_of_mean_area_prices(input_df, input_areas=BUCHAREST_AREAS):
    return {area: input_df[input_df[area] == 1]['eur_price'].mean() for area in input_areas}


def get_benchmark_price_for_one_area(input_row, input_area_dict):
    area_of_property = [area for area in input_area_dict if input_row[area] == 1][0]
    return input_area_dict[area_of_property]


def get_benchmark_prices_list(input_test_df, input_train_df):
    areas_dict = create_dict_of_mean_area_prices(input_train_df)
    return input_test_df.apply(lambda row: get_benchmark_price_for_one_area(row, areas_dict), axis=1).to_list()


def get_df_from_s3(input_bucket, input_key):
    s3 = boto3.resource('s3')
    obj = s3.Object(input_bucket, input_key)
    with BytesIO(obj.get()['Body'].read()) as file:
        df_from_s3 = pd.read_csv(file)
    return df_from_s3

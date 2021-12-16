import pandas as pd


def _print_success_message():
    print('Test passed!')
    
def test_rent_removed(input_df):
    assert input_df['price'].apply(lambda x: '/ lună' in x).sum() == 0
    _print_success_message()

    
def test_price_values(input_df):
    assert input_df['eur_price'].isnull().sum() == 0
    _print_success_message()
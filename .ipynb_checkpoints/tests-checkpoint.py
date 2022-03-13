import pandas as pd


def _print_success_message():
    print('Tests passed!')
    
def test_rent_removed(input_df):
    assert input_df['price'].apply(lambda x: '/ lună' in x).sum() == 0
    _print_success_message()
    
    
def test_column_has_only_accepted_values(input_df, input_col, accepted_values):
    assert all([val in accepted_values for val in input_df[input_col].unique()])
    _print_success_message()
    
    
def test_column_has_no_null_values(input_df, input_col):
    assert input_df[input_col].isnull().sum() == 0
    _print_success_message()

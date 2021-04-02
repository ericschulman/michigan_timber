import pandas as pd
import numpy as np
import datetime


def add_potential_bidders(df, date_name='Bid Open Date', bidder_name='Bidder Name'):
    # Baldwin Office
    df_edit = df.copy()
    df_edit['month_year'] = pd.to_datetime(
        df_edit[date_name]).dt.to_period('M').astype(str)
    new_dict_1 = df_edit.groupby('month_year').apply(
        lambda x: x[bidder_name].unique().tolist()).to_dict()
    '''delete = ['2013-05', 'NaT']
    for d in delete:
        del new_dict_1[d]'''
    Dict_1 = dict(sorted(new_dict_1.items()))

    # Create a dataframe with 2 columns (1) potential bidders and (2) the months they were active
    df1 = pd.DataFrame.from_dict(Dict_1, orient="index").sort_index(
    ).stack().reset_index(level=1, drop=True).reset_index()
    df1.columns = ['month_year', 'Bidder Name']

    # Create dataframe with (1) sale-# and (2) month
    new_dict_2 = df_edit.groupby('month_year').apply(
        lambda x: x['Sale #'].unique().tolist()).to_dict()
    '''delete = ['2013-05', 'NaT']
    for d in delete:
        del new_dict_2[d]'''
    Dict_2 = dict(sorted(new_dict_2.items()))
    df2 = pd.DataFrame.from_dict(Dict_2, orient="index").sort_index(
    ).stack().reset_index(level=1, drop=True).reset_index()
    df2.columns = ['month_year', 'Sale #']

    # Take cross product between the two dataframes and merge based on month
    df3 = df1.merge(df2, on='month_year', how='outer')

    # Merge bidder characteristics with this dataframe
    bidder_characteristics = ['Bid Per Unit', 'Highest_HIGHEST']

    # convert Highest column to dummies
    df_edit = pd.get_dummies(df_edit, columns=['Highest'])
    bid_array = df_edit[['month_year', 'Bidder Name', 'Sale #'] +
                        bidder_characteristics].copy()
    bid_array = bid_array.groupby(
        ['month_year', 'Bidder Name', 'Sale #']).mean()
    bid_merge = df3.merge(
        bid_array, on=['month_year', 'Bidder Name', 'Sale #'], how='left')

    # convert NaNs in Highest column to 0
    bid_merge['Highest_HIGHEST'] = bid_merge['Highest_HIGHEST'].fillna(
        0)

    # Merge auction characteristics with this dataframe
    auction_characteristics = ['Estimated Volume', 'Appraised Value Per Unit']

    auction_array = df_edit[['month_year', 'Bidder Name', 'Sale #'] +
                            auction_characteristics].copy()
    auction_array = auction_array.groupby(
        ['month_year', 'Sale #']).mean()
    auction_merge = bid_merge.merge(
        auction_array, on=['month_year', 'Sale #'], how='left')
    return auction_merge


if __name__ == "__main__":
    df = pd.read_csv("mich_bids.csv")
    baldwin_office = pd.DataFrame(
        df[df['Bid Open Location'] == "Baldwin Office"])
    add_potential_bidders(baldwin_office, date_name='Bid Open Date',
                          bidder_name='Bidder Name').to_csv('panel.csv', index=False)

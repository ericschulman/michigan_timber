import pandas as pd
import numpy as np
import datetime

# def merge_data(mich_sales = pd.read_csv('mich_sales.csv'),mich_bids = pd.read_csv('mich_bids.csv')):
def merge_data(mich_bids,mich_sales):
    mich_bids = mich_bids[mich_bids['Bid Open Location'] == 'Baldwin Office']
    mich_sales = pd.read_csv('mich_sales.csv')
    reformated_salenum = []
    for row in mich_bids['Sale #']:
        reformated_salenum.append(int(row.replace('-','')))
        
    # actual bidders
    acc_bidders = mich_bids.groupby('Sale #').nunique()
    acc_bidders = acc_bidders.rename(columns={"Bidder Name": 'acc_bidders'})
    mich_bids = mich_bids.merge(acc_bidders['acc_bidders'], on= 'Sale #')
    
    mich_bids['Sale #'] = reformated_salenum
    
    #make Highest_HIGHEST
    Highest_HIGHEST = []
    for row in mich_bids['Highest']:
        if row == 'HIGHEST':
            Highest_HIGHEST.append(1)
        else:
            Highest_HIGHEST.append(0)
    
    mich_bids['Highest_HIGHEST'] = Highest_HIGHEST

    mich_sales = mich_sales.rename(columns={"Sale Number": 'Sale #'})
    
    mich_sales_grouped = mich_sales.groupby('Sale #').mean()

    mich_data_merged = mich_bids.merge( mich_sales, on='Sale #')

    return mich_data_merged


def add_potential_bidders(df, date_name='Bid Open Date', bidder_name='Bidder Name'):
    # Baldwin Office
    df_edit = df.copy()
    print(df_edit[date_name])
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
#     print(df1)

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
#     print(df2)

    # Take cross product between the two dataframes and merge based on month
    df3 = df1.merge(df2, on='month_year', how='outer')
#     print(df3)

    # Merge bidder characteristics with this dataframe
    bidder_characteristics = ['Bid Per Unit', 'Highest']

    # convert Highest column to dummies
    pd.get_dummies(df_edit, columns=['Highest'])
    bid_array = df_edit[['month_year', 'Bidder Name', 'Sale #'] +
                        bidder_characteristics].copy()
    bid_array = bid_array.groupby(
        ['month_year', 'Bidder Name', 'Sale #']).mean()
    bid_merge = df3.merge(
        bid_array, on=['month_year', 'Bidder Name', 'Sale #'], how='left')
#     print(bid_merge)

    # Merge auction characteristics with this dataframe
    auction_characteristics = ['Estimated Volume', 'Appraised Value Per Unit','Acres','Length(days)','Received', 'Value','Volume','acc_bidders', 'Highest_HIGHEST']

    # convert Highest column to dummies
    pd.get_dummies(df_edit, columns=['Highest'])
    auction_array = df_edit[['month_year', 'Bidder Name', 'Sale #'] +
                            auction_characteristics].copy()
    auction_array = auction_array.groupby(
        ['month_year', 'Sale #']).mean()
    auction_merge = bid_merge.merge(
        auction_array, on=['month_year', 'Sale #'], how='left')
    
    df4= df1.groupby('month_year').agg({
    'Bidder Name': ['count']})
    
    final_merge = pd.merge(df4,auction_merge,how = 'left', on="month_year")
    
    print(final_merge)
    
    return final_merge
    
if __name__ == "__main__":
    mich_bids = pd.read_csv('mich_bids.csv')
    mich_sales = pd.read_csv('mich_sales.csv')
    add_potential_bidders(merge_data(mich_bids,mich_sales), 'Bid Open Date',
                          'Bidder Name').to_csv('panel.csv', index=False)
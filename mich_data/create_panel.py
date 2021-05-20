import pandas as pd
import numpy as np
import datetime

def merge_data(mich_bids,mich_sales):
    mich_bids = mich_bids[ (mich_bids['Bid Open Location'] == 'Baldwin Office') & (mich_bids['Sale #'].notna()) ]

    #fix the sale # format
    mich_bids['Sale # old'] = mich_bids['Sale #'].copy()
    mich_bids['Sale #'] = mich_bids['Sale #'].apply( lambda x : int(x.replace('-','')) )

    # actual bidders
    acc_bidders = mich_bids[['Sale #','Bidder Name']].groupby('Sale #').nunique()
    acc_bidders = acc_bidders.rename(columns={"Bidder Name": 'acc_bidders'})

    #merge on sale # but drop month or something?
    mich_bids = mich_bids.merge(acc_bidders['acc_bidders'], on= 'Sale #')
    

    mich_sales = mich_sales.rename(columns={"Sale Number": 'Sale #'})
    mich_sales_grouped = mich_sales.groupby('Sale #').max()
    mich_data_merged = mich_bids.merge( mich_sales_grouped, on='Sale #')

    return mich_data_merged


def add_potential_bidders(df, date_name='Bid Open Date', bidder_name='Bidder Name'):

    df_edit = df.copy()
    df_edit['month_year'] = pd.to_datetime(
        df_edit[date_name]).dt.to_period('M').astype(str)
    new_dict_1 = df_edit.groupby('month_year').apply(
        lambda x: x[bidder_name].unique().tolist()).to_dict()
    Dict_1 = dict(sorted(new_dict_1.items()))

    # Create a dataframe with 2 columns (1) potential bidders and (2) the months they were active
    df1 = pd.DataFrame.from_dict(Dict_1, orient="index").sort_index(
    ).stack().reset_index(level=1, drop=True).reset_index()
    df1.columns = ['month_year', 'Bidder Name']

    # Create dataframe with (1) sale-# and (2) month
    new_dict_2 = df_edit.groupby('month_year').apply(
        lambda x: x['Sale #'].unique().tolist()).to_dict()

    Dict_2 = dict(sorted(new_dict_2.items()))
    df2 = pd.DataFrame.from_dict(Dict_2, orient="index").sort_index(
    ).stack().reset_index(level=1, drop=True).reset_index()
    df2.columns = ['month_year', 'Sale #']

    # Take cross product between the two dataframes and merge based on month
    df3 = df1.merge(df2, on='month_year', how='outer')

    df3_len = df3.shape[0]
    df3_copy1 = df3.copy()
    df3_copy2 = df3.copy()
    df3 = pd.concat([df3,df3_copy1,df3_copy2])
    print(df3_len,df3.shape)
    #add unit to the index
    df3_Units = []
    for i in range(df3_len):
        df3_Units.append('MBF')
    for i in range(df3_len):
        df3_Units.append('Cords')
    for i in range(df3_len):
        df3_Units.append('Acres')
    df3['Units'] = df3_Units
   
    # Merge bidder characteristics with this dataframe
    bidder_characteristics = ['Bid Per Unit', 'Highest']

    # convert Highest column to dummies
    bid_array = df_edit[['month_year', 'Bidder Name', 'Sale #', 'Units'] +
                        bidder_characteristics].copy()
    bid_array['Highest'] = 1*(bid_array['Highest'] == 'HIGHEST')

    bid_array = bid_array.groupby(
        ['month_year', 'Bidder Name', 'Sale #','Units']).mean()
    bid_merge = df3.merge(
        bid_array, on=['month_year', 'Bidder Name', 'Sale #','Units'], how='left')
    bid_merge['Highest'] = bid_merge['Highest'].fillna(0)


    # Merge auction characteristics with this dataframe
    auction_characteristics = ['Estimated Volume', 'Appraised Value Per Unit','Acres','Length(days)','Received', 'Value','Volume','acc_bidders']

    # convert Highest column to dummies
    auction_array = df_edit[['month_year', 'Bidder Name', 'Sale #','Units'] +
                            auction_characteristics].copy()
    auction_array = auction_array.groupby(
        ['month_year', 'Sale #','Units']).mean()
    auction_merge = bid_merge.merge(
        auction_array, on=['month_year', 'Sale #','Units'], how='left')
    
    df4= df1.groupby('month_year').agg({
    'Bidder Name': ['count']})
    
    final_merge = pd.merge(df4,auction_merge,how = 'left', on=["month_year"])
    
    final_merge = final_merge[final_merge['Estimated Volume'].notna()]
    final_merge = final_merge.rename(columns={('Bidder Name', 'count'): 'pot_bidders'})
    print(final_merge.columns)

    return final_merge
    
if __name__ == "__main__":
    mich_bids = pd.read_csv('mich_bids.csv')
    mich_sales = pd.read_csv('mich_sales.csv')
    mich_bids_merged = merge_data(mich_bids,mich_sales)
    mich_bids_merged.to_csv('mich_bids_merged.csv')
    panel = add_potential_bidders(mich_bids_merged)
    panel.to_csv('panel.csv', index=False)
import pandas as pd 
import os 

def merge_shit_idk(df):
    #group all news on same day into same row
    news_titles = df.groupby(['Date'])['Text'].apply(lambda x: ', '.join(x.astype(str))).reset_index()
    #news_summaries = news.groupby(['Date'])['Summary'].apply(lambda x: ', '.join(x.astype(str))).reset_index()
    #drop extra date column
    #news_summaries = news_summaries.drop(["Date"], axis=1)

    #update dataframe with merged rows
    #news = pd.concat([news_titles, news_summaries], axis=1)
    return news_titles



df = pd.read_csv("./csvs/barrons_2015_1_news_data.csv", parse_dates=["Date"],
                 index_col=0)
#print(df)

for fileboi in sorted(os.listdir("./csvs/")):
    df_to_append = pd.read_csv("./csvs/" + fileboi, parse_dates=["Date"],
                               index_col=0)
    df = pd.concat([df, df_to_append], axis=0)

df = merge_shit_idk(df)

if not os.path.exists('data'):
    os.makedirs('data')
df.to_csv("./data/bigboi.csv")

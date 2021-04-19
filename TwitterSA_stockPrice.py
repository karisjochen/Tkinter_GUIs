#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Test Bed for Alpha Advantage
"""

import requests, json 
import pandas as pd
import numpy  as np
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning

import tweepy 
from numpy.core.numeric import NaN
from datetime import datetime, timedelta, date
import requests

#Classes provided from AdvancedAnalytics ver 1.25
from AdvancedAnalytics.Text          import text_analysis, text_plot
from AdvancedAnalytics.Text          import sentiment_analysis
from sklearn.feature_extraction.text import CountVectorizer

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import ImageTk, Image

class StockGUI:
    def __init__(self, guiWin, api_key, tweet_api):
        self.guiWin_ = guiWin
        self.guiWin_.title("Stock Price")
        self.guiWin_.geometry("630x650")
        self.api_key = api_key
        self.tweet_api = tweet_api
        
        # Declares root canvas is a grid of only one row and one column
        self.guiWin_.columnconfigure(0, weight=1)
        self.guiWin_.rowconfigure(0, weight=1)
        
        # Set styles for TK Label, Entry and Button Widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial",  20),foreground='deeppink')
        self.style.configure("TEntry", font=("Arial",  25),foreground='deeppink')
        self.style.configure("TCheckbutton",font=("Arial", 20),foreground='deeppink')
        self.style.configure("TButton",font=("Arial",  20),foreground='deeppink')
        
        # Create Frame inside GUI canvas
        self.mainframe = ttk.Frame(self.guiWin_, padding="5 5 5 5")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        # Add Label Widgets to mainframe
        #ttk.Label(self.mainframe, text="Symbol").grid(column=1,row=1, sticky=W)
        ttk.Label(self.mainframe, text="Average Tweet Sentiment"). \
                                              grid(column=1, row=2, sticky=W)
        ttk.Label(self.mainframe, text="Close Price (USD)"). \
                                              grid(column=1, row=3, sticky=W)                                             
        ttk.Separator(self.mainframe, orient=HORIZONTAL).\
                               grid(column=1, row=7, columnspan=4, sticky="EW")
 
                                              
        self.second_frame = ttk.Frame(self.mainframe, padding=(50, 5 ,5, 5), \
                                   relief='sunken', borderwidth=5)
        self.second_frame.grid(column=0, columnspan=4, row=8, rowspan=6, \
                            sticky=( N, W, E, S))
        ttk.Label(self.second_frame,text="Last 30 Days"). \
                                              grid(column=1, row=0, sticky=W)
        
 
        
        col2wdt = 8

        #############NEED TO UPDATE TO PULL SENTIMENT VALUE################# 
        
        self.sentiment_avg = StringVar()
        self.sentiment_avg_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                                textvariable=self.sentiment_avg, justify=CENTER)
        self.sentiment_avg_entry.grid(column=2, row=2, sticky=(W, E))
        
        # Add Entry Widget for Display of the Previous Stock Close Price
        self.p_close_price = StringVar()
        self.p_close_price_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                              textvariable=self.p_close_price, justify=CENTER)
        self.p_close_price_entry.grid(column=2, row=3, sticky=(W, E))
        

        # Add Button Widget for Calling stock_close() to Display Quote 
        ttk.Button(self.mainframe, text="Price", cursor="pirate", width=10,
                   command=self.stock_clear).grid(column=2, row=6, sticky=W)
                           
        self.stock_frame = ttk.Frame(self.mainframe, padding=(50, 5, 5, 5),
                                      relief='sunken', borderwidth=5)
        self.stock_frame.grid(column=3, columnspan=2, row=1, rowspan=6, 
                                      sticky=(N, W, E, S))
        self.s1 = IntVar()
        self.s1.set(0)
        self.sc1 = ttk.Checkbutton(self.stock_frame, text="Tesla", 
                                  variable=self.s1, command=self.stock1, 
                                  onvalue=1, offvalue=0).\
                                  grid(column=1, row=1, sticky=W)
        
        self.s2 = IntVar()
        self.s2.set(0)
        self.sc2 = ttk.Checkbutton(self.stock_frame, text="Amazon", 
                                  variable=self.s2, command=self.stock2, 
                                  onvalue=1, offvalue=0).\
                                  grid(column=1, row=2, sticky=W) 
        self.s3 = IntVar()
        self.s3.set(0)
        self.sc3 = ttk.Checkbutton(self.stock_frame, text="S&P 500 Index", 
                                  variable=self.s3, command=self.stock3, 
                                  onvalue=1, offvalue=0).\
                                  grid(column=1, row=3, sticky=W) 
        self.s4 = IntVar()
        self.s4.set(0)
        self.sc4 = ttk.Checkbutton(self.stock_frame, text="Wendy's", 
                                  variable=self.s4, command=self.stock4, 
                                  onvalue=1, offvalue=0).\
                                  grid(column=1, row=4, sticky=W)

                                
        self.stocks = ['TSLA', 'AMZN', 'VOOG', 'WEN']
        self.twitter_username = ['elonmusk', 'Amazon', 'POTUS','Wendys']
        self.username=StringVar()
        self.today = datetime.now()
        self.cutoff_date = self.today - timedelta(days=30)
        self.num_tweets = 250
        
    def stock_clear(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)


    def stock1(self):
        self.stock_clear()
        self.s1.set(1)
        self.symbol = self.stocks[0]
        self.cutoff_date2, self.stock_df = self.get_stock_data()
        self.username = self.twitter_username[0]
        self.tweets_df = self.user_timeline()
        self.sentiment_scores= self.sentiment()
        self.graph_ts()

      
    def stock2(self):
        self.stock_clear()
        self.s2.set(1)
        self.symbol = self.stocks[1]
        self.cutoff_date2, self.stock_df = self.get_stock_data()
        self.username = self.twitter_username[1]
        self.tweets_df = self.user_timeline()
        self.sentiment_scores= self.sentiment()
        self.graph_ts()
        
    def stock3(self):
        self.stock_clear()
        self.s3.set(1)
        self.symbol = self.stocks[2]
        self.cutoff_date2, self.stock_df = self.get_stock_data()
        self.username = self.twitter_username[2]
        self.tweets_df = self.user_timeline()
        self.sentiment_scores = self.sentiment()
        self.graph_ts()
        
    def stock4(self):
        self.stock_clear()
        self.s4.set(1)
        self.symbol = self.stocks[3]
        self.cutoff_date2, self.stock_df = self.get_stock_data()
        self.username = self.twitter_username[3]
        self.tweets_df = self.user_timeline()
        self.sentiment_scores= self.sentiment()
        self.graph_ts()
    

        
    def get_stock_data(self):   
        
        base_url = \
            r"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
  
        # main_url variable store complete url 
        main_url = base_url + "&symbol="+self.symbol+"&apikey="+self.api_key         
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json format data into python dictionary data type. 
        # rates are returned in a list of nested dictionaries 
        self.result = res_obj.json()
        series = self.result['Time Series (Daily)']
    
        self.date_list = []
        self.stock_close_list = []

    
        for date, dict in series.items():
            # Create date object in given time format yyyy-mm-dd
            self.my_date = datetime.strptime(date, "%Y-%m-%d")
            if self.my_date > self.cutoff_date:
                self.close_price = dict['5. adjusted close']
                self.date_list.append(self.my_date)
                self.stock_close_list.append(self.close_price)
                self.p_close_price.set("$"+self.close_price)
            else:
                break
    
        for i in range(len(self.date_list)):
            if self.date_list[i+1] == (self.date_list[i]- timedelta(days=1)):
                pass
            else:
                self.date_list.insert((i+1), (self.date_list[i]- timedelta(days=1)))
                self.stock_close_list.insert((i+1), self.stock_close_list[i+1]) 
    
        df = pd.DataFrame({'Date': self.date_list, 'Stock Price': self.stock_close_list})
        df['Date'] = df['Date'].dt.date
        df['Stock Price'] = df['Stock Price'].astype('float')
        
        print(df.head())
        return df.iloc[-1]['Date'], df         


    def graph_ts(self):
        font1 = {'family':'Times New Roman','color':'mediumvioletred','size': 16,
                 'weight':'normal'}
        font2 = {'family':'Times New Roman','color':'darkorchid','size': 14,
                    'weight':'normal'}
        font3 = {'family':'Times New Roman','color':'deeppink','size': 14,
                    'weight':'normal'}
        fig, ax = plt.subplots()
        ax.plot(self.stock_df['Date'], self.stock_df['Stock Price'], color='darkorchid', marker='o')
        plt.xticks(rotation=65, horizontalalignment='right')
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel(f'{self.symbol} Daily Stock Price', fontdict=font2)
        ax2 = ax.twinx()
        ax2.plot(self.sentiment_scores['Date'], self.sentiment_scores['sentiment'], color='deeppink', marker='o')
        ax2.set_ylabel(f'Average Daily {self.username} Sentiment', fontdict=font3)
        ax.set_title(f'Relationship Between {self.username} Twitter Sentiment and {self.symbol} Price', fontdict=font1)
       
        
        fig.savefig('stock_sentiment_plot.jpg',
            format='jpeg',
            dpi=100, bbox_inches='tight')
        self.imgobj = ImageTk.PhotoImage(Image.open('stock_sentiment_plot.jpg'))
        self.imgwin = ttk.Label(self.second_frame, image=self.imgobj). \
                        grid(column=0, row=1, rowspan=8, columnspan=5, sticky=W)
        

         
#################extracting data from twitter####################   
    def extract_place(self,row):
        if row['Place Info']:
            return row['Place Info'].full_name
        else:
            return None
            
    def insert_row(self, position, value):
        df1 = self.tweets_df.iloc[0:position]
        df2 = self.tweets_df.iloc[position:]
        df1.loc[position] = [np.nan]*len(df1.columns)
        df1.loc[position,'Date']  = value
        df_result = pd.concat([df1,df2])

        return df_result
        
    def user_timeline(self):
        #self.num_tweets = num_tweets # call will return multiples of 20 unless we specifyy count variable
        min_id_of_previous_batch = None
        self.tweet_list = []
        self.tweet_ids = []
        keep_going = True
    
        while keep_going == True:
            
            self.tweets = self.tweet_api.user_timeline(id=self.username, tweet_mode = 'extended', 
                                       max_id=min_id_of_previous_batch)
            for i in range(len(self.tweets)):
                tweet = self.tweets[i]
                id = tweet.id
                self.tweet_ids.append(id)
                self.tweet_list.append(tweet)
            min_id_of_previous_batch = min(self.tweet_ids)
            if len(self.tweet_list) > self.num_tweets:
                keep_going = False
    
    
        for tweet in self.tweet_list:
            self.tweets_info_list = [[tweet.full_text, tweet.created_at, tweet.id_str, tweet.user.screen_name, \
            tweet.user.id_str, tweet.user.location, tweet.user.followers_count, tweet.user.friends_count,  tweet.place,\
                    tweet.retweet_count, tweet.favorite_count, tweet.lang, tweet.source,\
                    tweet.in_reply_to_status_id, tweet.in_reply_to_screen_name, tweet.in_reply_to_user_id, tweet.is_quote_status] for tweet in self.tweet_list]
    
            self.tweets_df = pd.DataFrame(self.tweets_info_list,columns=['Tweet Text', 'Tweet Datetime', 'Tweet Id', 'User @ Name', \
            'User ID', 'User Location', 'User Followers Count', 'User Following Count','Place Info', 'Retweets', 'Favorites',\
                    'Language', 'Source', 'Replied Tweet Id', 'Replied Tweet User @ Name','Replied Tweet User Id', 'Quote Status Bool'])
    
            # Checks if there is place information available, if so extracts them
            self.tweets_df['Place Info'] = self.tweets_df.apply(self.extract_place,axis=1)
    
        self.tweets_df['Date']= self.tweets_df['Tweet Datetime'].dt.date

    
        today2 = date.today()
        day = self.tweets_df.iloc[0]['Date']
        date_list = []
        today_date = today2
        keep_going = True
        while keep_going == True:
            if today_date > day:
                print('yes')
                date_list.append(today_date)
                today_date = today_date - timedelta(days=1)
            else:
                print('no')
                keep_going = False
        
        date_list.reverse()
        for element in date_list:
            self.tweets_df = self.insert_row(self.tweets_df, 0, element)
        self.tweets_df.reset_index(drop=True, inplace=True)
   

    
            # If the company did not tweet one day, this inserts a row with that missing day
        # filled in and then nan values for all other columns 
        for i in range(len(self.tweets_df)-1):
            if self.tweets_df.iloc[i+1]['Date'] == self.tweets_df.iloc[i]['Date']:
                pass
            elif self.tweets_df.iloc[i+1]['Date'] == (self.tweets_df.iloc[i]['Date'] - timedelta(days=1)):
                pass
            else:
                value = self.tweets_df.iloc[i]['Date'] - timedelta(days=1)
                self.tweets_df = self.insert_row(i+1, value)
    
        # creates a dummy column to represent the tweets that align with the date of stock
        # data we have created. Value = 1 if within date range, 0 otherwise

        thirty_days = []
        for i in range(len(self.tweets_df)):
            if self.tweets_df.iloc[i]['Date'] > self.cutoff_date2:
                thirty_days.append(1)
            else:
                thirty_days.append(0)
    
        self.tweets_df['ThirtyDays'] = thirty_days
    
    
        print(self.tweets_df.head())
        
        return self.tweets_df

     

############END OF TWITTER EXTRACTION#######################
    
    
#######################SENTIMENT BET######################
    def sentiment(self):  
          # Set Pandas Columns Width for Excel Columns
        # Set Pandas Columns Width for Excel Columns
        pd.set_option('max_colwidth', 300)
        df = self.tweets_df
        df = df[df['Replied Tweet Id'].isna()]
        df = df[df['ThirtyDays']==1]
        df = df.reset_index()
        print(df[['Tweet Text', 'Date', 'ThirtyDays']])
        df['Tweet Text'] = df['Tweet Text'].astype(str)
        
        text_col  = 'Tweet Text' #Identify the Data Frame Text Target Column Name
    
        
        # Initialize  and Sentiment Analysis.  
        # n_terms=2 only displays text containing 2 or more sentiment words for
        # the list of the highest and lowest sentiment strings
        sa = sentiment_analysis(n_terms=2)
        
        # Create Word Frequency by Review Matrix using Custom Sentiment 
        cv = CountVectorizer(max_df=1.0, min_df=1, max_features=None, \
                             ngram_range=(1,2), analyzer=sa.analyzer, \
                             vocabulary=sa.sentiment_word_dic)
        stf        = cv.fit_transform(df[text_col])
        sterms     = cv.get_feature_names()
        
        # Calculate and Store Sentiment Scores into DataFrame "s_score"
        self.s_score    = sa.scores(stf, sterms)
        print(self.s_score)

        n_reviews  = self.s_score.shape[0]
        n_sterms   = self.s_score['n_words'].sum()
        max_length = df['Tweet Text'].apply(len).max()
        if n_sterms == 0 or n_reviews == 0:
            print("No sentiment terms found.")
        self.avg_sentiment = self.s_score['n_words'].sum() / n_reviews
        print('{:-<24s}{:>6d}'.format("\nMaximum Text Length", max_length))
        print('{:-<23s}{:>6d}'.format("Total Reviews", n_reviews))
        print('{:-<23s}{:>6d}'.format("Total Sentiment Terms", n_sterms))
        print('{:-<23s}{:>6.2f}'.format("Avg. Sentiment Terms", self.avg_sentiment))
        
        
        df = df.join(self.s_score)
        list(df.columns)
        
        self.g1 = df.groupby(['Date'])[['sentiment']].mean().reset_index()
        print(self.g1)
        self.sentiment_avg.set(self.avg_sentiment)

        return self.g1
     

#########END OF Sentiment Analysis################################
    
        
# Instantiate GUI Canvas Using Tk   

root = Tk()
root.title("Stock Price")
api_key         = "demo"
api_key         = "ENTER PERSONAL PITCH ADVANTAGE KEY HERE"
access_token = 'ENTER PERSONAL TWITTER DEVELOPER ACCESS TOKEN HERE'
access_token_secret = 'ENTER PERSONAL TWITTER DEVELOPER ACCESS TOKEN SECRET HERE'

consumer_key = 'ENTER PERSONAL TWITTER DEVELOPER KEY HERE'
consumer_secret_key = 'ENTER PERSONAL TWITTER DEVELOPER SECRET KEY HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
tweet_api = tweepy.API(auth)


# Paint Canvas Using Class StockGUI __init__()
my_gui = StockGUI(root, api_key, tweet_api)
# Display GUI
root.mainloop()




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

import matplotlib.pyplot as plt
from PIL import ImageTk, Image

class StockGUI:
    def __init__(self, guiWin, api_key):
        self.guiWin_ = guiWin
        self.guiWin_.title("Stock Price")
        self.guiWin_.geometry("750x750")
        self.api_key = api_key
        
        # Declares root canvas is a grid of only one row and one column
        self.guiWin_.columnconfigure(0, weight=1)
        self.guiWin_.rowconfigure(0, weight=1)
        
        # Create Frame inside GUI canvas
        self.mainframe = ttk.Frame(self.guiWin_, padding="5 5 5 5")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        # Set styles for TK Label, Entry and Button Widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial",  20),foreground='black')
        # Create Label Widgets Inside mainframe
        ttk.Label(self.mainframe, text="Symbol").grid(column=1,row=1, sticky=W)
        ttk.Label(self.mainframe, text="Close Price (USD)"). \
                                              grid(column=1, row=2, sticky=W)
        ttk.Label(self.mainframe, text="Previous Close"). \
                                              grid(column=1, row=3, sticky=W)
        ttk.Label(self.mainframe, text="Percent Change"). \
                                              grid(column=1, row=4, sticky=W)
        ttk.Label(self.mainframe, text="Volume"). \
                                              grid(column=1, row=5, sticky=W)
        
        # Create Entry Widgets Inside Mainframe
        self.style.configure("TEntry", font=("Arial",  25),foreground='maroon')
        col2wdt = 8
        # Add Entry Widget for Entering the Stock Symbol
        self.symbol = StringVar()
        self.symbol_entry = ttk.Entry(self.mainframe, width=col2wdt,justify=CENTER,
                        textvariable=self.symbol, font=("Arial", 20, "bold"))
        self.symbol_entry.grid(column=2, row=1, sticky=(W, E))
                           
        # Add Entry Widget for Display of the Last Stock Close Price           
        self.close_price = StringVar()
        self.close_price_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                                textvariable=self.close_price, justify=CENTER)
        self.close_price_entry.grid(column=2, row=2, sticky=(W, E))
        
        # Add Entry Widget for Display of the Previous Stock Close Price
        self.p_close_price = StringVar()
        self.p_close_price_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                              textvariable=self.p_close_price, justify=CENTER)
        self.p_close_price_entry.grid(column=2, row=3, sticky=(W, E))
        
        # Add Entry Widget for Display of the Percent Change in Price
        self.change = StringVar()
        self.change_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                                     textvariable=self.change, justify=CENTER)
        self.change_entry.grid(column=2, row=4, sticky=(W, E))
        
        # Add Entry Widget for Display of Trading Volume for Last Day
        self.vol = StringVar()
        self.vol_entry = ttk.Entry(self.mainframe, width=col2wdt, 
                                        textvariable=self.vol, justify=CENTER)
        self.vol_entry.grid(column=2, row=5, sticky=(W, E))

        # Create Button Widgets Inside mainframe
        self.style.configure("TButton",font=("Arial",  20),foreground='maroon')
        ttk.Button(self.mainframe, text="Price", cursor="hand2", width=10,
                   command=self.stock_close).grid(column=2, row=6, sticky=W)
        
        ttk.Separator(self.mainframe, orient=HORIZONTAL).\
                               grid(column=1, row=7, columnspan=4, sticky="EW")
                                              
        ttk.Label(self.mainframe,text="Last 100 Days"). \
                                              grid(column=1, row=8, sticky=W)
        
        self.imgwin = ttk.Label(self.mainframe, image=""). \
                        grid(column=1, row=9, columns=8, sticky=W)
        
        # Create Checkbutton Widgets Inside mainframe
        self.style.configure("TCheckbutton",font=("Arial", 20),
                             foreground='maroon')
        self.c = IntVar()
        self.c.set(0)
        self.c1 = ttk.Checkbutton(self.mainframe, text="Closing Price", 
                                  variable=self.c, command=self.plt_close, 
                                  onvalue=1, offvalue=0).\
                                  grid(column=3, row=8, sticky=W)
        self.v = IntVar()
        self.v.set(0)
        self.v1 = ttk.Checkbutton(self.mainframe, text="Volume", 
                                  variable=self.v, command=self.plt_vol, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=4, row=8, sticky=W)
        self.ac = IntVar()
        self.ac.set(0)
        self.ac1 = ttk.Checkbutton(self.mainframe, text="Adjusted Close", 
                                  variable=self.ac, command=self.plt_ac, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=2, row=8, sticky=W)
                                  
        self.fav_frame = ttk.Frame(self.mainframe, padding=(50, 5 ,5, 5), \
                                   relief='sunken', borderwidth=5)
        self.fav_frame.grid(column=3, columnspan=2, row=1, rowspan=6, \
                            sticky=( N, W, E, S))
        
        self.stocks = ['IBM', 'AAPL', 'MSFT', 'MRNA', 'PFE', 'NVAX', 'AZN']
        self.s1 = IntVar()
        self.s1.set(0)
        self.sc1 = ttk.Checkbutton(self.fav_frame, text='IBM', 
                                  variable=self.s1, command=self.stock1, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=1, sticky=W)
        self.s2 = IntVar()
        self.s2.set(0)
        self.sc2 = ttk.Checkbutton(self.fav_frame, text='Apple', 
                                  variable=self.s2, command=self.stock2, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=2, sticky=W)
                                 
        self.s3 = IntVar()
        self.s3.set(0)
        self.sc3 = ttk.Checkbutton(self.fav_frame, text='Microsoft', 
                                  variable=self.s3, command=self.stock3, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=3, sticky=W)
        self.s4 = IntVar()
        self.s4.set(0)
        self.sc4 = ttk.Checkbutton(self.fav_frame, text='Moderna', 
                                  variable=self.s4, command=self.stock4, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=4, sticky=W)

        self.s5 = IntVar()
        self.s5.set(0)
        self.sc5 = ttk.Checkbutton(self.fav_frame, text='Pfizer', 
                                  variable=self.s5, command=self.stock5, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=5, sticky=W)
        self.s6 = IntVar()
        self.s6.set(0)
        self.sc6 = ttk.Checkbutton(self.fav_frame, text='Novavax', 
                                  variable=self.s6, command=self.stock6, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=6, sticky=W)
        self.s7 = IntVar()
        self.s7.set(0)
        self.sc7 = ttk.Checkbutton(self.fav_frame, text='AstraZeneca', 
                                  variable=self.s7, command=self.stock7, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=7, sticky=W)                                  
    def stock1(self):
        self.s1.set(1)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(0)
        self.symbol.set(self.stocks[0])
        self.stock_close()
    def stock2(self):
        self.s1.set(0)
        self.s2.set(1)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(0)
        self.symbol.set(self.stocks[1])
        self.stock_close()
    def stock3(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(1)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(0)
        self.symbol.set(self.stocks[2])
        self.stock_close()
    def stock4(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(1)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(0)
        self.symbol.set(self.stocks[3])
        self.stock_close()
    def stock5(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(1)
        self.s6.set(0)
        self.s7.set(0)
        self.symbol.set(self.stocks[4])
        self.stock_close()
    def stock6(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(1)
        self.s7.set(0)
        self.symbol.set(self.stocks[5])
        self.stock_close()
    def stock7(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(1)
        self.symbol.set(self.stocks[6])
        self.stock_close()        

    # Function to get stock close information 
    def stock_close(self) : 
        if self.symbol.get() not in self.stocks:
            self.s1.set(0)
            self.s2.set(0)
            self.s3.set(0)
            self.s4.set(0)
            self.s5.set(0)
            self.s6.set(0)
            self.s7.set(0)
        # Check for missing stock symbol
        if self.symbol.get() == "":
            showinfo(title="Warning", message="Symbol Missing")
            self.clear_entries()
            return
        c_symbol = self.symbol.get().upper()
        self.symbol.set(c_symbol)
        # base_url variable store base url  
        base_url = \
        r"https://www.alphavantage.co/query?function=GLOBAL_QUOTE"

        # main_url variable store complete url 
        main_url = base_url + "&symbol=" + c_symbol + \
                   "&apikey=" + self.api_key      
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json format data into python dictionary data type. 
        # rates are returned in a list of nested dictionaries 
        self.result = res_obj.json()
        try:
            # Get and Display Last Closing Price
            self.c_price = self.result["Global Quote"]['05. price']
            f_price = round(float(self.c_price), 2)
            self.c_price = str(f_price)
            self.close_price.set("$"+self.c_price)
            
            # Get and Display Previous Day's Closing Price
            self.pc_price = self.result["Global Quote"]['08. previous close']
            f_price = round(float(self.pc_price), 2)
            self.pc_price = str(f_price)
            self.p_close_price.set("$"+self.pc_price)

            # Get and Display Percent Change in Stock Value
            self.p_change = self.result["Global Quote"]['10. change percent']
            self.change.set(self.p_change)
            
            # Get and Display Last Day's Volume for this Stock
            self.volume = self.result["Global Quote"]['06. volume']
            v = int(self.volume) # converts the string self.volume to integer
            v = "{:,}".format(v) # converts int to string with commas
            self.vol.set(v)
            
            self.plt_close()
            
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()

    def clear_entries(self):
        self.symbol.set("")
        self.close_price.set("")
        self.p_close_price.set("")
        self.change.set("")
        self.vol.set("")
        self.imgwin = ttk.Label(self.mainframe, text=""). \
                        grid(column=1, row=8, columns=8, sticky=W)

    def get_series(self):
        # Check for missing stock symbol
        if self.symbol == "":
            showinfo(title="Warning", message="Symbol Missing")
            return
        c_symbol = self.symbol.get().upper()
        # base_url variable store base url  
        base_url = \
          r"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
    
        # main_url variable store complete url 
        main_url = base_url + "&symbol="+c_symbol+"&apikey="+self.api_key         
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json format data into python dictionary data type. 
        # rates are returned in a list of nested dictionaries 
        result = res_obj.json()
        
        try:
            series = result['Time Series (Daily)']
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
            return
        
        n = len(series)
        f_array = np.array([[0.0]*4]*n)
        i_array = pd.Series([0]*n)
        t_array = pd.Series([pd.to_datetime("2020-01-01")]*n)
        i = n-1
        
        for key in series:
            t_array.loc[i] = pd.to_datetime(key, utc=False)
            i_array.loc[i] = int(series[key]['6. volume'])
            f_array[i][0] = float(series[key]['5. adjusted close'])
            f_array[i][1] = float(series[key]['4. close'])
            f_array[i][2] = float(series[key]['3. low'])
            f_array[i][3] = float(series[key]['2. high'])
            i-=1
            
        df0 = pd.DataFrame(t_array, columns=['date'])
        df1 = pd.DataFrame(f_array, columns = \
                          ['adjusted_close', 'close', 'low', 'high'])
        df2 = pd.DataFrame(i_array, columns=['volume'])
    
        self.df  = pd.concat([df0, df1, df2], axis=1).set_index('date')
    
    def graph_ts(self):
        self.get_series()
        # Check for missing stock symbol
        if self.symbol.get() == "":
            #showinfo(title="Warning", message="Symbol Missing")
            self.clear_entries()
            return

        if self.c.get() == 1:
            # plot close price
            title = "Closing Price"
            x     = 'close'
        elif self.v.get() == 1:
            # plot volume
            title = "Volume"
            x     = 'volume'
        elif self.ac.get() == 1:
            # plot change
            title = "Adjusted Close"
            x     = "adjusted_close"
            
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor('gray')
        self.fig.patch.set_alpha(0.3)
        font1 = {'family':'Arial','color':'maroon','size': 16,
                 'weight':'normal'}
        font2 = {'family':'Arial','color':'maroon','size': 14,
                 'weight':'normal'}
        gp = self.fig.add_subplot(1,1,1)
        gp.set_facecolor('maroon')
        gp.plot(self.df[x], color='white')
        
        start_date = str(self.df.index[0].date())
        n          = len(self.df.index)-1
        end_date   = str(self.df.index[n].date())
        
        c_symbol   = self.symbol.get().upper() + \
                             " ("  + start_date + " to "  + end_date+")"
                             
        base_url = \
          r"https://www.alphavantage.co/query?function=SYMBOL_SEARCH"
    
        # main_url variable store complete url 
        main_url = base_url + "&keywords="+self.symbol.get()+ \
                        "&apikey="+self.api_key         
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json format data into python dictionary data type. 
        # rates are returned in a list of nested dictionaries 
        result = res_obj.json()
        
        try:
            series = result['bestMatches']
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
            return
        first_company = result["bestMatches"][0]
        name = first_company["2. name"]
        score = float(first_company["9. matchScore"])
        if score > 0.9:
            plt.title(name,   fontdict=font1)
        else:
            plt.title(c_symbol, fontdict=font1)
        plt.ylabel(title, fontdict=font2)
        plt.grid(True)
        plt.savefig('ts_plot.png')
        plt.show()
        self.imgobj = ImageTk.PhotoImage(Image.open('ts_plot.png'))
        self.imgwin = ttk.Label(self.mainframe, image=self.imgobj). \
                        grid(column=1, row=9, columns=8, sticky=W)

    def plt_close(self):
        self.c.set(1)
        self.v.set(0)
        self.ac.set(0)
        self.graph_ts()
        
    def plt_vol(self):
        self.c.set(0)
        self.v.set(1)
        self.ac.set(0)
        self.graph_ts()
        
    def plt_ac(self):
        self.c.set(0)
        self.v.set(0)
        self.ac.set(1)
        self.graph_ts()
# Instantiate GUI Canvas Using Tk   

root = Tk()
root.title("Stock Price")
api_key         = "demo"
api_key         = "CK8FNM4QB629PDZL"
# Paint Canvas Using Class StockGUI __init__()
my_gui = StockGUI(root, api_key)
# Display GUI
root.mainloop()


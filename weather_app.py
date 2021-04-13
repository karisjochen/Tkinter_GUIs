import requests
from bs4 import BeautifulSoup
import pandas as pd
import mechanicalsoup

from tkinter import *
from tkinter import Tk
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning

from PIL import ImageTk, Image

        
# master belongs to the root, so the TK class. We renamed it master
class Weather:
    def __init__(self, master):
        self.master = master
        self.master.title("Upcoming Weather Forecast")
    
        self.master.config(bg='white')
        self.master.geometry("750x650") 

                # Declares root canvas is a grid of only one row and one column
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        # Create Frame inside GUI canvas
        self.mainframe = ttk.Frame(self.master, padding="5 5 5 5")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Times New Roman",  20),background='white',foreground='deeppink')
        ttk.Label(self.mainframe, text="Desired Location (Example: Boulder, CO)").grid(column=1,row=1, sticky=W)
        self.location = StringVar()
        self.location = ttk.Entry(self.mainframe, validate='all', validatecommand=self.entry_validation,justify=CENTER,
                        textvariable=self.location, font=("Times New Roman", 20, "bold"))
        self.location.grid(column=2, row=1, sticky=(W, E))

                # Create Button Widgets Inside mainframe
        self.style.configure("TButton",font=("Times New Roman",  20),background='white',foreground='deeppink')
        ttk.Button(self.mainframe, text="Get Graph",  width=10,
                   command=self.return_plot).grid(column=2, row=2, sticky=(W, E))

        self.second_frame = ttk.Frame(self.mainframe, padding=(50, 5 ,5, 5), \
                                   relief='sunken', borderwidth=5)
        self.second_frame.grid(column=0, columnspan=3, row=3, rowspan=6, \
                            sticky=( N, W, E, S))
    def return_plot(self):
        self.df = self.weather_data()

        font1 = {'family':'Times New Roman','color':'deeppink','size': 16,
            'weight':'normal'}
        font2 = {'family':'Times New Roman','color':'deeppink','size': 14,
                    'weight':'normal'}
        sns.set_style('darkgrid')
        plt.figure(figsize=(6, 5), dpi=50)
        scatter = sns.lmplot(x='period', y='temp value', data=self.df, hue='High/Low', \
            palette={'High':'deeppink', 'Low': 'deepskyblue'},fit_reg=False)
        plt.xticks(rotation=65, horizontalalignment='right')
        scatter.fig.subplots_adjust(top=0.95, bottom=0.2)
        scatter.ax.set_title('Projected Weather Report', fontdict=font1)
        plt.ylabel('Projected Temperature',fontdict=font2)

        plt.savefig('weather_plot.png')

        self.imgobj = ImageTk.PhotoImage(Image.open('weather_plot.png'))
        self.imgwin = ttk.Label(self.second_frame, image=self.imgobj). \
                        grid(column=0, row=1, columnspan=3, sticky=W)


    def entry_validation(self):
        pass


    def weather_data(self):
        if self.location.get() == "":
            showinfo(title="Warning", message="Symbol Missing")
        try:
                
            url = 'https://forecast.weather.gov'
            browser = mechanicalsoup.StatefulBrowser(
                soup_config={'features': 'lxml'},  # Use the lxml HTML parser
                raise_on_404=True
            )

            home_page = browser.open(url)
            home_page_url = browser.get(url).url
            home_html = home_page.soup # if we want to look at the html
            form = home_html.select('form[id="getForecast"]')[0] # this is a list
            form.select('input[id="inputstring"]')[0]['value'] = self.location.get() # setting search value
            boulder_page = browser.submit(form, url=home_page_url)
            boulder_html = boulder_page.soup

            week_forecast = boulder_html.select('div[id="seven-day-forecast-container"]')[0]
            days_forecast = week_forecast.find_all(class_='tombstone-container')


            period_names = [item.find(class_='period-name').get_text() for item in days_forecast]
            short_descriptions = [item.find(class_='short-desc').get_text() for item in days_forecast]
            temperatures = [item.find(class_='temp').get_text() for item in days_forecast]
            desc = []
            deg = []
            unit = []
            for temp in temperatures:
                x = temp.split()
                y = x[0]
                desc.append(y[:-1])
                deg.append(x[1])
                unit.append(x[2])

            self.df_weather = pd.DataFrame({'period': period_names, 'short_descriptions': short_descriptions,\
                'temps': temperatures, 'High/Low': desc, 'temp value': deg})
            
            self.df_weather['temp value'] = self.df_weather['temp value'].astype('int') 

            return self.df_weather
        except:
        # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Location " + self.location.get() + " Not Found"
            showwarning(title="Warning", message=warn_msg)
        
        return

root = Tk()

# must include root 
my_gui = Weather(root)
root.mainloop()
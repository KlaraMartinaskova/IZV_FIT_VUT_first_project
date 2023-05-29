#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: Klára Martinásková

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""


from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def integrate(x: np.array, y: np.array) -> float:
    """ Numeric count of a integral. """
    
    result = []
    for i in range(1,len(x)):
        result.append((x[i]-x[i-1]) * ((y[i-1]+y[i])/2))

    return sum(result)
    #pass


def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None=None):
    """ Function for generating graph with three functions. """

    a = np.array(a).reshape(-1,1)
    x = np.arange(-3,3,0.01).astype("f")

    f = np.power(x,2) * a

    fig = plt.figure(figsize=(9,4))

    ax = fig.add_subplot()

    # setting lables and axis parameters
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_a(x)$")
    ax.set_xlim([-3,3.9])
    ax.set_ylim([-20, 20])

    for i in range(len(a)):
        ax.plot(x,f[i,:], ls='-', label=r'$\gamma_{%0.1f}(x)$' %(a[i]))
        ax.fill_between(x,f[i,:],0, alpha=0.2) #filling space under curve - integral
        ax.annotate(
            text = r'$\int f_{%0.1f} (x)\,dx\ $' %(a[i]) , 
            xy=(0.87,f[i,0] ), 
            xytext=(1, 0), 
            xycoords=ax.get_yaxis_transform(), 
            textcoords="offset points", 
            size=10,  
            va="center")

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=False)

    if show_figure==True:
        plt.show()

    if save_path != None:
        fig.savefig(save_path)
    #pass

def generate_sinus(show_figure: bool=False, save_path: str | None=None):
    t = np.arange(0,100).astype("f")
    f1 = 0.5 * np.sin((1/50)*np.pi*t)
    f2 = 0.25 * np.sin(np.pi*t)

    pass


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    """ Function for download data from URL. """

    # Make a GET request to fetch the raw HTML content
    html_content= requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content,features="html.parser")

    table = soup.find('table')
    gdp_table_data = table.find_all('tr') # row
    final_list = [] # list for saving final data

    for row in range(len(gdp_table_data)):
        headings = [] 
        records = gdp_table_data[row].find_all("td")
        contents = {"year": None, "month": None, "temp": None}
        for td_idx in range(len(records)):
            td = records[td_idx]
            # remove any newlines and extra spaces from left and right
            str_ = td.text.replace('\n',' ').strip()
            if td_idx == 0 or td_idx == 1:
                headings.append(int(str_)) # first to items integer
            elif str_ !='Â': # means no records
                headings.append(float(str_.replace(',','.'))) # type float
            

        contents["year"] = headings[0]
        contents["month"] = headings[1]
        contents["temp"] = np.array(headings[2:])
        final_list.append(contents)
        
    return(final_list)
        #pass


def get_avg_temp(data, year=None, month=None) -> float:
    """ Function for data processing over a month and over a year. """

    results = download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html")
    k=[] # for saving select values of temp

    if year != None and month !=None: # if both are specified
        [k.append((td["temp"])) for i,td in enumerate(results) if td["year"] == year and td["month"] == month ]
    elif year != None: # only year is specified
        [k.append((td["temp"])) for i,td in enumerate(results) if td["year"] == year]
    elif month !=None: # only month is  specified
        [k.append(td["temp"]) for j,td in enumerate(results) if td["month"] == month]
    else:
        [k.append((td["temp"])) for i,td in enumerate(results)]  


    new_k = np.concatenate(k, axis=0 ) 
    return(np.mean(new_k))
    #pass

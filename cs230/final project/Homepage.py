'''
Name:   Janhavi Maniar
CS230:  Section 4
Data:   Shipwreck Database
URL:

Description:
This program uses data from the NJ Maritime Museum about shipwrecks. It starts by presenting a series of charts to analyze
and visualize the data. It also contains an interactive map in which the user can view the specific locations of shipwrecks
and filter the data based on the year of the shipwreck or the type of vessel.
'''

import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

path = "/Users/janhavi/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/final project"
st.set_option('deprecation.showPyplotGlobalUse', False)


df_shipwreck = pd.read_csv(path + "/Shipwreck_Database.csv")

df_shipwreck.set_index("SHIP'S NAME", inplace =True)

df_shipwreck.rename(columns={"LATITUDE":"lat", "LONGITUDE": "lon"}, inplace= True)

#PAGE 1 - Welcome and Charts

st.markdown("<span style= 'font-size: 45px'>**:green[Shipwreck Information]**</span>", unsafe_allow_html=True)

#header image
ship_image = Image.open("/Users/janhavi/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/final project/getimage-3-2.jpg")
st.image(ship_image, width = 700)

#welcome paragraph
st.header("Welcome!")
st.write("Whether caused by storms, human error, or hostile actions, shipwrecks have claimed countless lives and left countless stories to be told. Today, shipwrecks are often sought out by divers and historians alike, as they offer a glimpse into the past and provide valuable insights into the lives and experiences of those who once sailed the seas. Despite their tragic nature, shipwrecks continue to captivate our imaginations and remind us of the ever-present risks and uncertainties of life at sea. This site provides information regarding shipwrecks from the 19th and 20th centuries. All the information is based off data from the NJ Maritime Museum.")


##CHARTS
st.markdown("<span style= 'font-size: 45px'>**:blue[Charts]**</span>", unsafe_allow_html=True)

#Line chart showing number of losses per year
st.header("Yearly Losses")
df_years = df_shipwreck["YEAR"].copy()
df_years.dropna(inplace=True)

years = {}
def frequencyDict(data, dict, count = 1):
    '''
    :param data: the set of data that is being counted
    :param dict: an empty dictionary created to add variables and the frequencies
    :param count: the initial frequency of the value
    :return: a dictionary with the key as each variable and the value as the corresponding frequency
    '''
    for a in data:
        if a not in dict:
            dict[a] = count
        else:
            prev_count = int(dict[a])
            new_count = prev_count + count
            dict[a] = new_count
    return dict

frequencyDict(df_years, years)


#sort in increasing order
year_list = []
for k,v in years.items():
    values = (k,v)
    year_list.append(values)
sorted_years_list = sorted(year_list)


#return back to dict
sorted_years = dict(sorted_years_list)


#create a line chart - https://www.w3schools.com/python/matplotlib_line.asp
year = list(sorted_years.keys())
loss_freq = list(sorted_years.values())

plt.plot(year, loss_freq, color='darkcyan')
plt.title("Losses Per Year")
plt.xlabel('YEAR')
plt.ylabel('LOSSES')

st.pyplot()

#add a caption
st.caption("This chart shows the number of shipwrecks occurring every year between 1731 and 2020. The number of shipwrecks were increasing in the lat 19th centruty but began decreasing with the start of the 20th century. The end of warfare and the development of technology played a huge role in decreasing shipwrecks.")



#Bar chart showing cause of loss
st.header("Top 5 Causes of Loss")
df_loss = df_shipwreck["CAUSE OF LOSS"].copy()
df_loss.dropna(inplace=True)


#keep just the first word from cause of loss
first_word = [i.split(" ")[0] for i in df_loss]

#create a dictionary with the cause and frequency
final_words = {}
frequencyDict(first_word, final_words)


#create a tuple to order decreasingly
cause_list = []
def orderDecreasingly(word_dict, list):
    for k, v in word_dict.items():
        values = (v, k)
        list.append(values)
    sorted_cause_list = sorted(list, reverse=True)[:5]

    return sorted_cause_list


#convert tuple back to dict
sorted_cause_dict = dict(orderDecreasingly(final_words, cause_list))


#create a bar chart - https://www.w3schools.com/python/matplotlib_bars.asp
causes = list(sorted_cause_dict.values())
cause_freq = list(sorted_cause_dict.keys())

#color codes found using color library: https://htmlcolorcodes.com/colors/
colors = ['#C04000', '#F08000', '#E3735E', '#FFAA33', '#EC5800']

plt.bar(causes, cause_freq, color = colors)
plt.title('Causes of Loss')
plt.xlabel('CAUSES')
plt.ylabel('FREQUENCY OF LOSS')

st.pyplot()

#add a caption
st.caption("This graph shows the most common causes of shipwrecks. The #1 cause of shipwrecks is ships getting stranded in the ocean. It is about five times more likely to occur than a ship getting burned.")



#create a pie chart to show top 5 most frequent vessel types
st.header("Top 5 Shipwrecked Vessel Types")
df_vessel = df_shipwreck[['VESSEL TYPE']].copy()
df_vessel.dropna(inplace=True)


#create a dictionary with the type and frequency
vessel_categories = {}
frequencyDict(df_vessel["VESSEL TYPE"], vessel_categories)


#convert tuple back to dict
vessel_list = []
vessel_dict = dict(orderDecreasingly(vessel_categories, vessel_list))


#create a pie chart - https://www.w3schools.com/python/matplotlib_pie_charts.asp
type = list(vessel_dict.values())
freq = list(vessel_dict.keys())

colors = ['#4682B4', '#89CFF0', '#6082B6', '#A7C7E7', '#191970']

plt.pie(freq, autopct='%1.1f%%', pctdistance=1.2, colors=colors)
plt.legend(type, loc="upper right")
plt.title('Vessel Types')


st.pyplot()

#add caption
st.caption("This graph shows a breakdown of the most common vessel types. It highlights how Schooner ships are most likely to get shipwrecked, acounting for over half of the top types. In more recent times, schooners are less likely to be used.")







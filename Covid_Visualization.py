#!/usr/bin/env python3

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
print('modules are imported')


df = pd.read_csv("/Users/princeskngh/Downloads/countries-aggregated.csv.webarchive.txt.csv")
df.head()


######### Take data of those dates where atleast 1 +(ve) case was confirmed #################
df_confirmed = df[df.Confirmed > 0]
df_confirmed.head()

df_confirmed_India = df_confirmed[df_confirmed.Country == 'India']
df_confirmed_India.head()

#### The first case came in India on 30-th Jan 2020

fig = px.choropleth(df, locations = 'Country', locationmode = 'country names', color = 'Confirmed', animation_frame = 'Date')
fig.update_layout(title_text = "Global spread of COVID_19")
fig.show()


######### India ##########

df_India = df_confirmed_India[['Date', 'Confirmed']]
df_India["Infection Rate"] = df_India["Confirmed"].diff()
df_India
px.line(df_India, x = 'Date', y = ['Confirmed', 'Infection Rate'])

df_India['Infection Rate'].max()


''' Infection rate represents new cases !!
 Hence max infection rate in india is 4,14,188'''

df
''' Maximum patients total on earth at a given time'''
df.Confirmed.max()

################################################################

countries_list = list(df['Country'].unique())
ls = []
for c in countries_list:
    MIR = df[df.Country == c].Confirmed.diff().max()
    ls.append(MIR)

df_MIR = pd.DataFrame()
len(ls)
len(countries_list)
df_MIR['Countries'] = countries_list
df_MIR['Max Infection Rate'] = ls
df_MIR


px.bar(df_MIR, x = 'Countries', y = 'Max Infection Rate', color = 'Countries', title = 'Max Infection Rate World-wise')

px.bar(df_MIR, x = 'Countries', y = 'Max Infection Rate', color = 'Countries', title = 'Max Infection Rate World-wise', log_y = True )


##################### Firstly analysing about covid lockdown effects in italy ##############
'''Analysing about italy since it was in real bad shape in early phase of pandemic '''

start_date = '09-03-2020'
one_month_later = '09-03-2020'

df_Italy = df[df.Country == 'Italy']
df_Italy.head()

df_Italy = df_Italy[df_Italy.Confirmed > 0]
df_Italy.head()

########  First case came of 31st of January ########

df_Italy['Infection Rate'] = df_Italy.Confirmed.diff()
df_Italy.head()

### Analysis till 2021
fig = px.line(df_Italy, x = 'Date', y = 'Infection Rate', title = "Daily Cases in Italy")
fig.show(title = 'Daily new cases in Italy')

############ Lets extract first lockdown data #############
''' Note that format is year-month-date '''
df_Italy_lockdown = df_Italy[df_Italy['Date'] >= '2020-03-06']
df_Italy_lockdown = df_Italy_lockdown[df_Italy_lockdown['Date'] <= '2020-04-06']


fig = px.line(df_Italy_lockdown, x = 'Date', y = 'Infection Rate', title = "Daily Cases in Italy during lockdown")
fig.show()


fig.add_shape(dict(type = 'line',

    x0 = '2020-03-07', y0 = '0',
    x1 = '2020-03-07', y1 = df_Italy_lockdown['Infection Rate'].max(),

    ))


fig.add_shape(dict(type = 'line',

    x0 = '2020-04-06', y0 = '0',
    x1 = '2020-04-06', y1 = df_Italy_lockdown['Infection Rate'].max(),

    ))

fig.add_annotation(
    dict(
    x = '2020-03-07', y = df_Italy_lockdown['Infection Rate'].max(),
    text = 'Lockdown begins'
    )
)

fig.add_annotation(
    dict(
    x = '2020-04-06', y = 0,
    text = 'Lockdown ends'
    )
)


###################### Death rates before and after lockdown #######################
df_Italy['Death Rate'] = df_Italy['Deaths'].diff()
df_Italy.head()


death_infection_plot = px.line(df_Italy, x = 'Date', y = ['Infection Rate', 'Death Rate'])
death_infection_plot.show()


'''Now trying to plot normalized data '''

df_Italy['Death Rate Normalized'] = df_Italy['Death Rate']/(df_Italy['Death Rate'].max())
df_Italy['Infection Rate Normalized'] = df_Italy['Infection Rate']/(df_Italy['Infection Rate'].max())


death_infection_plot_normalized = px.line(df_Italy, x = 'Date', y = ['Infection Rate Normalized', 'Death Rate Normalized'])
death_infection_plot_normalized.show()


################### analysis of India death rate and lockdown ##################

df_India = df[df.Country == 'India']
df_India['Infection Rate'] = df_India['Confirmed'].diff()
df_India = df_India[df_India['Confirmed'] > 0]
df_India['Death Rate'] = df_India.Deaths.diff()
#Though it might turn out to be redundant since confirmed ≥ 0 pretty much always
df_India.head()

px.line(df_India, x = 'Date', y = ['Infection Rate', 'Death Rate'])




# Normalize
df_India['Death Rate Normalized'] = df_India["Death Rate"]/df_India["Death Rate"].max()
df_India['Infection Rate Normalized'] = df_India["Infection Rate"]/df_India["Infection Rate"].max()


px.line(df_India, x = 'Date', y = ['Infection Rate Normalized', 'Death Rate Normalized'])



############ Analysis of Lockdown ############
'''  24th March to 1st June  '''
start = '2020-03-24'
end = '2020-06-01'
df_India_first_lock = df_India[df_India['Date'] <= end]
df_India_first_lock = df_India_first_lock[df_India_first_lock['Date'] >= start]
df_India_first_lock

### It is amazing that initially there were so less cases

fig_infection_first_lock = px.line(df_India_first_lock, x = 'Date', y = 'Infection Rate')
fig_infection_first_lock
'''

It is quiet astonishing that cases went up and up despite a proper lockdown.
Some points to which it can be attributed are:
1) Migrant workers moving in masses.
2) Many religious gatherings, including weddings
3) People not obeying the prescribed guidelines appropriately.


Unfortunately on 1st june unlock was announced, and the number of cases just kept going on and on.
'''

df_India_after_first_lock = df_India[df_India['Date'] <= '2020-12-31']
df_India_after_first_lock = df_India_after_first_lock[df_India_after_first_lock['Date'] >= '2020-06-0']
df_India_after_first_lock
px.line(df_India_after_first_lock, x = 'Date', y = 'Infection Rate')

'So, it is clear that we weremt close to 1/10th the worst hit later this year'


'Likewise for the second lockdown, similar reasoning may be attributed to many religious festivals and political assemblies !!'
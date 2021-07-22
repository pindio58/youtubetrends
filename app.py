# import modules 
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import pytz
import os
import glob
import json
import missingno
from plotly.subplots import make_subplots
import seaborn as sns
import enum
import plotly.graph_objects as go
import plotly as py

# set required path 
cwd = os.getcwd()
path = os.path.join(cwd, "*.csv")

# get all the files 
all_files = glob.glob(path)

#set columns to be used and then load all the Dataframes based on counry name
cols = ['trending_date','title','channel_title','category_id','tags','views','likes','dislikes',
        'comment_count','description']
for filename in all_files:
    name = str(os.path.basename(filename)[:2])
    if name=='US':
        United_States = pd.read_csv(filename , encoding = "ISO-8859-1", usecols=cols)
    if name=='DE':
        Germany = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)
    if name=='MX':
        Mexico = pd.read_csv(filename , encoding = "ISO-8859-1", usecols=cols)
    if name=='GB':
        Britain = pd.read_csv(filename , encoding = "ISO-8859-1", usecols=cols)
    if name=='JP':
        Japan = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)
    if name=='KR':
        Korea = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)
    if name=='CA':
        Canada = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)
    if name=='IN':
        India = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)
    if name=='FR':
        France = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)        
    if name=='RU':
        Russia = pd.read_csv(filename, encoding = "ISO-8859-1", usecols=cols)

#below function will be used for merging category type into the dataframe
def merge_dfs(main,f):
    attributes = json.load(f)
    attributes = pd.json_normalize(attributes, record_path=['items'])
    attributes = attributes[['id','snippet.title']]
    attributes['id'] = attributes['id'].astype(int)
    attributes.columns=['category_id','Genre']
    main = main.merge(attributes, on='category_id', how='left')
    return main

#for json files
path_json = os.path.join(cwd, "*.json")
json_files = glob.glob(path_json)

# merge now
for filename in json_files:
    with open(filename) as f:
        name = str(os.path.basename(filename)[:2])
        if name=='US':
            United_States = merge_dfs(United_States,f)
            United_States.name=str(pytz.country_names[name])
            
        if name=='DE':
            Germany = merge_dfs(Germany,f)
            Germany.name=str(pytz.country_names[name])
            
        if name=='MX':
            Mexico = merge_dfs(Mexico,f)
            Mexico.name=str(pytz.country_names[name])
            
        if name=='GB':
            Britain = merge_dfs(Britain,f)
            Britain.name=str(pytz.country_names[name])
            
        if name=='JP':
            Japan = merge_dfs(Japan,f)
            Japan.name=str(pytz.country_names[name])
            
        if name=='KR':
            Korea = merge_dfs(Korea,f)
            Korea.name=str(pytz.country_names['KR'])
            
        if name=='CA':
            Canada = merge_dfs(Canada,f)
            Canada.name=str(pytz.country_names[name])
            
        if name=='IN':
            India = merge_dfs(India,f)
            India.name=str(pytz.country_names[name])
            
        if name=='FR':
            France = merge_dfs(France,f)
            France.name=str(pytz.country_names[name])
            
        if name=='RU':
            Russia = merge_dfs(Russia,f)
            Russia.name=str(pytz.country_names[name])

# for indexes to show in searborn 
indices = [ (x,y) for x in range(5) for y in range(5) ]            

fig, axes = plt.subplots(2, 5,figsize=(4, 4));
plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=0.5, wspace=0.4)
sns.set(rc={'axes.facecolor':'cornflowerblue'})

countries = [United_States,Germany,Mexico,Britain,Japan,Korea,Canada,India,France,Russia]
for n,country in enumerate(countries):
    x,y = indices[n]
    p = sns.heatmap(country[['likes','views']].corr(),annot=True, cmap='coolwarm' ,ax=axes[x,y], cbar=False);
    p.set_title(country.name),
    annot_kws={'rotation': 30}

fig.set_size_inches(16.5, 8.5)

#
indices = [ (x,y) for x in range(1,6) for y in range(1,6) ]
plots = ['United States','Germany','Mexico','Britain','Japan','Korea','Canada','India','France','Russia']
fig = make_subplots(
    rows=2, cols=5,
    subplot_titles=(plots))

for n,country in enumerate([United_States,Germany,Mexico,Britain,Japan,Korea,Canada,India,France,Russia]):
    fig.add_trace(go.Scatter( x=country['views'], y=country['likes']),row=indices[n][0], col=indices[n][1])

fig.update_layout(
    autosize=False,
    width=1000,
    height=800,)
fig.show();

###########    Starts for whole world here    ########

for country in countries:
    country['country'] = country.name

world = pd.concat(countries, axis=0)
fig = px.scatter(world[['likes','views','title','country']], x='views', y='likes',color='country',
                 hover_data=['title','country']);
fig.update_layout(
    autosize=False,
    width=800,
    height=800,)
fig.show();
    
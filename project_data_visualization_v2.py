# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:15:30 2021

@author: omarz
"""

import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State




players_df = pd.read_csv('premier-league-dataset.csv')



app = dash.Dash(external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'])


@app.callback(Output('BAN1', 'children'),
              Output('BAN2', 'children'),
              Output('BAN3', 'children'),
              Output('BAN4', 'children'),
              Output('BAN5', 'children'),
              Output('BAN6', 'children'),
              Output('top_scoring_players', 'figure'),
              Output('goals_vs_assists', 'figure'),
              Output('starts_vs_goals', 'figure'),
              Output('goals_per_club', 'figure'),
              Output('Most_Nationality', 'figure'),
              Input('submit', 'n_clicks'),
              State('dropdown', 'value'))
def display_value(n_clicks, value):
    if value == 'All':
        position_df = players_df
    else:
        position_df = players_df[players_df['one_Position'] == value]
    
    total_goals = np.sum(position_df['Goals'])
    goals_avg_per_player = round(np.mean(position_df['Goals']), 2)
    assists_avg_per_player = round(np.mean(position_df['Assists']), 2)
    avg_ycards = round(np.mean(position_df['Yellow_Cards']), 2)
    avg_rcards = round(np.mean(position_df['Red_Cards']), 2)
    avg_age = round(np.mean(position_df['Age']), 2)
    
    TSP = px.bar(position_df.sort_values('Goals').tail(10), x='Goals' , y='Name', title='Top Scoring Players', orientation='h')
    
    GvA = px.scatter(position_df, x = 'Assists', y = 'Goals', title='Goals vs Assists', color = 'one_Position', hover_data=['Name'], template="simple_white") # Goals vs Assists
    
    GvS = px.scatter(position_df, x= 'Starts', y = 'Goals', title='Goals vs Starts', color = 'one_Position', hover_data=['Name'], template="simple_white") # Starts vs Goals
    
    for_gbc = position_df.sort_values('Goals').groupby('Club').Goals.sum().sort_values()
    GPC = px.bar(for_gbc, x= for_gbc , y= for_gbc.index, title='Goals per Club', orientation='h', labels={'x':'Goals', 'y':'Club'})
    
    nation = position_df.groupby('Nationality').Name.count().sort_values().tail(10)
    NAT =  px.pie(values=nation, names=nation.index, title='Most Nationalities in league')
    
    return  total_goals, goals_avg_per_player, assists_avg_per_player, avg_ycards, avg_rcards, avg_age, TSP, GvA, GvS, GPC, NAT


app.layout = html.Div([
    
    html.Div([
        
        html.Img(src='/assets/premier-league-3-logo.png', style={'width':'600px', 'height':'200px'}),
    
        ], className = 'row', style={'textAlign':'center'}),
    
    html.Div([
        
        html.H1('English Premier League Players Stats for 20/21 Season', className = 'twelve columns', style={'textAlign': 'center', 'fontFamily':'Script'})
        
        ], className = 'row'),
    
    html.Div([
        
            html.H2('Choose a Position to display data for:'),
            dcc.Dropdown(
            id='dropdown', value='All', options=[
                {'label': str(Position), 'value': str(Position)} for Position in np.insert(players_df['one_Position'].unique(), 0, 'All')
                ], className='ten columns'),
            html.Button('Submit', id='submit', n_clicks=0, className='two columns'),
        ], className = 'row', style = {'textAlign' : 'center', 'padding':'10px'}),
    
    html.Div([
        
        html.Div([
            
            html.H4(id='BAN1',
                    style= {'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.P(children=['Total Goals Scored'], 
                   style={'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':20}),
            ], className = 'four columns'),
        
        html.Div([
            html.H2(id = 'BAN2',
                    style= {'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.H3('Average Goals per Match', 
                   style={'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':20})
            ], className = 'four columns', style = {'textAlign' : 'center'}),

        html.Div([
            html.H2(id = 'BAN3',
                    style= {'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.H3('Average Assists per Match', 
                   style={'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':20})
            ], className = 'four columns', style = {'textAlign' : 'center'}),
       
        ], className = 'row'),
    
    html.Div([
    
        html.Div([
            html.H2(id = 'BAN4',
                    style= {'textAlign': 'center', 'color': '#b3b300', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.H3('Yellow Cards per Match', 
                   style={'textAlign': 'center', 'color': '#b3b300', 'fontFamily':'Alkes Regular Italic', 'fontSize':20})
            ], className = 'four columns', style = {'textAlign' : 'center'}),
        
        html.Div([
            html.H2(id = 'BAN5',
                    style= {'textAlign': 'center', 'color': 'red', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.H3('Red Cards per Match', 
                   style={'textAlign': 'center', 'color': 'red', 'fontFamily':'Alkes Regular Italic', 'fontSize':20})
            ], className = 'four columns', style = {'textAlign' : 'center'}),
        
        html.Div([
            html.H2(id = 'BAN6',
                    style= {'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':60}),
            html.H3('Average Age of Players', 
                   style={'textAlign': 'center', 'color': 'purple', 'fontFamily':'Alkes Regular Italic', 'fontSize':20}),
            ], className = 'four columns', style = {'textAlign' : 'center'}),
    
        ], className = 'row'),
    
    html.Div([
        html.Div([
            
            dcc.Graph(id='top_scoring_players', figure = px.bar())
                 
            ],'Div5', className = 'four columns', style = {'textAlign' : 'center'}),
        html.Div([
                dcc.Graph(id = 'goals_vs_assists', figure = px.scatter())
            
            ],'Div7', className = 'four columns'),
        
        html.Div([
                dcc.Graph(id = 'starts_vs_goals', figure = px.scatter())
            
            ],'Div8', className = 'four columns')
        
        ], className = 'row', style={'padding':'15px'}),
    
    html.Div([
        
        html.Div([
                dcc.Graph(id='Most_Nationality', figure = px.pie())
            ],'Div6', className = 'five columns', style = {'textAlign' : 'center'}),
        
        html.Div([
            
            dcc.Graph(id='goals_per_club', figure = px.bar())
                 
            ],'Div9', className = 'seven columns')
        
        ], className = 'row')
        
        ])


app.run_server()
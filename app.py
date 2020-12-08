# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 13:35:46 2020

@author: Suyog
"""

from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime , timedelta
from plotly.subplots import make_subplots


 
st.title('Data Science Home Assignment  TY-52 ')
st.write()
st.write()

df = pd.read_csv("complete.csv")
df1 = pd.read_csv("AgeGroupDetails.csv")
p_df = pd.read_csv("patients_data.csv")

# Color pallette
cnf = '#393e46' # confirmed - grey
dth = '#ff2e63' # death - red
rec = '#21bf73' # recovered - cyan
act = '#fe9801' # active case - yellow

st.sidebar.header("Covid-19 Analysis")
st.sidebar.write('')
st.sidebar.write('')
slct = st.sidebar.selectbox("Data Science",("Show Dataset","Data Visualization"))
if slct == "Show Dataset":
    st.header("Age Group Details")
    st.write(df1)
    st.write()
    st.write()
    st.header("Patient Details")
    st.write(p_df)
    st.write()
    st.write()    
    st.header("Statewise Details")
    st.write(df)
    st.write()
    st.write()
if slct == "Data Visualization":

    st.write('')
    st.write('')
    st.header("Covid 19 Timeline")
    st.markdown("""<html>
                    <div class="flourish-embed flourish-cards" data-url="https://flo.uri.sh/visualisation/1786965/embed">
                    <script src="https://public.flourish.studio/resources/embed.js"></script>
                    </div>
                    <iframe src='https://flo.uri.sh/visualisation/1786965/embed' title='Interactive or visual content' frameborder='0' scrolling='no' style='width:100%;height:300px;'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/1786965/?utm_source=embed&utm_campaign=visualisation/1786965' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>
                    </html>
                    """,unsafe_allow_html=True)
    
    
    #patient.csv
    
    p_df = pd.read_csv("patients_data.csv")
    # fixing date format
    p_df['date_announced'] = pd.to_datetime(p_df['date_announced'], format='%d/%m/%Y')
    p_df['status_change_date'] = pd.to_datetime(p_df['status_change_date'], format='%d/%m/%Y')
    
    # fixing nationality values
    p_df['nationality'] = p_df['nationality'].replace('Indian', 'India')
    
    
    #complete.csv
    
    
    # Replacing 'union territory' with ''
    df['Name of State / UT'] = df['Name of State / UT'].str.replace('Union Territory of ', '')
    
    # Rearranging columns
    df = df[['Date', 'Name of State / UT', 'Latitude', 'Longitude', 'Total Confirmed cases', 'Death', 'Cured/Discharged/Migrated']]
    
    # Renaming columns
    df.columns = ['Date', 'State/UT', 'Latitude', 'Longitude', 'Confirmed', 'Deaths', 'Cured']
    
    # Fixing datatype
    for i in ['Confirmed', 'Deaths', 'Cured']:
        df[i] = df[i].astype('int')
        
    # Derived columns
    df['Active'] = df['Confirmed'] - df['Deaths'] - df['Cured']
    df['Mortality rate'] = df['Deaths']/df['Confirmed']
    df['Recovery rate'] = df['Cured']/df['Confirmed']
    
    # Rearranging columns
    df = df[['Date', 'State/UT', 'Latitude', 'Longitude', 'Confirmed', 'Active', 'Deaths', 'Mortality rate', 'Cured', 'Recovery rate']]
    ####
    st.header("Timeline of confirmation of cases in India")
    temp = df[df['Date']>='2020-03-15']
    fig = px.line(temp,x='Date', y='Confirmed',color='State/UT')
    fig.update_layout(xaxis_title='Date', yaxis_title='Confirmed cases')
    
    fig.add_trace(go.Scatter(x=temp['Date'], y=[500]*len(temp), 
                              mode='lines', name='500 count line', 
                              line = dict(dash='dash',color='gray')))
    
    fig.add_trace(go.Scatter(x=temp['Date'], y=[1000]*len(temp), 
                              mode='lines', name='1000 count line', 
                              line = dict(dash='dash',color='maroon')))
    
    fig.add_trace(go.Scatter(x=temp['Date'], y=[1500]*len(temp), 
                              mode='lines', name='1000 count line', 
                              line = dict(dash='dash',color='black')))
    st.plotly_chart(fig)
    
    ####
    st.header("State wise cases over time")
    fig = px.bar(df.sort_values('Confirmed', ascending=False), x="Date", y="Confirmed", color='State/UT',
                 color_discrete_sequence = px.colors.qualitative.Vivid)
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
    
    ####
    st.header("Spread of covid 19")
    temp = df.copy()
    temp = temp[temp['Date']>='2020-03-15']
    fig = px.scatter_geo(temp, lat="Latitude", lon="Longitude", color='Confirmed', size='Confirmed', projection="natural earth",
                         hover_name="State/UT", scope='asia', animation_frame="Date", center={'lat':20, 'lon':78}, 
                         range_color=[0, max(temp['Confirmed'])])
    st.plotly_chart(fig)
        
    ####
    st.header("No. of affected States / Union Territory")

    no_of_states = df.groupby('Date')['State/UT'].unique().apply(len).values
    dates = df.groupby('Date')['State/UT'].unique().apply(len).index
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=dates, y=[36 for i in range(len(no_of_states))], 
                             mode='lines', name='Total States+UT', 
                             line = dict(dash='dash',color=dth)))
    
    fig.add_trace(go.Scatter(x=dates, y=no_of_states, hoverinfo='x+y',
                             mode='lines', name='No. of affected States+UT',
                             line = dict(color=cnf)))
    
    fig.update_layout(xaxis_title='Date', yaxis_title='No. of affected States / Union Territory')
    fig.update_traces(textposition='top center')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
    
    ############################
    st.header("Statewise Data")
    # Latest data
    latest = df[df['Date']==max(df['Date'])]
    # days
    latest_day = max(df['Date'])
    latest_day = datetime.strptime(latest_day,'%Y-%m-%d').date()
    #birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y').date()
        
    #st.write(type(latest_day))
    day_before = latest_day - timedelta(days = 1)
    #st.write(day_before)
    #st.write(type(df.Date))
    latest_day_df = df[df['Date']==str(latest_day)].set_index('State/UT')
    #st.write(latest_day_df)
    #st.write(type(day_before))
    
    day_before_df = df[df['Date']==str(day_before)].set_index('State/UT')
    #st.write(day_before_df)
    
    # Merging data 
    temp = pd.merge(left = latest_day_df, right = day_before_df, on='State/UT', suffixes=('_lat', '_bfr'), how='outer')
    #st.write(temp)
    
    
    # New cases
    latest_day_df['New cases'] = temp['Confirmed_lat'] - temp['Confirmed_bfr']
    #st.write(latest_day_df)
    
    # Reset index
    latest = latest_day_df.reset_index()
    
    # filling na
    latest.fillna(1, inplace=True)
    #st.write(latest)
    ####
    temp = latest[['State/UT', 'Confirmed', 'Active', 'New cases', 'Deaths', 'Mortality rate', 'Cured', 'Recovery rate']]
    temp = temp.sort_values('Confirmed', ascending=False).reset_index(drop=True)
    #st.write(temp)
    st.dataframe(temp.style\
        .background_gradient(cmap="Blues", subset=['Confirmed', 'Active', 'New cases'])\
        .background_gradient(cmap="Greens", subset=['Cured', 'Recovery rate'])\
        .background_gradient(cmap="Reds", subset=['Deaths', 'Mortality rate']))
    
    #####
    st.header("Spread of the virus among different states")
    fig = px.pie(temp, values='Confirmed', names='State/UT', color= 'Confirmed',
                 color_discrete_sequence=px.colors.sequential.amp,  height=600)
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.show(renderer='colab')
    st.plotly_chart(fig)
    
    ####
    st.header("Cases over time")

    temp = df.groupby('Date')['Cured', 'Deaths', 'Active'].sum().reset_index()
    temp = temp.melt(id_vars="Date", value_vars=['Cured', 'Deaths', 'Active'],
                     var_name='Case', value_name='Count')
    temp.head()
    
    fig = px.bar(temp, x="Date", y="Count", color='Case', height=540, color_discrete_sequence = [rec, dth, act])
    st.plotly_chart(fig)
    
    #####
    st.header("Statewise Statistics")
    fig_c = px.bar(latest.sort_values('Confirmed').tail(15), x="Confirmed", y="State/UT", 
                   text='Confirmed', orientation='h', color_discrete_sequence = [act])
    fig_d = px.bar(latest.sort_values('Deaths').tail(15), x="Deaths", y="State/UT", 
                   text='Deaths', orientation='h', color_discrete_sequence = [dth])
    fig_r = px.bar(latest.sort_values('Cured').tail(15), x="Cured", y="State/UT", 
                   text='Cured', orientation='h', color_discrete_sequence = [rec])
    fig_a = px.bar(latest.sort_values('Active').tail(15), x="Active", y="State/UT", 
                   text='Active', orientation='h', color_discrete_sequence = ['#333333'])
    
    
    fig = make_subplots(rows=2, cols=2, shared_xaxes=False, horizontal_spacing=0.3, vertical_spacing=0.08,
                        subplot_titles=('Confirmed cases', 'Deaths reported', 'Recovered', 'Active cases'))
    
    fig.add_trace(fig_c['data'][0], row=1, col=1)
    fig.add_trace(fig_d['data'][0], row=1, col=2)
    fig.add_trace(fig_r['data'][0], row=2, col=1)
    fig.add_trace(fig_a['data'][0], row=2, col=2)
    
    fig.update_layout(height=1200)
    st.plotly_chart(fig)
    
    ####
    st.header("Gender vs Age")
    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.8, 0.2],
        specs=[[{"type": "histogram"}, {"type": "pie"}]]
    )
    
    temp = p_df[['age_bracket', 'gender']].dropna()
    gen_grp = temp.groupby('gender').count()
    
    fig.add_trace(go.Histogram(x=temp[temp['gender']=='F']['age_bracket'], nbinsx=50, name='Female', marker_color='#6a0572'), 1, 1)
    fig.add_trace(go.Histogram(x=temp[temp['gender']=='M']['age_bracket'], nbinsx=50, name='Male', marker_color='#39065a'), 1, 1)
    
    fig.add_trace(go.Pie(values=gen_grp.values.reshape(-1).tolist(), labels=['Female', 'Male'], marker_colors = ['#6a0572', '#39065a']),1, 2)
    
    fig.update_layout(showlegend=False)
    fig.update_layout(barmode='stack')
    fig.data[2].textinfo = 'label+text+value+percent'
    st.plotly_chart(fig)
    
    #####
    st.header("Cases vs Age")
    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.8, 0.2],
        specs=[[{"type": "histogram"}, {"type": "pie"}]]
    )
    
    temp = p_df[['age_bracket', 'current_status']].dropna()
    gen_grp = temp.groupby('current_status').count()
    
    fig.add_trace(go.Pie(values=gen_grp.values.reshape(-1).tolist(), labels=['Deceased', 'Hospitalized', 'Recovered'], 
                         marker_colors = ['#fd0054', '#393e46', '#40a798'], hole=.3),1, 2)
    
    fig.add_trace(go.Histogram(x=temp[temp['current_status']=='Deceased']['age_bracket'], nbinsx=50, name='Deceased', marker_color='#fd0054'), 1, 1)
    fig.add_trace(go.Histogram(x=temp[temp['current_status']=='Recovered']['age_bracket'], nbinsx=50, name='Recovered', marker_color='#40a798'), 1, 1)
    fig.add_trace(go.Histogram(x=temp[temp['current_status']=='Hospitalized']['age_bracket'], nbinsx=50, name='Hospitalized', marker_color='#393e46'), 1, 1)
    
    fig.update_layout(showlegend=False)
    fig.update_layout(barmode='stack')
    fig.data[0].textinfo = 'label+text+value+percent'    
    st.plotly_chart(fig)
    
    ####
    st.header('No. of foreign citizens')
    temp = p_df.groupby('nationality')['patient_number'].count().reset_index()
    temp = temp.sort_values('patient_number')
    temp = temp[temp['nationality']!='India']
    fig = px.bar(temp, x='patient_number', y='nationality', orientation='h', text='patient_number', width=600,
           color_discrete_sequence = [cnf])
    fig.update_xaxes(title='')
    fig.update_yaxes(title='')
    fig.show(renderer='colab')
    st.plotly_chart(fig)
    
    ###########
    st.header('Travel History of Patients')
    p_df['notes'] = p_df['notes'].replace('Details Awaited', 'Details awaited')
    p_df['notes'] = p_df['notes'].replace('Travelled from Dubai, UAE', 'Travelled from Dubai')
    p_df['notes'] = p_df['notes'].replace('attended religious event Tablighi Jamaat in delhi', 'Attended Delhi Religious Conference')
    p_df['notes'] = p_df['notes'].replace('Travelled from London', 'Travelled from UK')
    p_df['notes'] = p_df['notes'].replace('Travelled from Dubai.', 'Travelled from Dubai')
    temp = pd.DataFrame(p_df.groupby('notes')['notes'].count().sort_values(ascending=False))
    temp.columns = ['Count']
    temp = temp.reset_index()
    temp = temp[temp['notes']!='Details awaited']
    
    fig = px.bar(temp.head(10).sort_values('Count', ascending=True), x='Count', y='notes', orientation='h', text='Count',color='Count', 
                 range_color=[0,150],color_continuous_scale='amp')
    fig.update_xaxes(title='Cases')
    fig.update_yaxes(title='Travel History')
    st.plotly_chart(fig)

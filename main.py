import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
st.set_page_config( layout='wide')
from datetime import datetime, timedelta,date
plt.grid(False)
plt.style.use('ggplot')
import streamlit_theme as stt
stt.set_theme('dark')


st.markdown(
        f"""

<style>

    .reportview-container .main .block-container{{
        max-width: 10000px;
        padding-top: 5rem;
        
        padding-left: 4rem;
        padding-bottom: 10rem;
    }}
    .reportview-container .main {{
        background:black
        background-color: black;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

pd.options.display.float_format = '{:,.1f}'.format
st.markdown("<span style=“background-color:#121922”>",unsafe_allow_html=True)
df=pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
df.rename(columns={'Daily Confirmed':'Confirmed_Cases','Daily Recovered':'Recovered_Cases','Daily Deceased':'Deceased_Cases'},inplace=True)
df['Active_Cases']=df['Confirmed_Cases']-(df['Recovered_Cases']+df['Deceased_Cases'])
st.sidebar.title("COVID19 DASHBOARD")
st.sidebar.markdown("Select the Charts/Plots accordingly:")
select = st.sidebar.selectbox('COVID19 : ', ['HOME','INDIA','STATES','VACCINATION','INDIA vs WORLD'], key='1')


state_df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
state_df['Date'] = state_df.Date.apply(lambda x: pd.to_datetime(x).strftime('%d-%m-%Y'))
state_df.rename(columns={'AN': 'Andaman Nicobar', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam',
                                 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chattisgarh', 'DD': 'Daman & Diu', 'DL': 'Delhi',
                                 'GA': 'Goa', 'GJ': 'Gujarat',
                                 'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JK': 'Jammu And Kashmir', 'KA': 'Karnataka',
                                 'KL': 'Kerela',
                                 'LA': 'Ladakh', 'MP': 'Madhya Pradesh', 'MH': 'Maharashtra', 'MN': 'Manipur',
                                 'ML': 'Meghalaya',
                                 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Orissa', 'PY': 'Puducherry', 'PB': 'Punjab',
                                 'RJ': 'Rajasthan',
                                 'SK': 'Sikkim', 'TN': 'Tamil Nadu', 'TG': 'Telegana', 'TR': 'Tripura',
                                 'UP': 'Uttar Pradesh',
                                 'UT': 'Uttarakhand',
                                 'WB': 'West Bengal', 'TT': 'Total'}, inplace=True)

top_affected = state_df.loc[state_df['Status'] == 'Confirmed']
top_affected = top_affected.iloc[:, 3:-1]
top_affected = top_affected.reset_index()
top_affected.drop(['index'], axis=1, inplace=True)
confirmed = top_affected.sum(axis=0)
confirmed_df = pd.DataFrame(confirmed, columns=['Confirmed Cases'])

recovered_state = state_df.loc[state_df['Status'] == 'Recovered']
recovered_state = recovered_state.iloc[:, 3:-1]
recovered_state = recovered_state.reset_index()
recovered_state.drop(['index'], axis=1, inplace=True)
recovered = recovered_state.sum(axis=0)
recovered_df = pd.DataFrame(recovered, columns=['Recovered Cases'])

final_part1 = confirmed_df.merge(recovered_df, left_index=True, right_index=True)
deceased_state = state_df.loc[state_df['Status'] == 'Deceased']
deceased_state = deceased_state.iloc[:, 3:-1]
deceased_state = deceased_state.reset_index()
deceased_state.drop(['index'], axis=1, inplace=True)
deceased = deceased_state.sum(axis=0)
deceased_df = pd.DataFrame(deceased, columns=['Deceased Cases'])

final_df = final_part1.merge(deceased_df, left_index=True, right_index=True)
final_df['Active Cases'] = final_df['Confirmed Cases'] - (final_df['Recovered Cases'] + final_df['Deceased Cases'])
final_df.index.name = 'State'
final_df1 = final_df.drop(final_df.index[0])
st.title("INDIA'S CURRENT COVID19 STATUS")
st.markdown(' ')
a1,a2,a3,a4=st.beta_columns((1,1,1,1))
a1.markdown('TOTAL ACTIVE CASES')
a1.info('{:,}'.format(final_df.iloc[0, 3]))
a2.markdown('TOTAL CONFIRMED CASES')
a2.info('{:,}'.format(final_df.iloc[0,0]))
a3.markdown('TOTAL RECOVERED CASES')
a3.info('{:,}'.format(final_df.iloc[0, 1]))
a4.markdown('TOTAL DECEASED CASES')
a4.info('{:,}'.format(final_df.iloc[0, 2]))
st.markdown(' ')


if select=='INDIA':
    st.title("COVID19:-  LETS FIGHT TOGETHER AS ONE TEAM ")
    st.markdown('The dashboard will visualize the Covid-19 Situation in India')
    st.markdown(
        'Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.')
    expanded_bar=st.beta_expander('About')
    expanded_bar.markdown('CONFIRMED CASES : People who got affected by COVID19')
    expanded_bar.markdown('RECOVERED CASES : People who got recovered by COVID19')
    expanded_bar.markdown('DECEASED CASES : People who died due to COVID19')
    expanded_bar.markdown('ACTIVE CASES : People who currently have COVID19')
    st.markdown('    ')

    col1, col2 = st.beta_columns((1.5, 1.5))
    col1.markdown('COVID19 in India')

    col1.dataframe(final_df1, width=800, height=1000)

    final_df1['State']=final_df1.index


    india_fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
    indiaChart1 = go.Bar(x=final_df1['State'],y=final_df1['Confirmed Cases'],name='Confirmed Cases')
    indiaChart2 = go.Bar(x=final_df1['State'], y=final_df1['Recovered Cases'], name='Recovered Cases')
    indiaChart3 = go.Bar(x=final_df1['State'], y=final_df1['Active Cases'], name='Active Cases')
    indiaChart4 = go.Bar(x=final_df1['State'], y=final_df1['Deceased Cases'], name='Deceased Cases')
    india_fig.add_traces(indiaChart3, 1, 1)
    india_fig.add_traces(indiaChart1, 2, 1)
    india_fig.add_traces(indiaChart2, 3, 1)
    india_fig.add_traces(indiaChart4, 4, 1)
    india_fig.update_layout(height=1500, width=850)
    col2.plotly_chart(india_fig)



    col1.markdown(' ')
    col1.markdown('The Pie chart shows you haw much percentage of people are currently having COVID19 in comparison with different aspects')
    pie_expand=col1.beta_expander('INFORMATION')
    pie_expand.markdown('The active case percentage is calculated in the following manner:')
    pie_expand.markdown('Active Cases Percentage=(Total Active Cases * 100)/Total Confirmed Case ')
    pie_expand.markdown('The rest type of Cases are calculated similarly')

    colors = ['plum', 'navyblue', 'greenyellow']
    names = ['Deceased Cases', 'Active Cases', 'Recovered Cases']
    pie_graph = go.Pie(values=[df['Deceased_Cases'].sum(), df['Active_Cases'].sum(), df['Recovered_Cases'].sum()],
                       labels=names,
                       hole=.2)
    layout = go.Layout(height=500, width=700)
    figure = go.Figure(data=pie_graph, layout=layout)
    figure.update_traces(textinfo='percent+label', textfont_size=18,
                         marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    col1.plotly_chart(figure)
    pd.options.display.float_format = '{:,.1f}'.format
    df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
    df.rename(columns={'Daily Confirmed': 'Confirmed_Cases', 'Daily Recovered': 'Recovered_Cases',
                       'Daily Deceased': 'Deceased_Cases'}, inplace=True)
    df['Active_Cases'] = df['Confirmed_Cases'] - (df['Recovered_Cases'] + df['Deceased_Cases'])

    abc = df.iloc[:, [0, 2, 4, 6, 8]]


    def color_negative(value):
        if value > 0:
            color = 'red'
        elif value < 0:
            color = 'blue'
        else:
            color = 'grey'
        return 'color: %s' % color


    abc=abc.style.applymap(color_negative, subset=['Active_Cases'])


    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### ** Download output CSV File **')
    href = f'<a href="https://api.covid19india.org/csv/latest/state_wise_daily.csv">State Wise Data</a> '
    st.markdown(href, unsafe_allow_html=True)




elif select=='HOME':
    st.title("COVID19:-  LETS FIGHT TOGETHER AS ONE TEAM")
    st.markdown(' ')
    st.markdown(' ')


    st.markdown('The dashboard will visualize the Covid-19 Situation in India')
    st.markdown('From the chart, you can clearly see that from 20th NOV, 2020, there started a downfall in the number '
                        'of COVID CASES as there was LOCKDOWN in many states, but as LOCKDOWN & RESTRICTION were slowly removed,'
                        ' there again started the rise of COVID19 CASES from the mid of FEB,2021.')
    st.markdown(' The period between NOV, 2020 - '
                        ' FEB, 2021 saw the decrement in CONFIRMED CASES, but now the condition is exactly the opposite.')
    df=df.tail(150)
    graph1 = go.Scatter(x=df['Date'],y=df['Confirmed_Cases'],name='Confirmed Cases',mode='markers+lines')
    graph2 = go.Scatter(x=df['Date'], y=df['Recovered_Cases'], name='Recovered Cases',mode='markers+lines')
    graph3 = go.Scatter(x=df['Date'], y=df['Deceased_Cases'], name='Deceased Cases',mode='markers+lines')
    data=[graph3,graph1,graph2]
    layout=go.Layout(height=500,width=850,title='DAILY TRACKER',xaxis=dict(showgrid=False))

    figure1=go.Figure(data=data,layout=layout)
    figure1.update_xaxes(nticks=30)
    figure1=figure1.update_layout(
                        title={
                            'y': 0.9,
                            'x': 0.5,
                            'xanchor':'center',
                            'yanchor':'top'
                        }
                    )
    figure1.update_layout(height=700, width=1650)

    st.plotly_chart(figure1)
    st.title(' TIME SERIES')
    st.markdown('In the following figure you can figure out how much cases were reported on a particular data just by hovering your mouse pointer'
                ' on the bar chart. You can select the number of days from the drop-down list')

    no_of_days = st.selectbox('DAYS', [ '30 DAYS', '10 DAYS', '2 MONTHS','4 MONTHS', '6 MONTHS', '8 MONTHS'],
                                      key=2)
    home_col1, home_col2 = st.beta_columns((1, 1.2))
    home_col1.title(' ')
    home_col1.title(' ')

    if no_of_days == '4 MONTHS':
        df = df.tail(120)
    elif no_of_days == '10 DAYS':
        df = df.tail(10)

    elif no_of_days == '30 DAYS':
        df = df.tail(30)
    elif no_of_days == '2 MONTHS':
        df = df.tail(60)

    elif no_of_days == '6 MONTHS':
        df = df.tail(180)
    elif no_of_days == '8 MONTHS':
        df = df.tail(240)


    image11 = Image.open('Timeline_project.jpg')
    home_col1.image(image11, caption='Timeline', width=600)

    df = df.tail(105)
    fig = make_subplots(rows=4, cols=1)

    data1 = go.Bar(x=df['Date'], y=df['Confirmed_Cases'], name='Confirmed Cases')
    data2 = go.Bar(x=df['Date'], y=df['Recovered_Cases'], name='Recovered Cases')
    data3 = go.Bar(x=df['Date'], y=df['Active_Cases'], name='Active Cases')
    data4 = go.Bar(x=df['Date'], y=df['Deceased_Cases'], name='Deceased Cases')

    fig.add_trace(data3, 1, 1)
    fig.add_trace(data1, 2, 1)
    fig.add_trace(data2, 3, 1)
    fig.add_trace(data4, 4, 1)
    fig.update_xaxes(nticks=8,tickangle=20)
    fig.update_layout(height=1500, width=900)
    home_col2.plotly_chart(fig)
    col1, col2 = st.beta_columns([.5, 1])
    csv=df.to_csv(index=False)
    b64=base64.b64encode(csv.encode()).decode()
    st.markdown(" ")
    st.markdown(' ')
    st.markdown('### **Download CSV File**')
    href = f'<a href="https://api.covid19india.org/csv/latest/case_time_series.csv">Case Time Series</a> '
    st.markdown(href, unsafe_allow_html=True)









elif select=='STATES':

        option=st.sidebar.selectbox('SELECT STATE ', ['Maharashtra','Andaman Nicobar', 'Andhra Pradesh',  'Arunachal Pradesh', 'Assam',
                                 'Bihar', 'Chandigarh', 'Chattisgarh', 'Daman & Diu','Delhi',
                                 'Goa', 'Gujarat',
                                  'Haryana', 'Himachal Pradesh',  'Jammu And Kashmir', 'Karnataka',
                                 'Kerela',
                                 'Ladakh', 'Madhya Pradesh',  'Manipur',
                                 'Meghalaya',
                                 'Mizoram', 'Nagaland', 'Orissa',  'Puducherry',  'Punjab',
                                 'Rajasthan',
                                  'Sikkim', 'Tamil Nadu', 'Telegana',  'Tripura',
                                 'Uttar Pradesh',
                                  'Uttarakhand',
                                  'West Bengal'],key=1)
        final=final_df1.reset_index()

        final=final.loc[final['State']==option]

        st.title(str.upper(option))
        s1, s2 = st.beta_columns((1, 1))
        s1.write(' CONFIRMED CASES : ')
        s1.info('{:,}'.format(final.iat[0, 1]))
        s1.write(' RECOVERED CASES : ')
        s1.info('{:,}'.format(final.iat[0, 2]))
        s1.markdown(' ACTIVE CASES  : ')
        s1.info('{:,}'.format(final.iat[0, 4]))
        s1.write(' DECEASED CASES  : ')
        s1.info('{:,}'.format(final.iat[0, 3]))
        #st.write(' RECOVERED CASES PERCENTAGE : ')
        #st.info(final.iat[0,5])
        #st.markdown(' ACTIVE CASES PERCENTAGE : ')
        #st.info(final.iat[0, 6])
        #st.write(' DECEASED CASES PERCENTAGE : ')
        #st.info(final.iat[0, 7])

        state = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv ')





        state1 = state.loc[state['State'] == option][
                ['District', 'Confirmed', 'Recovered', 'Active', 'Deceased']]
        state1=state1.reset_index()
        state_fig = make_subplots(rows=4, cols=1, shared_xaxes=True)

        state_fig1 = go.Bar(x=state1['District'], y=state1['Confirmed'], name='Confirmed Cases')
        state_fig2 = go.Bar(x=state1['District'], y=state1['Active'], name='Active Cases')
        state_fig3 = go.Bar(x=state1['District'], y=state1['Recovered'], name='Recovered Cases')
        state_fig4 = go.Bar(x=state1['District'], y=state1['Deceased'], name='Deceased Cases')

        state_fig.add_trace(state_fig2, 1, 1)
        state_fig.add_trace(state_fig1, 2, 1)
        state_fig.add_trace(state_fig3, 3, 1)
        state_fig.add_trace(state_fig4, 4, 1)
        state_fig.update_layout(height=1500, width=950)

        c1, c2 = st.beta_columns((1.2, 1.5))
        c1.title('DISTRICT WISE')
        c1.markdown(' ')
        abcd = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv ')
        abcd = abcd.loc[abcd['State'] == option][
                ['District', 'Confirmed', 'Recovered', 'Active', 'Deceased']]


        c1.dataframe(abcd, width=1000, height=1400)
        label11 = ['Recovered Cases', 'Active Cases', 'Deceased Cases']
        state_color=['beige','lightskyblue','peachpuff']
        state_pie = go.Pie(values=[final.iat[0, 2], final.iat[0, 4], final.iat[0, 3]], labels=label11,hole=0.2)
        pie_layout = go.Layout(height=530, width=800)

        pie_fig = go.Figure(data=state_pie, layout=pie_layout)
        pie_fig.update_traces(textinfo='percent+label', textfont_size=18,
                             marker=dict(colors=state_color,line=dict(color='#000000', width=1)))
        s2.plotly_chart(pie_fig)
        c2.plotly_chart(state_fig)



elif select=='VACCINATION':
    vaccinated_dframe = pd.read_csv('http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv')
    column_list = list(vaccinated_dframe)

    vaccinated_df = vaccinated_dframe.iloc[:-2]
    col_vaccine=vaccinated_df.iloc[:,-2]
    fig12 = px.bar(x=vaccinated_df['State'], y=col_vaccine, color=col_vaccine)
    fig12.update_layout(height=800,width=1500)
    st.title('VACCINATION IN INDIA')
    st.markdown("On 16 January 2021 India started its national vaccination programme against the SARS-CoV-2 virus which has caused the COVID-19 pandemic. "
                "The drive prioritises healthcare and frontline workers, "
                "and then those over the age of 60, and then those over the age of 45 and suffering from certain comorbidities. "
                "In January 2021 S"
                "ecretary-General of the United Nations António Guterres said that India's vaccine-production capacity is the "
                "best asset the world has.")
    vaccinated_df['Total_Statedata']=vaccinated_df.iloc[:,-2]
    vaccinated_df1=vaccinated_df.sort_values(by='Total_Statedata',ascending=False)
    total_vaccination=vaccinated_dframe .iloc[-1,-2]
    highest_state=vaccinated_df1.iloc[0,0]
    lowest_state=vaccinated_df1.iloc[-1,0]

    st.write('TOTAL VACCINATION DONE IN INDIA')
    st.info('{:,}'.format(total_vaccination))
    a1, a2 = st.beta_columns((1, 1))
    a1.write('STATE/TERRITORY HAVING HIGHEST NUMBER OF VACCINATION DONE : ')
    a1.info(highest_state)
    a2.write('STATE/TERRITORY HAVING LOWEST NUMBER OF VACCINATION DONE : ')
    a2.info(lowest_state)
    st.plotly_chart(fig12)
    st.title('VACCINATION DATE WISE')
    st.write()
    st.markdown('With the help of following dataframe, you can view how much INDIVIDUALS were vaccinated till that date. The only thing you need to'
                'do is to select the specific date of which you want to view')
    ad=st.date_input("DATE")
    ad=str(ad)
    datetimeobject = datetime.strptime(ad, '%Y-%m-%d')

    newformat = datetimeobject.strftime('%d/%m/%Y')
    d1=date.today()-timedelta(days=1)
    da=d1.strftime('%d/%m/%Y')
    st.info(da)
    vaccinated_df111 = pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv')
    vaccinated_df11 = vaccinated_df111.loc[vaccinated_df111['Updated On'] == da]
    b1,b2,b3=st.beta_columns((1,1,1))
    b1.write('Male Individuals Vaccinated in India')
    b1.info('{:,}'.format(vaccinated_df11.iloc[0, 7]))
    b2.write('Female Individuals Vaccinated in India')
    b2.info('{:,}'.format(vaccinated_df11.iloc[0, 8]))
    b3.write('Transgender Individuals Vaccinated in India')
    b3.info('{:,}'.format(vaccinated_df11.iloc[0, 9]))
    vaccinated_df1=vaccinated_df1.reset_index()
    st.dataframe(vaccinated_df11[['State','Male(Individuals Vaccinated)','Female(Individuals Vaccinated)','Transgender(Individuals Vaccinated)','Total Individuals Vaccinated']],height=1000)
    plot1=px.bar(x=[vaccinated_df11['Male(Individuals Vaccinated)'],vaccinated_df11['Female(Individuals Vaccinated)']])

elif select=='INDIA vs WORLD':
    world_df = pd.read_csv(r'https://covid19.who.int/WHO-COVID-19-global-table-data.csv')
    world_confirmedsum = world_df['Cases - cumulative total'].sum()
    world_deathsum = world_df['Deaths - cumulative total'].sum()
    st.title("WORLD'S COVID19 STATUS")
    w1,w2=st.beta_columns((1,1))
    w1.markdown('TOTAL AFFECTED CASES')
    w1.info('{:,}'.format(world_df.loc[0,'Cases - cumulative total']))
    w2.markdown('TOTAL DEATH NUMBER')
    w2.info('{:,}'.format(world_df.loc[0,'Deaths - cumulative total']))
    sort1 = world_df.sort_values(by='Cases - cumulative total', ascending=False)
    sort1 = sort1.head(6)
    sort1 = sort1.iloc[1:]
    worldconfbar = px.bar(sort1,x='Name', y='Cases - cumulative total',labels={'Name':'Country','Cases - cumulative total':'Total Cases'},width=800,height=500,title='Top 5 Country having Highest Affected Cases')
    abcd1 = world_df.groupby(['WHO Region'])['Cases - cumulative total'].sum()
    abcd1=abcd1.to_frame()
    abcd1=abcd1.reset_index()
    pie_label=abcd1['WHO Region'].tolist()
    world_pie=px.pie(abcd1,values='Cases - cumulative total',names='WHO Region',width=800,height=500,title='Region wise COVID19 Affected Pie Chart')
    w1.plotly_chart(worldconfbar)
    w2.plotly_chart(world_pie)

    world_df1=world_df.iloc[1:15]
    world_bar=px.bar(world_df1,x='Name',y='Cases - newly reported in last 24 hours',height=600,width=850,title='Cases in last 24 hours',labels={'Name':'Country','Cases - newly reported in last 24 hours':'Number of Cases'})
    w1.plotly_chart(world_bar)

    world_df1 = world_df.iloc[1:15]
    world_bar = px.bar(world_df1, x='Name', y='Cases - newly reported in last 7 days', height=600, width=850,
                       title='Cases in last 7 days',
                       labels={'Name': 'Country', 'Cases - newly reported in last 7 days': 'Number of Cases'})
    w2.plotly_chart(world_bar)
    w1.title(' ')
    w2.title(' ')
    st.markdown("India's Account for Total Affected Cases in World ")
    india_percent = (world_df.loc[2, 'Cases - cumulative total'] * 100) / world_df.loc[0, 'Cases - cumulative total']
    st.info('{:,}'.format(round(india_percent)) + '% ')

    w1.markdown("India's Cases - cumulative total per 1,00,000 population")
    cum_total=world_df.loc[2,'Cases - cumulative total per 100000 population']
    w1.info('{:,}'.format(cum_total))

    w2.markdown("India's Deaths - cumulative total per 1,00,000 population")
    cum_death_total = world_df.loc[2, 'Deaths - cumulative total per 100000 population']
    w2.info('{:,}'.format(cum_death_total))
st.sidebar.title('STAY HOME | STAY SAFE ')
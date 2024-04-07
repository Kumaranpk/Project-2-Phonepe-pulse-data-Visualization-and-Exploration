import os
import json
import requests
import pandas as pd
import mysql.connector as mysql
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu


#connect sql with python and create database
mydb = mysql.connect(
    host = "127.0.0.1",
    user = "root",
    password = "sqlroot",
    database = "Capstone_2"
)

cursor = mydb.cursor(buffered=True)

#aggregated transaction table
table_query_1 = "SELECT * FROM agg_transaction"
Agg_Transaction = pd.read_sql(table_query_1, mydb)

#aggregated user table
table_query_2 = "SELECT * FROM agg_user"
Agg_User = pd.read_sql(table_query_2, mydb)

#Map transaction table
table_query_3 = "SELECT * FROM map_transaction"
Map_Transaction = pd.read_sql(table_query_3, mydb)

# MAP USER table
table_query_4 = "SELECT * FROM map_users"
Map_User = pd.read_sql(table_query_4, mydb)

#Top transaction table
table_query_5 = "SELECT * FROM top_transaction"
Top_Transaction = pd.read_sql(table_query_5, mydb)

#Top user table
table_query_6 = "SELECT * FROM top_user"
Top_User = pd.read_sql(table_query_6, mydb)


def transaction_count_amount_y(df, yrs):
    tacy = df[df['Year'] == yrs]
    tacy.reset_index(drop= 'index', inplace= True)

    tacyg = tacy.groupby('State')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x='State', y='Transaction_amount', title= f'{yrs} TRANSACTION AMOUNT',
                            color_discrete_sequence= px.colors.sequential.Greens_r, height= 650, width= 600)

        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tacyg, x='State', y='Transaction_count', title= f'{yrs}TRANSACTION COUNT',
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)

        st.plotly_chart(fig_count)

    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{yrs} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{yrs} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return tacy

def transaction_count_amount_Q(df,qtr):
    tacq = df[df["Quater"] == qtr]
    tacq.reset_index(drop= True, inplace= True)

    tacqg = tacq.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    tacqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(tacqg, x= "State", y= "Transaction_amount", 
                            title= f"{tacq['Year'].min()} AND {qtr} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(tacqg, x= "State", y= "Transaction_count", 
                            title= f"{tacq['Year'].min()} AND {qtr} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(tacqg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (tacqg["Transaction_amount"].min(),tacqg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{tacq['Year'].min()} AND {qtr} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(tacqg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (tacqg["Transaction_count"].min(),tacqg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{tacq['Year'].min()} AND {qtr} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return tacq

def Agg_Transaction_type(df, state):
    df_state= df[df["State"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Agg_user_plot_1(df,year):
    aupy = df[df["Year"] == year]
    aupy.reset_index(drop= True, inplace= True)
    
    aupyg= pd.DataFrame(aupy.groupby("Brands")["Counts"].sum())
    aupyg.reset_index(inplace= True)

    fig_line_1= px.bar(aupyg, x="Brands",y= "Counts", title=f"{year} BRANDS AND COUNTS",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aupy

def Agg_user_plot_2(df,quater):
    aupq = df[df["Quater"] == quater]
    aupq.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=aupq, names= "Brands", values="Counts", hover_data= "Percentage",
                      width=1000,title=f"{quater} QUATER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return aupq

def Agg_user_plot_3(df,state):
    aups = df[df["State"] == state]
    aups.reset_index(drop= True, inplace= True)

    aupsg= pd.DataFrame(aups.groupby("Brands")["Counts"].sum())
    aupsg.reset_index(inplace= True)

    fig_scatter_1= px.line(aupsg, x= "Brands", y= "Counts", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_trans_plot_1(df,state):
    mtpbs = df[df["State"] == state]
    mtpbsg = mtpbs.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    mtpbsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(mtpbsg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(mtpbsg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_trans_plot_2(df,state):
    mtpps = df[df["State"] == state]
    mtppsg = mtpps.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    mtppsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(mtppsg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(mtppsg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    mupy = df[df["Year"] == year]
    mupy.reset_index(drop= True, inplace= True)
    mupyg = mupy.groupby("State")[["RegisteredUser", "AppOpens"]].sum()
    mupyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(mupyg, x= "State", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return mupy

def map_user_plot_2(df, quater):
    mupq= df[df["Quater"] == quater]
    mupq.reset_index(drop= True, inplace= True)
    mupqg= mupq.groupby("State")[["RegisteredUser", "AppOpens"]].sum()
    mupqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(mupqg, x= "State", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Year'].min()}, {quater} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return mupq

def map_user_plot_3(df, state):
    mups= df[df["State"] == state]
    mups.reset_index(drop= True, inplace= True)
    mupsg= mups.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    mupsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(mupsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(mupsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tupy= df[df["Year"] == year]
    tupy.reset_index(drop= True, inplace= True)

    tupyg= pd.DataFrame(tupy.groupby(["State","Quater"])["RegisteredUser"].sum())
    tupyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tupyg, x= "State", y= "RegisteredUser", barmode= "group", color= "Quater",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tupy

def top_user_plot_2(df,state):
    tups= df[df["State"] == state]
    tups.reset_index(drop= True, inplace= True)

    tupsg= pd.DataFrame(tups.groupby("Quater")["RegisteredUser"].sum())
    tupsg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tups, x= "Quater", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "Pincodes",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)


def ques1():
    brand= Agg_User[["Brands","Counts"]]
    brand1= brand.groupby("Brands")["Counts"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Counts", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Counts")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Agg_Transaction[["State", "Transaction_amount"]]
    lt1= lt.groupby("State")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "State", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_User[["State", "AppOpens"]]
    sa1= sa.groupby("State")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "State", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_User[["State", "AppOpens"]]
    sa1= sa.groupby("State")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "State", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Agg_Transaction[["State", "Transaction_count"]]
    stc1= stc.groupby("State")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "State", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Agg_Transaction[["State", "Transaction_count"]]
    stc1= stc.groupby("State")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "State", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Agg_Transaction[["State", "Transaction_amount"]]
    ht1= ht.groupby("State")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "State", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_Transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


#streamlit part

st.set_page_config(layout="wide")
st.title(':red[PHONEPE PULSE DATA VISUALIZATION & EXPLORATION]')

with st.sidebar:
    select = option_menu('Main menu',['DATA EXPLORATION','TOP CHARTS','ABOUT'])

if select == "ABOUT":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****1.Credit & Debit card linking****")
        st.write("****2.Bank Balance check****")
        st.write("****3.Money Storage****")
        st.write("****4.PIN Authorization****")
        st.write("****5.Easy Transactions****")
        st.write("****6.One App For All Your Payments****")
        st.write("****7.Your Bank Account Is All You Need****")
        st.write("****8.Multiple Payment Modes****")
        st.write("****9.PhonePe Merchants****")
        st.write("****10.Multiple Ways To Pay****")
        st.write("****-->Direct Transfer & More****")
        st.write("****-->QR Code****")
        st.write("****11.Earn Great Rewards****")
        st.write("****12.No Wallet Top-Up Required****")
        st.write("****13.Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****14.Instantly & Free****")

    st.subheader("****Project Description:****")
    st.write('''The project :red[PHONEPE PULSE DATA VISUALIZATION AND EXPORATION] helps to analyze large amount of data
             related to various metrics and statistcs which are all lively geo visualized and displays information and insights from the phonepe
             pulse github repositary in an interactive and visually appeaaling manner''')
    
    st.write('''Overall, This project will be a comprehensive and user_friendly solution for extracting, transforming,
             and visualizing data from the phonepe pulse github repository''')


if select == 'DATA EXPLORATION':
    tab1, tab2, tab3 = st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

    with tab1:
        button1 = st.radio('select the option',['Aggregated Transaction Analysis','Aggregated User Analysis'])

        if button1 == 'Aggregated Transaction Analysis':

            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox('select the year', Agg_Transaction['Year'].unique())
            df_agg_tran_Y = transaction_count_amount_y(Agg_Transaction, years)

            with col2:
                quaters = st.selectbox('select the Quater', Agg_Transaction['Quater'].unique())
            df_agg_tran_Y_Q = transaction_count_amount_Q(Agg_Transaction, quaters)

            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["State"].unique())

            Agg_Transaction_type(df_agg_tran_Y,state_Y_Q)

        elif button1 == 'Aggregated User Analysis':
            year_au= st.selectbox("Select the Year_AU",Agg_User["Year"].unique())
            agg_user_Y= Agg_user_plot_1(Agg_User,year_au)

            quater_au= st.selectbox("Select the Quater_AU",agg_user_Y["Quater"].unique())
            agg_user_Y_Q= Agg_user_plot_2(agg_user_Y,quater_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["State"].unique())
            Agg_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        button2 = st.radio('select the option',['Map Transaction Analysis','Map User Analysis'])

        if button2 == 'Map Transaction Analysis':
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.selectbox("**Select the Year_mt**", Map_Transaction["Year"].unique())

            df_map_tran_Y= transaction_count_amount_y(Map_Transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mt", df_map_tran_Y["State"].unique())

            map_trans_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quaters_m2= st.selectbox("**Select the Quater_mt**", df_map_tran_Y["Quater"].unique())

            df_map_tran_Y_Q= transaction_count_amount_Q(df_map_tran_Y, quaters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_mty", df_map_tran_Y_Q["State"].unique())            
            
            map_trans_plot_2(df_map_tran_Y_Q, state_m4)

        elif button2 == 'Map User Analysis':
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_User["Year"].unique())
            map_user_Y= map_user_plot_1(Map_User, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quater_mu1= st.selectbox("**Select the Quater_mu**",map_user_Y["Quater"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quater_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["State"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        button3 = st.radio('select the option',['Top Transaction Analysis','Top User Analysis'])

        if button3 == 'Top Transaction Analysis':
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.selectbox("**Select the Year_tt**", Top_Transaction["Year"].unique())
 
            df_top_tran_Y= transaction_count_amount_y(Top_Transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quaters_t2= st.selectbox("**Select the Quater_tt**", df_top_tran_Y["Quater"].unique())

            df_top_tran_Y_Q= transaction_count_amount_Q(df_top_tran_Y, quaters_t2)

        elif button3 == 'Top User Analysis':
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_User["Year"].unique())

            df_top_user_Y= top_user_plot_1(Top_User,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["State"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)

elif select == 'TOP CHARTS':
    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()


        
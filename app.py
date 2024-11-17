import streamlit as st
import pandas as pd
import plotly.express as px


#read in data 
data = pd.read_csv("vehicles_us.csv")


#Prelim EDA
#change date posted to datetime format
data["date_posted"] = pd.to_datetime(data["date_posted"], format = "%Y-%m-%d")

#split car make and model
def get_make(car):
    return car.split(' ')[0]

def get_model(car):
    info  = car.split(' ')
    return ' '.join(info[1:])

data['vehicle_make'] = data['model'].apply(get_make)
data['vehicle_model'] =  data['model'].apply(get_model)

#change certain columns to int type
data["cylinders"] =  data["cylinders"].fillna(0).astype("int")
data["is_4wd"] =  data["is_4wd"].fillna(0).astype("int")

#create data frames
df_suv = data[data["type"] == "SUV"]
df_truck = data[data["type"] == "truck"]
df_sedan = data[data["type"] == "sedan"]

#Crafting webpage
st.header("Welcome to Fast and Fueryous Used Cars!", divider = "orange")

#Number of cars at a certain price separated by make for SUVs
price_and_make_suv = px.histogram(df_suv, x ="price", nbins= 300, color = "vehicle_make")
price_and_make_suv.show()

#Number of cars at a certain price separated by make for Trucks
price_and_make_truck = px.histogram(df_truck, x ="price", nbins= 300, color = "vehicle_make")
price_and_make_truck.show()

#Number of cars at a certain price separated by make for Sedans
price_and_make_sedan = px.histogram(df_sedan, x ="price", nbins= 300, color = "vehicle_make")
price_and_make_sedan.show()

#model year vs color
aesthetic = px.histogram(data, x= "model_year", color= "paint_color")
aesthetic.show()

#model year vs number of miles on car by vehicle make
car_use = px.scatter(data, x="odometer", y= "model_year", color= "vehicle_make")
car_use.show()

#Activate Page
insurance = st.checkbox("I already have car insurance")
if insurance:
    st.header("Shop our most popular Vehicle Types!")
    st.write(price_and_make_suv)
    st.write(price_and_make_truck)
    st.write(price_and_make_sedan)
    st.header("Get A Car that matches your Style")
    st.write(aesthetic)
    st.header9("Get the Most Bang for Your Buck!")
    st.write(car_use)


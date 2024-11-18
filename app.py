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
st.header("Welcome to Fast & Feury-ous New & Used Cars!", divider = "orange")

#model type vs manufacturer
make_vs_type = px.histogram(data, x= "vehicle_make", color ="type", title = "Car Types by Vehicle Manufacturer", labels={"vehicle_make": "Manufacturer"} )
make_vs_type.update_layout(yaxis_title="Number of Cars Availible") 

#model year vs color
aesthetic = px.histogram(data, x= "model_year", color= "paint_color", title = "Car Color and Year", labels={"model_year": "Model Year"})
aesthetic.update_layout(yaxis_title="Number of Cars Availible") 

#model year vs number of miles on car by vehicle make
car_use = px.scatter(data, x="model_year", y= "odometer", color= "price", title = "Car Miles vs. Model Release Year by Price", labels={"model_year": "Model Year"})
car_use.update_layout(yaxis_title="Odometer Reading") 

#condition and type avaiable
condition = px.histogram(data, x="condition", y="price", histfunc= "avg", color= "type", title = "Price vs. Condition of Availbe Car Types", labels={"condition": "Condition"})
condition.update_layout(yaxis_title="Average Price") 

#Activate Page
insurance = st.checkbox("I have car insurance")
if insurance:
    looking = st.checkbox("I am looking to buy!")
    if looking:
        st.header("Explore Our Inventory", divider = "blue")
        st.plotly_chart(make_vs_type)
        st.header("Find A Car That Matches Your Style", divider = "blue")
        st.write(aesthetic)
        st.header("Get the Most Bang for Your Buck!", divider = "blue")
        st.write(car_use)
        st.plotly_chart(condition)


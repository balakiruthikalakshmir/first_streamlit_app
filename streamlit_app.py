import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit

st.title('My first streamlit title')
st.header('My first streamlit header')
st.text('My first streamlit text')
st.text('My second streamlit text')

st.header('Breakfast Menu')
st.text('Omega 3 & Blueberry Oatmeal')
st.text('Kale, Spinach & Rocket Smoothie')
st.text('Hard-Boiled Free-Range Egg')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)


st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("pls select a fruit to get information")
  else:
    #st.write('The user entered ', fruit_choice)
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #st.text(fruityvice_response.json())
    # takes the json version of response and normalize it
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_fuction = get_fruityvice_data(fruit_choice)
    # output it the data as table in screen
    st.dataframe(back_from_fuction)
except URLError as e:
  st.error()

st.header("fruit load list contains:")
if st.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#st.header("fruit load list contains:")
#st.dataframe(my_data_rows)


fruit_choice = st.text_input('What fruit would you like to add?')
if st.button('Add fruit to list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_fuction = insert_row_snowflake(fruit_choice)
    my_cnx.close()
    st.text(back_from_fuction)
#st.write('Thanks for adding ', fruit_choice)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

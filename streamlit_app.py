import streamlit
import snowflake.connector
from urllib.error import URLError
import pandas
import requests
streamlit.title('My parents new heathy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text ('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑  Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =my_fruit_list.set_index('Fruit')
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Grapes'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
#create the repeatable code (function)
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please select fruit to get information')
  else:
     back_from_function =get_fruitvice_data(fruit_choice)
     streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.header("Hello from Snowflake:")
streamlit.text(my_data_row)
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur2:
         my_cur2.execute("select * from fruit_load_list")
         return  my_cur2.fetchall()
streamlit.header("The fruit list contains:")
# Add a button to fruit load list
if streamlit.button('Get fruit load list'):
   my_data_rows = get_fruit_load_list()  
   streamlit.dataframe(my_data_rows)
# Allow end user to add fruit to list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur2:
     my_cur2.execute("insert into fruit_load_list values (new_fruit)")  
     return  "Thanks for adding" + new_fruit
fruit_add=streamlit.text_input('What fruit you like to add?)
back_from_function =insert_row_snowflake(insert_row_snowflake(new_fruit))
streamlit.text(back_from_function)

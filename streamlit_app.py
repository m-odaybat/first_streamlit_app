import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show) 

streamlit.header("Fruityvice Fruit Advice!")
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    streamlit.write("The user entered", fruit_choice)
    get_fruity_vice_data(fruit_choice)

except URLError as e:
  streamlit.error()


def get_fruity_vice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  #takes the json version of the response and normalizes it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return  streamlit.dataframe(fruityvice_normalized) #outputs the normalized data as a table on the screen
  
streamlit.stop()
# snowflake connector part
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice_2 = streamlit.text_input("What fruit would you like to add?", "jackfruit")
streamlit.write(f"Thanks for adding {fruit_choice_2}")

my_cur.execute("Insert INTO FRUIT_LOAD_LIST values ('from streamlit')")



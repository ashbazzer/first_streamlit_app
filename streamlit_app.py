import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title('Foods')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# pick list to pick wanted fruit
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Banana', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    call_fruityvice = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(call_fruityvice)
except URLError as e:
  streamlit.error()

streamlit.header("View our fruit list - Add your favourites!")
# snowflake func
def get_fruit_list_load():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return(my_cur.fetchall())

# add button
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_list_load()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# allow end user to add fruit to list
def insert_row_snowflake(new_fruit): 
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"INSERT INTO fruit_load_list VALUES ('{new_fruit}')")
    return f"Thanks for adding {new_fruit}"
 
add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  add_fruit = insert_row_snowflake(add_my_fruit)
  streamli.text(add_fruit)

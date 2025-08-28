#SMOOTHIES.PUBLIC# Import python packages
import streamlit as st
cnx = st.connection('snowflake')
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
        
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    #st.write(ingredients_string)
    
    insert_variable = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(insert_variable)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_variable).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon='✅')






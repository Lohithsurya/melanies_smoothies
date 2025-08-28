#SMOOTHIES.PUBLIC# Import python packages
import streamlit as st
import requests
cnx = st.connection('snowflake')
from snowflake.snowpark.functions import col
import pandas


# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose upto 5 ingredients:', my_dataframe, max_selections = 5)



if ingredients_list:
    ingredients_string = ''
        
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for', fruit, 'is', search_on, '.')

      
        st.subheader(fruit + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    #st.write(ingredients_string)
    
    insert_variable = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(insert_variable)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_variable).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon='✅')






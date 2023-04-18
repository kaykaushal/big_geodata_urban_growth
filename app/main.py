import streamlit as st
#import leafmap.foliumap as leafmap
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Template URL: <https://template.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Streamlit for Geospatial Applications of Urban Growth")

st.markdown(
    """
    This is a interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). 
    """
)

st.header("Image Exploaration & Analysis")



data = {'col1': [1, 2, 3, 4, 5], 
        'col2': [6, 7, 8, 9, 10], 
        'col3': [11, 12, 13, 14, 15]}
df = pd.DataFrame(data)

st.dataframe(df.describe())

st.title('Band Density Plot')
# plot the density plot for all columns with legend
fig, ax = plt.subplots()
df.plot.density(ax=ax, legend=True, figsize=(20, 10))

data = np.random.randn(10, 1)

col1, col2 = st.columns(2)
col1.subheader("Bands Discriptive Analysis")
col1.dataframe(df.describe())

col2.subheader("Bands Density Density Plot")
col2.pyplot(fig)
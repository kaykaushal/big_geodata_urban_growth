import streamlit as st
#import leafmap.foliumap as leafmap
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

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


data = {'column1': np.random.normal(0, 1, 100), 
        'column2': np.random.normal(1, 2, 100), 
        'column3': np.random.normal(-1, 0.5, 100),
        'column4': np.random.normal(2, 1.5, 100)}
df = pd.DataFrame(data)

# create a figure with a size of 8 inches by 6 inches
fig_b, ax_b = plt.subplots(figsize=(8, 6))

# create a box plot for each column and add it to the figure
for col in df.columns:
    ax_b.boxplot(df[col], positions=[df.columns.get_loc(col)+1], widths=0.6, showfliers=True)

# set the x-axis tick labels to the column names
ax.set_xticks(range(1, len(df.columns)+1))
ax.set_xticklabels(df.columns)

# set the y-axis label
ax.set_ylabel('Pixel Value')

st.pyplot(fig_b)

# create a correlation matrix heaymap

correlations = df.corr()
fig_c, ax_c = plt.subplots()
heatmap = sns.heatmap(correlations, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Band Correlation Heatmap', fontdict={'fontsize':18}, pad=12);

st.pyplot(fig_c)


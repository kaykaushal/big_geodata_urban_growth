import streamlit as st
import leafmap.foliumap as leafmap
import yaml
from pathlib import Path
import pandas as pd
import rasterio
import rasterio.plot
from rasterio.plot import show_hist
import seaborn as sns


# visualization package
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
This app is developement stage with source code at
GitHub Repository: <https://github.com/kaykaushal/big_geodata_urban_growth.git>
Template URL: <https://template.streamlit.app>
"""
# Sidebar
# Create data selector 
with st.sidebar.form(key="my_form"):
    selectbox_city = st.selectbox("Choose a city", ["ernakulam", "pune"])
    selectbox_year = st.selectbox("Select year", [2002, 2012, 2022])
    selectbox_band = st.multiselect("Select Bands", ['blue','green','red','nir','swir1','swir2'])
    # st.markdown(
    #     '<p class="small-font">Results Limited to top 5 per State in overall US</p>',
    #     unsafe_allow_html=True,
    # )
    pressed = st.form_submit_button("Load Image")

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

## Main Page 
# Customize page title
st.title("Streamlit for Geospatial Applications of Urban Growth")
st.markdown(
    """
    This is a interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). 
    """
)
## Data Collection & Processing 
# Load tiff file and 
@st.cache_data
def load_data(area, year):
    # check if file exists
    output_file = f"{area}_{year}.tif"
    file_path = Path("download.yml")
    if file_path.exists():
        # open file using PyYAML library
        with open('download.yml') as f:
            data = yaml.safe_load(f)
            url = data[area][year]
            load_url = (url)
            if output_file in locals():
              return output_file
            else:
              return leafmap.download_file(load_url, output_file, unzip=False)

    else:
        print("File not found.")

src_image = load_data(selectbox_city, selectbox_year)

# get dataframe from .tif
@st.cache_data
def get_dataframe(file_path):
    with rasterio.open(str(file_path)) as src:
        data = src.read()
    df = pd.DataFrame(data.reshape(data.shape[0], -1).T, columns=['blue','green','red','nir','swir1','swir2'])
    df = df.dropna()
    return df 

#st.write('Selected image path:', src_image)
## Data Exploration and visualization  
# get dataframe from raster layer
df = get_dataframe(src_image)

# density
fig_hist, ax_hist = plt.subplots(figsize=(10, 8))
for col in df.columns:
    ax_hist.hist(df[col], alpha=0.7, label=col)
ax_hist.legend() # Add this line to show legend
ax_hist.set_xlabel('pixel value')
ax_hist.set_ylabel('density')  

# Add into one column of main page 
col1, col2 = st.columns(2)
col1.subheader("Bands Discriptive Analysis")
col1.dataframe(df.describe())

col2.subheader("Bands Density Density Plot")
col2.pyplot(fig_hist)

## Layout 2 Visualization 

# create a figure with a size of 8 inches by 6 inches
fig_b, ax_b = plt.subplots(figsize=(8, 6))
# create a box plot for each column and add it to the figure
for col in df.columns:
    ax_b.boxplot(df[col], positions=[df.columns.get_loc(col)+1], widths=0.6, showfliers=True)
# set the x-axis tick labels to the column names
ax_b.set_xticks(range(1, len(df.columns)+1))
ax_b.set_xticklabels(df.columns)
# set the y-axis label
ax_b.set_ylabel('Pixel Value')

#st.pyplot(fig_b)
# create a correlation matrix heaymap

correlations = df.corr()
fig_c, ax_c = plt.subplots()
heatmap = sns.heatmap(correlations, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Band Correlation Heatmap', fontdict={'fontsize':18}, pad=12);

# Add into one column of main page 
col3, col4 = st.columns(2)
col3.subheader("Box Plots")
col3.pyplot(fig_b)

col4.subheader("Bands Correlation Heatmap")
col4.pyplot(fig_c)



# # Plot raster 
m_band = leafmap.Map()
m_band.add_raster(src_image, bands=[5, 4, 3], colormap='terrain', layer_name='All Band')
m_band.to_streamlit(height=600)

# Model expander 
with st.expander("Expand for image class model"):
    if st.button('Predict'):
        st.write('Class prediction for loaded image!')



# with st.expander("See source code"):
#     with st.echo():
#         m1 = leafmap.Map()
#         m1.add_tile_layer(
#         url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
#         name="Google Satellite",
#         attribution="Google",)
#         m1.add_raster(src_image, bands=[3, 4, 5], layer_name=f'Ernakulum 2022')
#         #m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')
# m1.to_streamlit(height=700)

# # visualize 
# raster_data = rasterio.open(str(src_image))
# #raster_plot = plt.imshow(raster_data.read(1), cmap='pink')
# #raster_plot = rasterio.plot.show(raster_data, 3)
# # Plot on dashboard
# #st.image(raster_plot, caption=f'Raster Image {selectbox_city}-{selectbox_year}')
# fig, ax = plt.subplots()
# ax.imshow(raster_data.read(1), cmap='pink')
# st.pyplot(fig)


# # Band Frequency
# fig_hist, ax_hist = plt.subplots()
# for col in df.columns:
#     ax_hist.hist(df[col], alpha=0.5, label=col)
# ax_hist.legend()  # Add this line to show legend
# st.pyplot(fig_hist)


# st.header("Global LULC & FCC Map")


# # LULC worldwide map
# with st.expander("See source code"):
#     with st.echo():
#         m = leafmap.Map()
#         m.split_map(
#             left_layer='ESA WorldCover 2020 S2 FCC', right_layer='ESA WorldCover 2020'
#         )
#         m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')

# m.to_streamlit(height=700)
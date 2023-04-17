import streamlit as st
import leafmap.foliumap as leafmap
import yaml
from pathlib import Path
import pandas as pd
import rasterio
import rasterio.plot
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Template URL: <https://template.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""
# Sidebar
# Create data selector 
with st.sidebar.form(key="my_form"):
    selectbox_city = st.selectbox("Choose a city", ["ernakulam", "pune"])
    selectbox_year = st.selectbox("Select year", [2002, 2012, 2022])
    selectbox_band = st.multiselect("Select Bands", ['blue','green','red','nir','swir1','swir2'])
    st.markdown(
        '<p class="small-font">Results Limited to top 5 per State in overall US</p>',
        unsafe_allow_html=True,
    )
    pressed = st.form_submit_button("Load Image")

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

st.header("Global LULC & FCC Map")


# LULC worldwide map
with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            left_layer='ESA WorldCover 2020 S2 FCC', right_layer='ESA WorldCover 2020'
        )
        m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')

m.to_streamlit(height=700)

# Load tiff file and 
@st.cache()
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

st.write('Selected image path:', src_image)

# get dataframe from .tif
@st.cache()
def get_dataframe(file_path):
    with rasterio.open(str(file_path)) as src:
        data = src.read()
    df = pd.DataFrame(data.reshape(data.shape[0], -1).T, columns=['blue','green','red','nir','swir1','swir2'])
    df = df.dropna()
    return df 

# Plot raster 
with st.expander("See source code"):
    with st.echo():
        m1 = leafmap.Map()
        m1.add_tile_layer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        name="Google Satellite",
        attribution="Google",)
        m1.add_raster(src_image, bands=[3, 4, 5], layer_name=f'Ernakulum 2022')
        #m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')

m1.to_streamlit(height=700)

df = get_dataframe(src_image)
st.write(df.describe())

# visualize 
raster_data = rasterio.open(str(src_image))
#raster_plot = plt.imshow(raster_data.read(1), cmap='pink')
#raster_plot = rasterio.plot.show(raster_data, 3)
# Plot on dashboard
#st.image(raster_plot, caption=f'Raster Image {selectbox_city}-{selectbox_year}')
fig, ax = plt.subplots()
ax.imshow(raster_data.read(1), cmap='pink')
st.pyplot(fig)
//script for exporting Landsat8 images to Google drive
//give respective filters
//use boundary to clip data

var boundary = ee.FeatureCollection("users/sreeharikollamattam/pune_dist");


var dataset_2022 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterDate('2022-01-01', '2022-04-20')
    .filterMetadata('CLOUD_COVER', 'less_than', 10)
    .filterBounds(boundary);
    
var image_2022 = dataset_2022.median();

image_2022 = image_2022.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'])
                       .rename(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);
                       

Export.image.toDrive({
  image: image_2022.clip(boundary),
  description: 'image_2022_mean',
  region: boundary,
  scale: 30,
  maxPixels: 1e13
});
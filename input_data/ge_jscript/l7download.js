//script for exporting Landsat7 images to Google Drive
//give respective filters
//use boundary to clip data

var boundary = ee.FeatureCollection("users/sreeharikollamattam/ekm_dist");

var dataset_2002 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
    .filterDate('2012-01-01', '2012-12-31')
    .filterMetadata('CLOUD_COVER', 'less_than', 10)
    .filterBounds(boundary);
    
    
var image_2002 = dataset_2002.median();

image_2002 = image_2002.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'])
                       .rename(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);

Export.image.toDrive({
  image: image_2002.clip(boundary),
  description: 'image_2012',
  region: boundary,
  scale: 30,
  maxPixels: 1e13
});
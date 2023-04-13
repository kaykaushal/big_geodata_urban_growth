//script for exporting Landsat5 images to Google Drive
//give respective filters
//use boundary to clip data

var boundary = ee.FeatureCollection("users/sreeharikollamattam/ekm_dist");

var dataset_1992 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
    .filterDate('2002-01-01', '2002-12-31')
    .filterMetadata('CLOUD_COVER', 'less_than', 10)
    .filterBounds(boundary);
    
    
    

var image_1992 = dataset_1992.median()

image_1992 = image_1992.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'])
                       .rename(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);
                       
                       
Export.image.toDrive({
  image: image_1992.clip(boundary),
  description: 'image_2011ekm',
  region: boundary,
  scale: 30,
  maxPixels: 1e13
});
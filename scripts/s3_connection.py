# package import 
from pyspark.sql.functions import *
import urllib

## mount s3 bucket 
# create iam user with FullAccessS3
# download access_key .csv and load into databricks dbfs 

dbutils.fs.ls('/FileStore/tables/')
# read config and key file 
file_type = "csv"
first_row_header = "true"
delimeter = ","

aws_key_df = spark.read.format(file_type) \
.option("header", first_row_header) \
.option("sep", delimeter) \
.load('/FileStore/tables/databricks_1_accessKeys.csv')

# variable of keys for s3 access
ACCESS_KEY = aws_key_df.select('access_key').collect()[0].access_key
SECRET_KEY = aws_key_df.select('secret_access_key').collect()[0].secret_access_key
# Encode the key 
ENCODE_SECRET_KEY = urllib.parse.quote(SECRET_KEY, "")

# data access of from s3 bucket
AWS_BUCKET_NAME = "iirs-geospatial-store"
MOUNT_NAME = "/mnt/iirs-geospatial-store"
sourceUri = "s3n://{0}:{1}@{2}".format(ACCESS_KEY, ENCODE_SECRET_KEY, AWS_BUCKET_NAME)

dbutils.fs.mount(sourceUri, MOUNT_NAME)

# check file in local 
## %fs ls "/mnt/iirs-geospatial-store"
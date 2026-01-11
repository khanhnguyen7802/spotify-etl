@dlt.table(
    name="raw_data",
    comment="Raw .csv files ingested from Google Cloud Storage",
    table_properties={"quality": "landing"}
)
def raw_data():
  return (
      spark.readStream \
      .format("cloudFiles") \
      .option("cloudFiles.format", "csv") \
      .load(f"/Volumes/...")
  )
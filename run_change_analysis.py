from pathlib import Path

from src.export_cog import export_cog, export_geotiff

from rasterio.windows import Window

from src.change_detection import calculate_ndvi_change
from src.pipeline import process_sentinel2_window
from src.visualization import plot_ndvi_change

from src.postgis_loader import connect_postgis, insert_change_product
from src.preprocess import get_footprint_wkt


window = Window(1900, 2902, 100, 100)

result_2021 = process_sentinel2_window(
    "data/raw/2021-06-17_T33UUS_B04_10m.jp2",
    "data/raw/2021-06-17_T33UUS_B08_10m.jp2",
    "data/raw/2021-06-17_T33UUS_SCL_20m.jp2",
    window,
    0.0001,
    -0.1,
    0,
)

result_2024 = process_sentinel2_window(
    "data/raw/2024-06-26_T33UUS_B04_10m.jp2",
    "data/raw/2024-06-26_T33UUS_B08_10m.jp2",
    "data/raw/2024-06-26_T33UUS_SCL_20m.jp2",
    window,
    0.0001,
    -0.1,
    0,
)

change = calculate_ndvi_change(
    result_2021,
    result_2024,
)

Path("outputs").mkdir(exist_ok=True)

geotiff_path = export_geotiff(
    change,
    "outputs/ndvi_change_2021_2024.tif",
)

cog_path = export_cog(
    geotiff_path,
    "outputs/ndvi_change_2021_2024_cog.tif",
)


plot_ndvi_change(
    change,
    output_path="outputs/ndvi_change_2021_2024.png",
)

print(f"Mean NDVI change: {change['mean_change']:.4f}")
print(f"Median NDVI change: {change['median_change']:.4f}")
print(
    f"Pixels decreased: "
    f"{change['decreased_fraction']:.2%}"
)
print("Saved: outputs/ndvi_change_2021_2024.png")
print("GeoTIFF:", geotiff_path)
print("COG:", cog_path)



footprint_wkt = get_footprint_wkt(
    change["change"].shape,
    change["transform"],
    change["crs"],
)

conn = connect_postgis()

product_id = insert_change_product(
    conn=conn,
    asset_id=1,
    before_date="2021-06-17",
    after_date="2024-06-26",
    change_result=change,
    cog_path=cog_path,
    footprint_wkt=footprint_wkt,
)

conn.close()

print(f"PostGIS product ID: {product_id}")
from pathlib import Path

from src.export_cog import export_cog, export_geotiff

from rasterio.windows import Window

from src.change_detection import calculate_ndvi_change
from src.pipeline import process_sentinel2_window
from src.visualization import plot_ndvi_change


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

Path("outputs").mkdir(exist_ok=True)

plot_ndvi_change(
    change,
    output_path="outputs/ndvi_change_2021_2024.png",
)

print(f"Mean ΔNDVI: {change['mean_change']:.4f}")
print(f"Median ΔNDVI: {change['median_change']:.4f}")
print(
    f"Pixels decreased: "
    f"{change['decreased_fraction']:.2%}"
)
print("Saved: outputs/ndvi_change_2021_2024.png")
print("GeoTIFF:", geotiff_path)
print("COG:", cog_path)
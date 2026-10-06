from pathlib import Path

import numpy as np
import rasterio


def export_geotiff(change, output_path):
    """Export an NDVI change result as a georeferenced GeoTIFF."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    nodata = -9999.0

    data = change["change"].astype("float32").copy()
    data[np.isnan(data)] = nodata

    with rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype="float32",
        crs=change["crs"],
        transform=change["transform"],
        nodata=nodata,
        compress="deflate",
    ) as dst:
        dst.write(data, 1)

    return output_path


def export_cog(source_path, output_path):
    """Convert a GeoTIFF into a Cloud Optimized GeoTIFF."""

    source_path = Path(source_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(source_path) as src:
        profile = src.profile.copy()
        data = src.read(1)

        profile.update(
            driver="COG",
            compress="DEFLATE",
        )

        with rasterio.open(
            output_path,
            "w",
            **profile,
        ) as dst:
            dst.write(data, 1)

    return output_path
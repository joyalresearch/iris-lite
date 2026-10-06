import numpy as np
import rasterio

from src.indices import calculate_ndvi
from src.preprocess import (
    align_categorical_raster,
    apply_raster_scaling,
    create_scl_quality_mask,
)

def process_sentinel2_window(
    red_path,
    nir_path,
    scl_path,
    window,
    scale,
    offset,
    nodata,
):
    """Process Sentinel-2 bands for one analysis window and return NDVI."""

    with rasterio.open(red_path) as red_src, \
         rasterio.open(nir_path) as nir_src, \
         rasterio.open(scl_path) as scl_src:

        red_raw = red_src.read(1, window=window)
        nir_raw = nir_src.read(1, window=window)

        analysis_transform = red_src.window_transform(window)

        scl_raw = scl_src.read(1)

        aligned_scl = align_categorical_raster(
            source=scl_raw,
            source_transform=scl_src.transform,
            source_crs=scl_src.crs,
            destination_shape=red_raw.shape,
            destination_transform=analysis_transform,
            destination_crs=red_src.crs,
        )

        red = apply_raster_scaling(
            red_raw,
            scale=scale,
            offset=offset,
            nodata=nodata,
        )

        nir = apply_raster_scaling(
            nir_raw,
            scale=scale,
            offset=offset,
            nodata=nodata,
        )

        quality_mask = create_scl_quality_mask(aligned_scl)

        red[~quality_mask] = np.nan
        nir[~quality_mask] = np.nan

        ndvi = calculate_ndvi(nir, red)

        return {
            "ndvi": ndvi,
            "crs": red_src.crs,
            "transform": analysis_transform,
            "valid_pixel_count": int(np.isfinite(ndvi).sum()),
            "total_pixel_count": int(ndvi.size),
            "valid_fraction": float(np.isfinite(ndvi).sum() / ndvi.size),
            "scl_classes": np.unique(aligned_scl).tolist(),
        }



import numpy as np
from rasterio.warp import reproject, Resampling




def apply_raster_scaling(data, scale, offset, nodata=None):
    """Convert stored raster values to physical values and mask nodata."""

    result = data.astype(float)

    if nodata is not None:
        nodata_mask = data == nodata
    else:
        nodata_mask = np.zeros(data.shape, dtype=bool)

    result = result * scale + offset
    result[nodata_mask] = np.nan

    return result

def create_scl_quality_mask(scl, excluded_classes=None):
    """Return True for pixels considered valid for analysis."""

    if excluded_classes is None:
        excluded_classes = [3, 8, 9, 10]

    return ~np.isin(scl, excluded_classes)

def align_categorical_raster(
    source,
    source_transform,
    source_crs,
    destination_shape,
    destination_transform,
    destination_crs,
):
    """Align categorical raster data to a destination grid."""

    destination = np.empty(destination_shape, dtype=source.dtype)

    reproject(
        source=source,
        destination=destination,
        src_transform=source_transform,
        src_crs=source_crs,
        dst_transform=destination_transform,
        dst_crs=destination_crs,
        resampling=Resampling.nearest,
    )

    return destination
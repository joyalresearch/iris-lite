import numpy as np
from rasterio.transform import array_bounds
from rasterio.warp import reproject, Resampling, transform_bounds




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


def get_footprint_wkt(shape, transform, crs):
    """Return a raster grid footprint as an EPSG:4326 WKT polygon."""

    height, width = shape

    left, bottom, right, top = array_bounds(
        height,
        width,
        transform,
    )

    lon_left, lat_bottom, lon_right, lat_top = transform_bounds(
        crs,
        "EPSG:4326",
        left,
        bottom,
        right,
        top,
    )

    return (
        f"POLYGON(("
        f"{lon_left} {lat_bottom}, "
        f"{lon_right} {lat_bottom}, "
        f"{lon_right} {lat_top}, "
        f"{lon_left} {lat_top}, "
        f"{lon_left} {lat_bottom}"
        f"))"
    )
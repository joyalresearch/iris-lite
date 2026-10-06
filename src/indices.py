import numpy as np


def calculate_ndvi(nir, red):
    """Calculate NDVI while preserving invalid pixels."""

    denominator = nir + red

    ndvi = np.full(
        nir.shape,
        np.nan,
        dtype=float
    )

    valid = (
        np.isfinite(nir)
        & np.isfinite(red)
        & (denominator != 0)
    )

    ndvi[valid] = (
        (nir[valid] - red[valid])
        / denominator[valid]
    )

    return ndvi
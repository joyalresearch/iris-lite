import numpy as np

from src.indices import calculate_ndvi


def test_calculate_ndvi_handles_invalid_pixels():
    red = np.array([0.2, 0.0, np.nan])
    nir = np.array([0.6, 0.0, 0.5])

    result = calculate_ndvi(nir, red)

    assert np.isclose(result[0], 0.5)
    assert np.isnan(result[1])
    assert np.isnan(result[2])
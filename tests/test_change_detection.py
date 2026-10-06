import numpy as np
from rasterio.transform import from_origin

from src.change_detection import calculate_ndvi_change


def test_calculate_ndvi_change_handles_invalid_pixels():
    transform = from_origin(
        500000,
        5700000,
        10,
        10,
    )

    before = {
        "ndvi": np.array([0.7, 0.5, np.nan, 0.2]),
        "crs": "EPSG:32633",
        "transform": transform,
    }

    after = {
        "ndvi": np.array([0.4, 0.6, 0.3, np.nan]),
        "crs": "EPSG:32633",
        "transform": transform,
    }

    result = calculate_ndvi_change(before, after)

    expected = np.array([-0.3, 0.1, np.nan, np.nan])

    assert np.allclose(
        result["change"],
        expected,
        equal_nan=True,
    )

    assert result["valid_pixel_count"] == 2
    assert result["decreased_pixel_count"] == 1
    assert np.isclose(result["decreased_fraction"], 0.5)


def test_calculate_ndvi_change_rejects_misaligned_grids():
    before = {
        "ndvi": np.array([[0.7, 0.5]]),
        "crs": "EPSG:32633",
        "transform": from_origin(
            500000,
            5700000,
            10,
            10,
        ),
    }

    after = {
        "ndvi": np.array([[0.4, 0.6]]),
        "crs": "EPSG:32633",
        "transform": from_origin(
            500010,
            5700000,
            10,
            10,
        ),
    }

    try:
        calculate_ndvi_change(before, after)
        assert False, "Expected ValueError for misaligned grids"
    except ValueError as error:
        assert "transform" in str(error).lower()
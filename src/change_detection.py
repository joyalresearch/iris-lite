import numpy as np


def calculate_ndvi_change(before_result, after_result):
    """Calculate NDVI change between two spatially aligned observations."""

    before = before_result["ndvi"]
    after = after_result["ndvi"]

    if before.shape != after.shape:
        raise ValueError(
            "Before and after NDVI arrays must have the same shape."
        )

    if before_result["crs"] != after_result["crs"]:
        raise ValueError(
            "Before and after observations must have the same CRS."
        )

    if before_result["transform"] != after_result["transform"]:
        raise ValueError(
            "Before and after observations must have the same transform."
        )

    change = np.full(before.shape, np.nan, dtype=float)

    valid = np.isfinite(before) & np.isfinite(after)

    change[valid] = after[valid] - before[valid]

    valid_changes = change[valid]

    return {
        "change": change,
        "crs": before_result["crs"],
        "transform": before_result["transform"],
        "valid_pixel_count": int(valid.sum()),
        "mean_change": float(np.mean(valid_changes)),
        "median_change": float(np.median(valid_changes)),
        "decreased_pixel_count": int(np.sum(valid_changes < 0)),
        "decreased_fraction": float(np.mean(valid_changes < 0)),
    }
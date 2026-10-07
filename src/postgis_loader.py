
import os

import psycopg
from dotenv import load_dotenv


def connect_postgis():
    """Create a connection to the IRIS-Lite PostGIS database."""
    load_dotenv()

    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

def insert_change_product(
    conn,
    asset_id,
    before_date,
    after_date,
    change_result,
    cog_path,
    footprint_wkt,
):
    """Insert metadata and summary statistics for an EO change product."""

    sql = """
        INSERT INTO eo_change_products (
            asset_id,
            before_date,
            after_date,
            index_name,
            mean_change,
            median_change,
            decreased_fraction,
            valid_pixel_count,
            total_pixel_count,
            cog_path,
            raster_crs,
            pixel_size_m,
            footprint
        )
        VALUES (
            %(asset_id)s,
            %(before_date)s,
            %(after_date)s,
            'NDVI',
            %(mean_change)s,
            %(median_change)s,
            %(decreased_fraction)s,
            %(valid_pixel_count)s,
            %(total_pixel_count)s,
            %(cog_path)s,
            %(raster_crs)s,
            %(pixel_size_m)s,
            ST_GeomFromText(%(footprint_wkt)s, 4326)
        )
        RETURNING product_id;
    """

    parameters = {
        "asset_id": asset_id,
        "before_date": before_date,
        "after_date": after_date,
        "mean_change": change_result["mean_change"],
        "median_change": change_result["median_change"],
        "decreased_fraction": change_result["decreased_fraction"],
        "valid_pixel_count": change_result["valid_pixel_count"],
        "total_pixel_count": change_result["change"].size,
        "cog_path": str(cog_path),
        "raster_crs": str(change_result["crs"]),
        "pixel_size_m": 10.0,
        "footprint_wkt": footprint_wkt,
    }

    product_id = conn.execute(sql, parameters).fetchone()[0]
    conn.commit()

    return product_id
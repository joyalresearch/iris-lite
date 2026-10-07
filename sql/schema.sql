CREATE EXTENSION IF NOT EXISTS postgis;


CREATE TABLE IF NOT EXISTS monitored_assets (
    asset_id SERIAL PRIMARY KEY,
    asset_name TEXT NOT NULL,
    asset_type TEXT,
    geometry GEOMETRY(Polygon, 4326)
);


CREATE TABLE IF NOT EXISTS eo_change_products (
    product_id SERIAL PRIMARY KEY,

    asset_id INTEGER REFERENCES monitored_assets(asset_id),

    before_date DATE NOT NULL,
    after_date DATE NOT NULL,

    index_name TEXT NOT NULL,

    mean_change DOUBLE PRECISION,
    median_change DOUBLE PRECISION,
    decreased_fraction DOUBLE PRECISION,

    valid_pixel_count INTEGER,
    total_pixel_count INTEGER,

    cog_path TEXT NOT NULL,

    raster_crs TEXT,
    pixel_size_m DOUBLE PRECISION,

    footprint GEOMETRY(Polygon, 4326),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_monitored_assets_geometry
ON monitored_assets
USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_eo_change_products_footprint
ON eo_change_products
USING GIST (footprint);
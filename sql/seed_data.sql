INSERT INTO monitored_assets (
    asset_name,
    asset_type,
    geometry
)
VALUES (
    'Energiepark Witznitz',
    'Solar Energy Facility',
    ST_GeomFromText(
        'POLYGON((
            12.40886 51.14724,
            12.42886 51.14724,
            12.42886 51.16724,
            12.40886 51.16724,
            12.40886 51.14724
        ))',
        4326
    )
);
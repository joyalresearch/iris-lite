# IRIS-Lite Methodology

## 1. Objective

IRIS-Lite investigates whether Earth Observation data can be used to detect and summarize environmental and surface change around an infrastructure asset.

The demonstration compares observations from 2021 and 2024 within a 1 km x 1 km analysis area near Energiepark Witznitz in Saxony, Germany.

Two complementary satellite sensors are used:

- Sentinel-2 multispectral imagery for vegetation-related spectral change
- Sentinel-1 Synthetic Aperture Radar (SAR) for radar backscatter change

The objective is change detection rather than causal attribution. A detected satellite signal indicates that measured surface properties changed; it does not by itself establish why the change occurred.

## 2. Analysis Area

The analysis uses a fixed 1 km x 1 km raster window around the demonstration area.

The working raster CRS is:

```text
EPSG:32633
WGS 84 / UTM zone 33N
```

A projected CRS is useful for this analysis because raster dimensions and pixel spacing can be represented in metres.

At 10 m spatial resolution, the analysis window contains:

```text
100 rows x 100 columns = 10,000 pixels
```

Each 10 m pixel represents approximately a 10 m x 10 m ground cell.

The demonstration geometry is used for portfolio analysis and should not be interpreted as an authoritative infrastructure boundary.

## 3. Sentinel-2 Data Selection

Sentinel-2 Level-2A products were selected through the Copernicus Data Space Ecosystem STAC API.

Level-2A was preferred because it provides atmospherically corrected Bottom-of-Atmosphere reflectance estimates suitable for surface and vegetation analysis.

The primary bands used were:

- B04 - Red
- B08 - Near Infrared (NIR)
- SCL - Scene Classification Layer

B04 and B08 have a native spatial resolution of 10 m.

SCL is categorical quality information provided at a lower native resolution and therefore requires alignment with the 10 m analysis grid before it can be used as a pixel-level mask.

The selected observations were approximately season matched:

```text
2021 Sentinel-2 observation: June 2021
2024 Sentinel-2 observation: June 2024
```

Using approximately comparable times of year reduces, but does not eliminate, seasonal vegetation effects.

## 4. Sentinel-2 Reflectance Preprocessing

Sentinel-2 raster files store numerical values that require interpretation using product metadata.

The workflow applies the raster scale and offset before spectral-index calculation.

Conceptually:

```text
physical reflectance = stored value * scale + offset
```

NoData values are converted to invalid values before analysis so they cannot be interpreted as legitimate reflectance measurements.

This distinction is important because missing raster data must not contribute to NDVI or change statistics.

## 5. Scene Classification and Quality Masking

The Sentinel-2 Scene Classification Layer is used to identify pixels unsuitable for optical analysis.

The workflow excludes classes representing:

- cloud shadow
- medium-probability cloud
- high-probability cloud
- cirrus

The SCL raster is categorical rather than continuous.

For that reason, nearest-neighbor resampling is used when aligning SCL with the 10 m analysis grid. Interpolating categorical class numbers would create values that do not represent valid SCL classes.

Resampling the lower-resolution SCL raster to a 10 m grid does not create additional classification information. It only aligns the existing classification with the analysis grid.

## 6. Raster Alignment

Raster subtraction is only meaningful when corresponding array cells represent the same locations on Earth.

Matching CRS and nominal pixel resolution alone are not sufficient to guarantee this.

Before temporal comparison, the workflow checks spatial properties including:

- CRS
- raster dimensions
- affine transform
- analysis extent
- pixel resolution

The affine transform provides the relationship between raster row/column positions and projected spatial coordinates.

This validation ensures that a pixel at a particular array location in the 2021 raster corresponds to the same ground location in the 2024 raster.

## 7. NDVI Calculation

Vegetation response is measured using the Normalized Difference Vegetation Index:

```text
NDVI = (NIR - Red) / (NIR + Red)
```

Healthy vegetation commonly absorbs a large proportion of incoming red radiation while strongly scattering or reflecting near-infrared radiation.

This creates the spectral contrast measured by NDVI.

Pixels with invalid Red or NIR measurements are excluded. Pixels where the NDVI denominator is zero are also treated as invalid rather than being assigned an artificial NDVI value.

NDVI is interpreted as a spectral vegetation indicator rather than direct proof of vegetation health or land-cover type.

## 8. Sentinel-2 Temporal Change

NDVI change is calculated pixel by pixel as:

```text
NDVI change = NDVI_2024 - NDVI_2021
```

Therefore:

```text
negative value -> NDVI decreased
positive value -> NDVI increased
value near zero -> little measured NDVI change
```

Within the 10,000-pixel analysis area, the observed results were:

- 2021 mean NDVI: 0.542
- 2024 mean NDVI: 0.306
- mean NDVI change: -0.236
- median NDVI change: -0.152
- fraction of pixels with decreased NDVI: 69.5%

These statistics indicate a substantial decline in vegetation-like spectral response across much of the analysis area.

They do not establish the cause of that decline.

## 9. Sentinel-1 Experiment

Sentinel-1 was added as a complementary sensor because SAR measures different physical properties from Sentinel-2 optical imagery.

Sentinel-1 is an active microwave sensor. It transmits microwave energy toward the Earth and measures the returned radar signal, or backscatter.

Because the sensor supplies its own transmitted energy, Sentinel-1 observations do not depend on sunlight and can operate during both day and night.

Microwave observations are also substantially less affected by cloud cover than optical Sentinel-2 imagery.

Radar backscatter can respond to factors including:

- surface roughness
- surface geometry
- vegetation structure
- soil and surface moisture
- buildings and other structures
- radar viewing geometry

For this reason, radar change is not interpreted as a direct substitute for NDVI change.

## 10. Sentinel-1 Acquisition Matching

Radar comparisons are sensitive to acquisition geometry.

The 2021 and 2024 acquisitions were therefore selected to match key characteristics:

- Sentinel-1A platform
- IW acquisition mode
- GRD product type
- descending orbit direction
- relative orbit 95
- VV and VH availability

VV polarization was used for the experiment.

The selected acquisitions were:

```text
2021: 2021-06-13
2024: 2024-06-21
```

Selecting approximately season-matched acquisitions also reduces large seasonal differences, although environmental conditions such as moisture can still influence radar backscatter.

## 11. Sentinel-1 Product Inspection

Initial inspection of the Sentinel-1 GRD measurement COG showed that the accessed measurement raster exposed amplitude values without a conventional projected CRS and affine transform suitable for direct quantitative temporal subtraction.

Inspection of the associated product metadata confirmed the presence of:

- geolocation-grid points
- latitude and longitude information
- incidence-angle information
- radiometric calibration vectors
- sigma nought calibration information

This demonstrated that the measurement data required additional SAR preprocessing rather than being treated as an ordinary analysis-ready georeferenced raster.

The project therefore avoids manually implementing the complete Sentinel-1 calibration and geolocation workflow.

## 12. Sentinel-1 Processing with openEO

Sentinel-1 processing was performed server-side using the Copernicus Data Space openEO service.

The processing workflow:

1. loads the selected Sentinel-1 GRD acquisition,
2. selects VV polarization,
3. applies SAR backscatter processing,
4. produces sigma0-ellipsoid backscatter,
5. enables noise removal,
6. resamples the result to 10 m,
7. projects the result to EPSG:32633, and
8. exports the processed raster.

The processed 2021 and 2024 products were verified to use the same spatial grid.

They were then cropped to the exact 1 km x 1 km Sentinel-2 analysis footprint.

The resulting Sentinel-1 and Sentinel-2 analysis arrays were all:

```text
100 x 100 pixels
EPSG:32633
10 m pixel spacing
```

Their transforms were verified before cross-sensor comparison.

## 13. Radar Backscatter in Decibels

Processed sigma0 values were converted to decibels using:

```text
VV_dB = 10 * log10(sigma0)
```

Temporal radar change was then calculated as:

```text
VV change = VV_2024_dB - VV_2021_dB
```

Within the common analysis area:

- 2021 median VV: -14.01 dB
- 2024 median VV: -13.98 dB
- mean VV change: -0.35 dB
- median VV change: -0.17 dB
- fraction of pixels with decreased VV: 51.7%

The nearly balanced proportions of increasing and decreasing pixels indicate spatially heterogeneous radar change rather than a strong AOI-wide directional shift.

## 14. Cross-Sensor Comparison

The aligned Sentinel-2 NDVI-change raster and Sentinel-1 VV-change raster contain 10,000 common valid pixels.

The Pearson correlation between the two change measurements was:

```text
r = 0.305
```

This represents a weak-to-moderate positive spatial association.

The result should not be interpreted as evidence that both sensors measure the same phenomenon.

Sentinel-2 NDVI primarily captures spectral contrast associated with vegetation, while Sentinel-1 backscatter responds to microwave interactions with surface structure, geometry, vegetation, and moisture.

The difference between the signals is therefore scientifically useful rather than necessarily an error.

## 15. Raster Output

The detailed Sentinel-2 NDVI-change result is exported as a georeferenced raster and converted to a Cloud Optimized GeoTIFF.

The COG retains the pixel-level spatial result while allowing the database layer to remain focused on searchable metadata and summary information.

For this small 100 x 100 demonstration raster, the advantages of tiled remote access are limited, but the format demonstrates a storage pattern that scales to larger EO products.

## 16. PostGIS Data Model

PostgreSQL with the PostGIS extension is used for spatial metadata persistence.

The database separates two concepts:

```text
monitored asset
        |
        v
derived EO change product
```

The monitored-assets table stores infrastructure geometry and identifying information.

The EO change-products table stores information including:

- associated asset
- before and after dates
- index name
- mean change
- median change
- decreased-pixel fraction
- valid-pixel count
- total-pixel count
- raster path
- raster CRS
- pixel size
- analysis footprint

The detailed raster itself remains outside the relational database.

This architecture allows PostGIS to answer spatial and metadata queries while raster files retain the full pixel-level result.

## 17. Spatial Database Geometry

Database geometries use EPSG:4326 for asset and footprint storage.

Raster analysis is performed in EPSG:32633.

When required, geometries are transformed between coordinate systems rather than assuming that coordinates from different CRSs are directly interchangeable.

GiST spatial indexes are created on geometry columns to support efficient spatial queries as the number of assets and EO products grows.

## 18. Reproducibility

The project uses a Dockerized PostGIS environment so the database software and PostGIS version can be recreated consistently.

Python dependencies are recorded in:

```text
requirements.txt
```

Environment-variable placeholders are provided in:

```text
.env.example
```

Real Copernicus credentials and database passwords remain in the local `.env` file and are excluded from Git.

Core deterministic processing behavior is validated with pytest.

The current automated tests cover:

- NDVI behavior with invalid pixels
- temporal change behavior with invalid pixels
- rejection of incompatible raster grids during change calculation

## 19. Interpretation Constraints

Several factors limit how strongly the observed changes can be interpreted.

NDVI can vary because of:

- vegetation seasonality
- agricultural activity
- drought or rainfall
- land clearing
- construction
- cloud contamination
- atmospheric and acquisition differences

Sentinel-1 backscatter can vary because of:

- soil moisture
- rainfall
- vegetation structure
- surface roughness
- buildings
- incidence and viewing geometry
- acquisition conditions

For these reasons, neither NDVI change nor radar backscatter change is treated as independent proof of construction activity or infrastructure impact.

The analysis identifies measurable satellite-observed change that can be investigated further.

## 20. Scope and Future Development

IRIS-Lite is intentionally limited to a portfolio-scale demonstration.

A production system would require additional capabilities such as:

- automated multi-date time-series processing
- stronger provenance tracking
- automated AOI-level quality assessment
- retry and failure handling
- scalable job orchestration
- monitoring of multiple infrastructure assets
- additional optical indices such as NDWI
- multi-polarization SAR analysis
- terrain-aware radar processing
- web-based map visualization
- automated change alerts

A separate future direction would be Sentinel-1 interferometric analysis.

The current Sentinel-1 experiment uses GRD backscatter intensity and should not be described as InSAR. InSAR would require phase-preserving SLC products and an interferometric processing workflow.

## 21. Methodological Principle

The central principle of IRIS-Lite is that numerical raster comparison is only meaningful after establishing that the measurements are physically interpretable, quality controlled, spatially aligned, and sufficiently comparable in acquisition conditions.

The project therefore treats satellite imagery as geospatial measurement data rather than simply as pictures.
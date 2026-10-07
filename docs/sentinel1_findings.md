# Sentinel-1 Backscatter Change Experiment

## Objective

This experiment evaluates whether Sentinel-1 radar backscatter changed within the same 1 km² Witznitz analysis area used for the Sentinel-2 NDVI change analysis.

The Sentinel-1 result is intended as a complementary sensing modality. Sentinel-2 measures spectral reflectance and provides information such as vegetation-related NDVI change, while Sentinel-1 is an active microwave radar sensor whose backscatter responds to surface and structural properties.

This experiment does not attempt to prove that observed radar changes were caused by construction or any single physical process.

## Acquisition Strategy

Two Sentinel-1A acquisitions were selected:

| Period | Date | Mode | Product | Polarization | Orbit | Relative Orbit |
|---|---|---|---|---|---|---|
| Before | 2021-06-13 | IW | GRD | VV/VH | Descending | 95 |
| After | 2024-06-21 | IW | GRD | VV/VH | Descending | 95 |

VV was used for this experiment.

The acquisitions were selected from similar times of year and matched on platform, acquisition mode, product type, orbit direction, relative orbit, and polarization to reduce avoidable differences in acquisition geometry and seasonality.

## Why GRD Instead of InSAR?

This is a radar backscatter-change experiment, not an InSAR analysis.

Sentinel-1 GRD products are suitable for intensity/backscatter analysis. InSAR requires phase information preserved in SLC products and additional interferometric processing. Implementing InSAR was outside the scope of this project.

## Raw GRD Inspection

Initial inspection of the Sentinel-1 GRD measurement COG showed that the accessed measurement raster exposed amplitude values and did not provide a conventional projected CRS and affine transform suitable for direct quantitative comparison.

Inspection of the associated SAFE metadata confirmed the presence of:

- geolocation grid points;
- latitude and longitude information;
- incidence-angle information;
- radiometric calibration vectors;
- sigma-nought calibration information.

Therefore, raw 2021 and 2024 measurement pixels were not directly subtracted.

## Processing

Sentinel-1 processing was performed server-side through the Copernicus Data Space Ecosystem openEO service.

The processing workflow was:

1. Load the selected Sentinel-1 GRD acquisition.
2. Select VV polarization.
3. Apply the openEO `sar_backscatter` process using `sigma0-ellipsoid`.
4. Enable noise removal.
5. Resample the processed raster to EPSG:32633 at 10 m resolution.
6. Export the result as GeoTIFF.
7. Download the processed raster for local analysis with Rasterio.

The resulting 2021 and 2024 rasters had identical:

- CRS;
- resolution;
- shape;
- affine transform;
- spatial bounds.

This allowed direct pixel-to-pixel temporal comparison.

## Common Sentinel-1 / Sentinel-2 Analysis Area

The original Sentinel-1 processing extent was larger than the Sentinel-2 analysis area.

To make the cross-sensor comparison spatially consistent, the Sentinel-1 rasters were cropped to the exact footprint of the existing Sentinel-2 NDVI change COG.

Common analysis grid:

- CRS: EPSG:32633
- Resolution: 10 m
- Shape: 100 × 100 pixels
- Ground area: approximately 1 km²
- Valid overlapping pixels: 10,000

The cropped Sentinel-1 grid and Sentinel-2 change raster were verified to have identical CRS, resolution, shape, and affine transform before pixel-level comparison.

## Backscatter Change

Calibrated sigma0 values were converted to decibels (dB) before change analysis.

Change was defined as:

`VV change = VV 2024 - VV 2021`

Within the common 1 km² analysis area:

| Metric | Result |
|---|---:|
| 2021 median VV | -14.008 dB |
| 2024 median VV | -13.978 dB |
| Mean VV change | -0.349 dB |
| Median VV change | -0.173 dB |
| Pixels with increased VV | 48.34% |
| Pixels with decreased VV | 51.66% |

The aggregate VV signal therefore showed little net directional shift across the full analysis area.

However, the spatial change map showed heterogeneous local increases and decreases in radar backscatter.

## Comparison with Sentinel-2

The Sentinel-2 analysis produced:

- mean NDVI change: -0.236;
- median NDVI change: -0.152.

Pixel-level comparison between NDVI change and Sentinel-1 VV change produced:

`Pearson r = 0.305`

This indicates a weak-to-moderate positive spatial association between the two change measurements, but with substantial dispersion.

The radar result therefore does not simply reproduce the optical NDVI signal.

## Interpretation

Sentinel-2 showed a substantial decline in NDVI within the analysis area between the selected 2021 and 2024 observations.

Sentinel-1 VV showed heterogeneous spatial backscatter changes but little net AOI-wide shift. The pixel-level relationship between NDVI and VV change was positive but relatively weak.

The Sentinel-1 analysis therefore provides complementary information about surface response rather than independent confirmation of a single causal mechanism.

The observed changes should not be interpreted as proof that construction, vegetation removal, moisture variation, or another specific process caused the measured radar response.

## Limitations

This experiment has several important limitations:

- only one acquisition from each year was compared;
- radar backscatter can respond to soil moisture, vegetation structure, surface roughness, geometry, and built structures;
- SAR imagery contains speckle and substantial local variability;
- only VV was analyzed;
- no multi-temporal radar baseline was established;
- no field observations were used for validation;
- the analysis is backscatter change detection, not InSAR;
- correlation between NDVI and VV change does not establish causation.

A production implementation would benefit from multiple temporally matched acquisitions, additional polarization analysis, stronger temporal baselines, and validation against independent site information.

## Output

Final visualization:

`outputs/sentinel1/sentinel1_change_2021_2024.png`

The figure contains:

1. June 2021 VV backscatter;
2. June 2024 VV backscatter;
3. pixel-level VV backscatter change;
4. pixel-level NDVI change versus VV change.

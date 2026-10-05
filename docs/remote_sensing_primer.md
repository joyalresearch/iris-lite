# Remote Sensing Primer

This document records my understanding of the core remote-sensing concepts used in the IRIS-Lite project.

## 1. Reflectance

Reflectance is the proportion of incoming electromagnetic radiation that a surface reflects.

## 2. Spatial Resolution

Spatial resolution describes the ground dimensions represented by a pixel. A 10 m Sentinel-2 pixel represents approximately a 10 m × 10 m ground area.

## 3. Sentinel-2

Sentinel-2 is a passive multispectral Earth-observation mission. Its MSI sensor measures solar radiation reflected from Earth's surface across visible, NIR and SWIR spectral bands. Because it is passive optical sensing, clouds can obstruct surface observations and it depends on solar illumination.

## 4. Sentinel-1

Complement Sentinel-2. Has it's own energy source - microwave. Active sensing capabilities. Can penetrate through clouds.

## 5. NDVI

Healthy green vegetation typically absorbs much of the incoming red radiation while strongly reflecting/scattering NIR. NDVI normalizes the contrast between these measurements to provide an indicator of vegetation greenness/vigor.

NDVI should be interpreted in context; a high NDVI value alone does not prove that vegetation is healthy, and temporal comparisons can be confounded by seasonality and other environmental or measurement conditions

## 6. CRS

A Coordinate Reference System (CRS) defines how a dataset's coordinates correspond to locations on Earth. Two datasets may represent the same physical location using different coordinate systems, so CRS compatibility must be considered before spatial comparison.

## 7. Raster Alignment

Raster alignment means that corresponding pixels from different rasters represent the same ground locations. Matching CRS and spatial resolution alone do not guarantee alignment; the placement of the pixel grids must also match.

## Sentinel-2 Product Selection

L1C vs L2A
L1C provides top-of-atmosphere (TOA) reflectance, where atmospheric effects are still present. L2A provides atmospherically corrected bottom-of-atmosphere (surface) reflectance estimates. L2A is therefore generally more suitable for comparing surface conditions over time.

Why AOI cloud conditions matter more than scene-wide cloud percentage
scene-wide cloud percentage being good doesn't guarantee our AOI being cloud free

Why seasonality matters in temporal comparison
Vegetation naturally changes across seasons, so comparing observations from very different times of year could make normal seasonal change look like environmental change. Comparing similar seasonal periods gives us a better reference.

Why observed NDVI change does not automatically establish causation
NDVI change alone does not establish causation because other factors such as drought, rainfall differences, flooding, agricultural cycles, land management, clouds/data-quality issues, or other land-cover changes could affect the measurement.
# NSIDC Projections

A repo containing projection and grid definitions for projections and grids
used by NSIDC.  Projections and grid definitions are in a Grid class.
The Grid class has `pyproj.CRS` and `affine.Affine` objects as attributes that
contain projection and grid definitions.  The Grid class has methods to generate
cartopy.crs objects, projected coordinates for each grid, and 2D latitude and longitude
arrays.

__Methods for gdal crs and rasterio srs will be added soon.__

Gridded data hosted by NSIDC are in a number of projections and grids.
These projections and grids are used widely by the Cryospheric
community.  However, projections are not always the standard
projections available in software packages.  Moreover, projection
definitions are sometimes hard to find.  Defining projections in
`cartopy` or `rasterio` is not always straight forward.

This repo is an attempt to solve these problems.

## NSIDC Projections
Gridded data at NSIDC are most commonly archived on two families of
projections: Polar Stereographic projections and Equal Area Scaleable
Earth (EASE) grids.  EASE-Grids are defined on north and south
Lambert's equal-area, azimuthal projections for polar regions,
and cylindrical equal-area projections for temperate regions and
global data. Both Polar Stereographic and EASE-Grids are available at
variety of grid resolutions.

The original EASE-Grids are defined on a spherical horizontal datum.
An EASE-Grid version 2 was defined using the WGS84 ellipsoid as the
horizontal datum to accomodate use of data in GIS packages.  GIS
software such as ArcGIS assumes all projections use WGS84 as a
horizonal datum.

NSIDC's Polar Stereographic projection differs from standard polar
stereographic projections used by `cartopy` etc in that the latitudes
of true scale are 70 N and 70 S, not 90 N and 90 S used in standard
definitions.  This is done to reduce distortion of the grid in the
marginal ice zones.

More information about EASE-Grid https://nsidc.org/data/ease
More information about Polar Stereographic data https://nsidc.org/data/polar-stereo

More information on projections and grids can be found at
https://nsidc.org/support/how/Points-Pixels-Grids-and-Cells-A-Mapping-and-Gridding-Primer

| Projection | Horizontal Datum | EPSG Code | Projection | proj4 string |
| :---- | :---- | :-----: | :---- | :----- |
| EASE-Grid North | 1924 Authalic Sphere | 3408 | Lambert Azimuthal | +proj=laea +lat_0=90 +lon_0=0 +x_0=0 +y_0=0 +a=6371228 +b=6371228 +units=m +no_defs |
| EASE-Grid South | 1924 Authalic Sphere | 3409 | Lambert Azimuthal | +proj=laea +lat_0=-90 +lon_0=0 +x_0=0 +y_0=0 +a=6371228 +b=6371228 +units=m +no_defs |
| EASE-Grid Global | 1924 Authalic Sphere | 3410 | Cylindrical Equal-Area | +proj=cea +lon_0=0 +lat_ts=30 +x_0=0 +y_0=0 +a=6371228 +b=6371228 +units=m +no_defs |
| EASE-Grid 2.0 North | WGS84 | 6931 | Lambert Azimuthal | +proj=laea +lat_0=90 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs |
| EASE-Grid 2.0 South | WGS84 | 6932 | Lambert Azimuthal | +proj=laea +lat_0=-90 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs |
| EASE-Grid 2.0 Global | WGS84 | 6933 | Cylindrical Equal-Area | +proj=cea +lon_0=0 +lat_ts=30 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs |
| Polar Stereographic North | Hughs 1980 | 3411 | Stereographic | +proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +a=6378273 +b=6356889.449 +units=m +no_defs |
| Polar Stereographic South | Hughs 1980 | 3412 | Stereographic | +proj=stere +lat_0=-90 +lat_ts=-70 +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378273 +b=6356889.449 +units=m +no_defs |
| WGS84 Polar Stereographic North | WGS84 | 3413 | Stereographic | +proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs |
| WGS84 Polar Stereographic South | WGS84 | 3976 | Stereographic | +proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs |



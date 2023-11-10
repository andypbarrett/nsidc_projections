"""Contains constants for EPSG"""
import pytest

from pyproj import CRS, Transformer
import cartopy.crs as ccrs
from osgeo import osr


NSIDC_EPSG_CODES = {
    3408: "NSIDC EASE-Grid North",
    3409: "NSIDC EASE-Grid South", 
    3410: "NSIDC EASE-Grid Global",
    6931: "WGS 84 / NSIDC EASE-Grid 2.0 North",
    6932: "WGS 84 / NSIDC EASE-Grid 2.0 South",
    6933: "WGS 84 / NSIDC EASE-Grid 2.0 Global",
    3411: "NSIDC Sea Ice Polar Stereographic North", 
    3412: "NSIDC Sea Ice Polar Stereographic South",
    3413: "WGS 84 / NSIDC Sea Ice Polar Stereographic North",
    3976: "WGS 84 / NSIDC Sea Ice Polar Stereographic South",
}

WGS84_EPSG = 4326

# Projected and geographic coordinates for NSIDC CRS
# Corners are derived from 25 km grid definitions
# N3B.gpd and S3B.gpd for Polar Stereographic and
# Nl.gpd and Sl.gpd for EASE-Grid

# North Polar Stereographic
NPS_GRID_CORNERS = [
    (-3850000., 5850000.),
    (3750000., 5850000.),
    (3750000., -5350000.),
    (-3850000., -5350000.)
]
NPS_MAPX_LATLON = [
    (30.980564, 168.349701),
    (31.365253, 102.339087),
    (34.345371, -9.972058),
    (33.924961, -80.739778),
]

# South Polar Stereographic



EASE_GRID_NORTH_MAPX_LATLON = [
    (-89.997996, 168.349701),
    (-89.997980, 102.339087),
    (-89.997852, -9.972058),
    (-89.997871, -80.739778),
]

EASE_GRID_NORTH_CORNERS = [
    (-9036842.762500001, 9036842.762500001),
    (9036842.762500001, 9036842.762500001),
    (9036842.762500001, -9036842.762500001),
    (-9036842.762500001, -9036842.762500001)
]


@pytest.mark.parametrize("epsg,target_crs_name", list(NSIDC_EPSG_CODES.items()))
def test_correct_crs_from_proj(epsg, target_crs_name):
    """Checks that CRS name returned from proj CRS 
    instantiation matches expected CRS name"""
    crs = CRS.from_epsg(epsg)
    result = crs.name
    assert result == target_crs_name


@pytest.mark.parametrize("epsg,target_crs_name", list(NSIDC_EPSG_CODES.items()))
def test_correct_crs_from_osgeo(epsg, target_crs_name):
    """Checks that CRS name returned from osgeo.osr CRS 
    instantiation matches expected CRS name"""
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(epsg)
    result = inSpatialRef.GetName()
    assert result == target_crs_name


@pytest.mark.parametrize("epsg,target_crs_name", list(NSIDC_EPSG_CODES.items()))
def test_correct_crs_from_cartopy(epsg, target_crs_name):
    """Checks that CRS name returned from cartopy CRS 
    instantiation matches expected CRS name"""
    crs = ccrs.epsg(epsg)
    result = crs.name
    assert result == target_crs_name

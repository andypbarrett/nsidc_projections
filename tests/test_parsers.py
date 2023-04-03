"""Tests for parsing gpd and mpp files"""

import pytest

import nsidc_projections.mapx.parse_mapx as mapx

# Test Cases for MPP parsing
MPP_CASE = [
    ("N200correct", {
        "Map Projection": "Azimuthal Equal-Area",
        "Map Reference Latitude": 90.0,
        "Map Reference Longitude": 0.0,
        "Map Rotation": 0.0,
        "Scale km per map unit": 200.5402,
        }
    ),
    ("Sps.mpp", {
        "Map Projection": "Polar Stereographic Ellipsoid",
        "Map Reference Latitude": -90.0,
        "Map Reference Longitude": 0.0,
        "Map Latitude True Scale": -70.0,
        "Map Rotation": 0.0,
        "Scale km per map unit": 100.,
        "Map Equatorial Radius": 6378273.,
        "Map Eccentricity": 0.081816153,
        }
    ),
    ("ramp.mpp", {
        "Map Projection": "Polar Stereographic Ellipsoid",
        "Map Reference Latitude": -90.0,
        "Map Reference Longitude": 0.0,
        "Map Latitude True Scale": -71.0,
        "Map Rotation": 0.0,
        "Scale km per map unit": 100.,
        "Map Equatorial Radius": 6378137.,
        "Map Eccentricity": 0.081819190843,
        }
    ),
    ]


GPD_CASE = [
    ("Nl", {
        **MPP_CASE[0][1],
        'Grid MPP File': 'N200correct.mpp',
        'Grid Width': 721,
        'Grid Height': 721,
        'Grid Cells per Map Unit': 8.,
        'Grid Map Origin Column': 360.0,
        'Grid Map Origin Row': 360.0,
        'Map Equatorial Radius': 6371228,
    }
    ),
    ("Nh", {
        **MPP_CASE[0][1],
        'Grid MPP File': 'N200correct.mpp',
        'Grid Width': 1441,
        'Grid Height': 1441,
        'Grid Cells per Map Unit': 16.,
        'Grid Map Origin Column': 720.0,
        'Grid Map Origin Row': 720.0,
        'Map Equatorial Radius': 6371228,
    #     'Map Origin X': -9030574.08,
    #     'Map Origin Y': 9030574.08,
    #     'Grid Map Units per Cell': 12533.76,
    },
    )
    ]


def test_make_gpd_path():
    gpdname = "Nl"
    target = "/home/apbarret/src/mapxmaps/Nl.gpd"
    result = mapx.make_gpd_path(gpdname)
    assert target == str(result)


def test_make_mpp_path():
    mpp_name = "N200correct.mpp"
    target = "/home/apbarret/src/mapxmaps/N200correct.mpp"
    result = mapx.make_mpp_path(mpp_name)
    assert target == str(result)


@pytest.mark.parametrize(
    "case,expected",
    GPD_CASE
)
def test_parse_gpd(case, expected):
    gpdname = case
    result = mapx.get_grid_definition(gpdname)
    assert result == expected


@pytest.mark.parametrize(
    "case,expected",
    MPP_CASE
)
def test_parse_mpp(case, expected):
    mpp_name = case
    result = mapx.parse_mpp(mpp_name)
    assert result == expected
    #print(result)
    #print(expected)


def test_calc_grid_map_units_per_cell():
    """Use Nl.gpd and Sl.gpd as test cases"""
    test = {
        "Scale km per map unit": 200.5402,
        'Grid Cells per Map Unit': 16.,
        }
    expected = 12533.7625
    result = mapx.calc_grid_map_units_per_cell(test)
    assert result == expected


def test_calc_map_origin_x():
    test ={
        "Grid Map Units per Cell": 12533.76,
        "Grid Map Origin Column": 720.0,
        }
    expected = -9030574.08
    result = mapx.calc_map_origin_x(test)
    assert expected == result


def test_calc_map_origin_y():
    test ={
        "Grid Map Units per Cell": 12533.76,
        "Grid Map Origin Row": 720.0,
        }
    expected = 9030574.08
    result = mapx.calc_map_origin_y(test)
    assert expected == result

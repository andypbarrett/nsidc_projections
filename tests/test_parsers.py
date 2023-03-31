"""Tests for parsing gpd and mpp files"""

import pytest

from nsidc_projections.mapx.parse_mapx import parse_gpd, make_gpd_path, make_mpp_path, parse_mpp


def test_make_gpd_path():
    gpdname = "Nl"
    target = "/home/apbarret/src/mapxmaps/Nl.gpd"
    result = make_gpd_path(gpdname)
    assert target == str(result)


def test_make_mpp_path():
    mpp_name = "N200correct.mpp"
    target = "/home/apbarret/src/mapxmaps/N200correct.mpp"
    result = make_mpp_path(mpp_name)
    assert target == str(result)


def test_parse_gpd():
    gpdname = "Nl"
    target = {
        'Grid MPP File': 'N200correct.mpp',
        'Grid Width': 721,
        'Grid Height': 721,
        'Grid Cells per Map Unit': 8.,
        'Grid Map Origin Column': 360.0,
        'Grid Map Origin Row': 360.0,
    }
    result = parse_gpd(gpdname)
    assert result == target


@pytest.mark.parametrize(
    "case",
    ["N200correct", "Sps.mpp", "ramp.mpp"]
)
def test_parse_mpp(case):
    mpp_name = case
    result = parse_mpp(mpp_name)
    print(result)

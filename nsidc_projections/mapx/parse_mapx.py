"""Readers and parsers for mapx gpd and mpp files"""
import re

import numpy as np

import pyproj
import cartopy.crs as ccrs

from nsidc_projections.filepath import MAPXMAPS_PATH
from nsidc_projections.mapx.constants import (MAP_EQUATORIAL_RADIUS,
                                              Expected_Missing_Radius,
                                              km2m)


class GPDefinition():
    """Class to hold MAPX projection and grid definition"""
    def __init__(self):
        self.map_projection = None
        self.map_reference_latitude = np.nan
        self.map_reference_longitude = np.nan
        self.map_latitude_true_scale = np.nan
        self.map_rotation = np.nan
        self.map_equatorial_radius = np.nan
        self.map_eccentricity = np.nan
        self.map_origin_x = np.nan  # meters
        self.map_origin_y = np.nan  # meters
        self.grid_map_origin_column = np.nan
        self.grid_map_origin_row = np.nan
        self.grid_map_units_per_cell = np.nan  # meters
        self.grid_width = 0
        self.grid_height = 0
        self.cell_width = 0  # meters
        self.cell_height = 0  # meters


    def __str__(self):
        return (f"Map Projection:                     {self.map_projection}\n"
                f"Map Reference Latitude:             {self.map_reference_latitude:5.1f} degrees\n"
                f"Map Reference Longitude:            {self.map_reference_longitude:5.1f} degrees\n"
                f"Map Latitude True Scale:            {self.map_latitude_true_scale:5.1f} degrees\n"
                f"Map Rotation:                       {self.map_rotation:6.1f}\n"
                f"Map Equatorial Radius:              {self.map_equatorial_radius:9.1f} meters\n"
                f"Map Eccentricity:                   {self.map_eccentricity:14.12f}\n"
                f"Map Origin X:                       {self.map_origin_x:12.1f} meters\n"
                f"Map Origin Y:                       {self.map_origin_y:12.1f} meters\n"
                f"Grid Map Origin Column:             {self.grid_map_origin_column:8.3f}\n"
                f"Grid Map Origin Row:                {self.grid_map_origin_row:8.3f}\n"
                f"Grid Map Units per Cell:            {self.grid_map_units_per_cell:9.2f} meters\n"
                f"Grid Width:                         {self.grid_width:5d}\n"
                f"Grid Height:                        {self.grid_height:5d}\n"
                f"Cell Width:                         {self.cell_width:10.3f} meters\n"
                f"Cell Height:                        {self.cell_height:10.3f} meters\n")


    def from_gpd(self, gpd_name):
        """Initializes from a gpd file"""
        params = get_grid_definition(gpd_name)
        self.map_projection = params.get('Map Projection', None)
        self.map_reference_latitude = params.get('Map Reference Latitude', np.nan)
        self.map_reference_longitude = params.get('Map Reference Longitude', np.nan)
        self.map_rotation = params.get('Map Rotation', np.nan)
        self.map_equatorial_radius = params.get('Map Equatorial Radius', np.nan)
        self.map_eccentricity = params.get('Map Eccentricity', np.nan)
        self.map_origin_x = params.get('Map Origin X', np.nan)
        self.map_origin_y = params.get('Map Origin Y', np.nan)
        self.grid_map_origin_column = params.get('Grid Map Origin Column', np.nan)
        self.grid_map_origin_row = params.get('Grid Map Origin Row', np.nan)
        self.grid_map_units_per_cell = params.get('Grid Cells per Map Unit', np.nan)
        self.grid_width = params.get('Grid Width', 0)
        self.grid_height = params.get('Grid Height', 0)
        self.cell_width = params.get('Cell Width', 0)
        self.cell_height = params.get('Cell Height', 0)
        

def make_gpd_path(gpdname):
    """Returns a Path object for gpd"""
    if ".gpd" not in gpdname:
        return MAPXMAPS_PATH / (gpdname + ".gpd")
    else:
        return MAPXMAPS_PATH / gpdname


def make_mpp_path(mpp_name):
    """Returns a Path object to mpp"""
    if ".mpp" not in mpp_name:
        return MAPXMAPS_PATH / (mpp_name + ".mpp")
    else:
        return MAPXMAPS_PATH / mpp_name


def parse_grid_mpp_file(s):
    return {'Grid MPP File': s}


def parse_column_rows(s):
    keys = ['Grid Width', 'Grid Height']
    return {k: int(v) for k, v in zip(keys, s.split())}


def parse_grid_cells_per_map_unit(s):
    return {'Grid Cells per Map Unit': float(s)}


def parse_map_origin_col_row(s):
    keys = ['Grid Map Origin Column', 'Grid Map Origin Row']
    return {k: float(v) for k, v in zip(keys, s.split())}


gpd_parser = {
    'map projection parameters': parse_grid_mpp_file,
    'columns rows': parse_column_rows,
    'map origin column,row': parse_map_origin_col_row,
    'grid cells per map unit': parse_grid_cells_per_map_unit,
}


def parse_lat0_lon0(s):
    keys = ["Map Reference Latitude", "Map Reference Longitude"]
    return {k: float(v) for k, v in zip(keys, s.split())}


def parse_lat0_lon0_lat1(s):
    keys = ["Map Reference Latitude", "Map Reference Longitude", "Map Latitude True Scale"]
    return {k: float(v) for k, v in zip(keys, s.split())}


def parse_rotation(s):
    return {"Map Rotation": float(s)}


def parse_scale(s):
    return {"Scale km per map unit": float(s)}


def parse_earth_radius(s):
    return {"Map Equatorial Radius": float(s)*km2m}


def parse_eccentricity(s):
    return {"Map Eccentricity": float(s)}


mpp_parser = {
    "lat0 lon0": parse_lat0_lon0,
    "lat0 lon0 lat1": parse_lat0_lon0_lat1,
    "rotation": parse_rotation,
    "scale (km/map unit)": parse_scale,
    "Earth equatorial radius (km)": parse_earth_radius,
    "eccentricity": parse_eccentricity,
    }


def get_mpp_fields(lines):
    """Returns a dictionary of mpp parameters from each line"""
    these_fields = ['lat0 lon0', 'lat0 lon0 lat1', 'rotation', 'scale (km/map unit)',
                    'Earth equatorial radius (km) -- wgs84', 'eccentricity -- wgs84',
                    'Earth equatorial radius (km)', 'eccentricity']

    def as_pair(line):
        """Create key value tuple"""
        arr = re.split("\t+", line.strip())
        key = arr[-1].split(' -- ')[0]
        value = " ".join([s.strip() for s in arr[:-1] if s.strip() != ""])
        return (key, value)
    
    fields = {}
    for line in lines:
        key, value = as_pair(line)
        if key in these_fields:
            fields.update(mpp_parser[key](value))
    return fields


def parse_mpp(mpp_name):
    """Parses a mpp definition file

    :mpp_name: name of mpp file - normally defined in orig gpd_name

    :returns: a dictionary of projection parameters
    """
    path_to_mpp = make_mpp_path(mpp_name)
    with open(path_to_mpp, "r") as f:
        lines = f.readlines()
    fields = {}
    fields["Map Projection"] = lines[0].strip().title()
    fields.update(get_mpp_fields(lines))
    return fields


def parse_original_gpd(lines):
    """Parses an original-style gpd file"""
    fields = {}
    for line in lines:
        value, key = re.split("\t+", line.strip())[:2]
        fields.update(gpd_parser[key](value))
    fields.update(parse_mpp(fields["Grid MPP File"]))
    return fields


def get_equatorial_radius(params):
    """Returns missing equatorial radius for projection

    !!!This should only be for original EASE-Grid!!!
    """
    if params["Map Projection"] not in Expected_Missing_Radius:
        raise KeyError(f"Unexpected projection {params['Map Projection']} for missing radius")
    params["Map Equatorial Radius"] = MAP_EQUATORIAL_RADIUS[params["Map Projection"]]


def calc_missing_parameters(params):
    """Calculates or fills in missing parameters"""
    if "Map Equatorial Radius" not in params:
        get_equatorial_radius(params)
    if "Map Units per Cell" not in params:
        params["Map Units per Cell"] = calc_grid_map_units_per_cell(params)
    if "Cell Width" not in params:
        params["Cell Width"] = params["Map Units per Cell"]
    if "Cell Height" not in params:
        params["Cell Height"] = -1. * params["Map Units per Cell"]
    if "Map Origin X" not in params:
        params["Map Origin X"] = calc_map_origin_x(params)
    if "Map Origin Y" not in params:
        params["Map Origin Y"] = calc_map_origin_y(params)
    return params


def calc_map_origin_x(params):
    """Calculates the Map Origin of the x-axis
    
    Add 0.5 t0 column

    See https://nsidc.org/data/user-resources/help-center/mapping-and-gridding-primer-points-pixels-grids-and-cells#anchor-1 for discussion of column, row coords
    """
    return -1 * params["Map Units per Cell"] * (params["Grid Map Origin Column"] + 0.5)


def calc_map_origin_y(params):
    """Calculates the Map Origin of the y-axis
    
    Add 0.5 t0 row

    See https://nsidc.org/data/user-resources/help-center/mapping-and-gridding-primer-points-pixels-grids-and-cells#anchor-1 for discussion of column, row coords
    """
    return params["Map Units per Cell"] * (params["Grid Map Origin Row"] + 0.5)


def calc_grid_map_units_per_cell(params):
    """Calculate the grid cell size - expected in meters"""
    map_units_per_cell = params["Scale km per map unit"] * km2m / params["Grid Cells per Map Unit"]
    return map_units_per_cell


def get_grid_definition(gpdname):
    """Parses a gpd definition file

    :path_to_gpd: str or Path object to gpd file

    :returns: dict containing parameters
    """
    path_to_gpd = make_gpd_path(gpdname)
    with open(path_to_gpd, "r") as f:
        lines = f.readlines()
    if 'map projection parameters' in lines[0]:
        params = parse_original_gpd(lines)
        params = calc_missing_parameters(params)
    else:
        raise NotImplementedError("Parser for new format gpd coming soon!")
    return params


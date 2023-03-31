"""Readers and parsers for mapx gpd and mpp files"""
import re

import numpy as np

import pyproj
import cartopy.crs as ccrs

from nsidc_projections.filepath import MAPXMAPS_PATH


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


    def __str__(self):
        return (f"Map Projection:                     {self.map_projection}\n"
                f"Map Reference Latitude:             {self.map_reference_latitude:5.1f}\n"
                f"Map Reference Longitude:            {self.map_reference_longitude:5.1f}\n"
                f"Map Latitude True Scale:            {self.map_latitude_true_scale:5.1f}\n"
                f"Map Rotation:                       {self.map_rotation:6.1f}\n"
                f"Map Equatorial Radius:              {self.map_equatorial_radius:9.1f}\n"
                f"Map Eccentricity:                   {self.map_eccentricity:14.12f}\n"
                f"Map Origin X:                       {self.map_origin_x:12.1f} ; meters\n"
                f"Map Origin Y:                       {self.map_origin_y:12.1f} ; meters\n"
                f"Grid Map Origin Column:             {self.grid_map_origin_column:8.3f}\n"
                f"Grid Map Origin Row:                {self.grid_map_origin_row:8.3f}\n"
                f"Grid Map Units per Cell:            {self.grid_map_units_per_cell:9.2f} ; meters\n"
                f"Grid Width:                         {self.grid_width:5d}\n"
                f"Grid Height:                        {self.grid_height:5d}\n")


    def from_gpd(self, gpd_name):
        """Initializes from a gpd file"""
        result = parse_gpd(gpd_name)
        self.map_projection = result.get('Map Projection', None)
        self.map_reference_latitude = result.get('Map Reference Latitude', np.nan)
        self.map_reference_longitude = result.get('Map Reference Longitude', np.nan)
        self.map_rotation = result.get('Map Rotation', np.nan)
        self.map_equatorial_radius = result.get('Map Equatorial Radius', np.nan)
        self.map_eccentricity = result.get('Map Eccentricity', np.nan)
        self.map_origin_x = result.get('Map Origin X', np.nan)
        self.map_origin_y = result.get('Map Origin Y', np.nan)
        self.grid_map_origin_column = result.get('Grid Map Origin Column', np.nan)
        self.grid_map_origin_row = result.get('Grid Map Origin Row', np.nan)
        self.grid_map_units_per_cell = result.get('Grid Map Units per Cell', np.nan)
        self.grid_width = result.get('Grid Width', 0)
        self.grid_height = result.get('Grid Height', 0)
        


def make_gpd_path(gpdname):
    """Returns a Path object for gpd"""
    if ".gpd" not in gpdname:
        fgpd = gpdname + ".gpd"
    return MAPXMAPS_PATH / fgpd


def make_mpp_path(mpp_name):
    """Returns a Path object to mpp"""
    if ".mpp" not in mpp_name:
        fmpp = mpp_name + ".mpp"
    return MAPXMAPS_PATH / fmpp


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


def parse_mpp(mpp_name):
    """Parses a mpp definition file

    :mpp_name: name of mpp file - normally defined in orig gpd_name

    :returns: a dictionary of projection parameters
    """
    path_to_mpp = make_mpp_path(mpp_name)

    

def parse_original_gpd(lines):
    """Parses an original-style gpd file"""
    fields = {}
    for line in lines:
        value, key = re.split("\t+", line.strip())[:2]
        fields.update(gpd_parser[key](value))
    return fields


def parse_gpd(gpdname):
    """Parses a gpd definition file

    :path_to_gpd: str or Path object to gpd file

    :returns: dict containing parameters
    """
    path_to_gpd = make_gpd_path(gpdname)
    with open(path_to_gpd, "r") as f:
        lines = f.readlines()
    if 'map projection parameters' in lines[0]:
        result = parse_original_gpd(lines)
    return result


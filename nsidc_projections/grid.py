"""Classes for NSIDC Grids"""

import numpy as np

from pyproj import CRS, Transformer
from affine import Affine
import cartopy.crs as ccrs

import grid_info

# Need to add cylindrical projection
keymap_projclass = {
    'laea': ccrs.LambertAzimuthalEqualArea,
    'stere': ccrs.Stereographic,
    }

keymap_projparam = {
    'lat_0': 'central_latitude',
    'lon_0': 'central_longitude',
    'lat_ts': 'true_scale_latitude',
    'x_0': 'false_easting',
    'y_0': 'false_northing',
    }

keymap_globeparam = {
    'R': 'semimajor_axis',
    'a': 'semimajor_axis',
    'b': 'semiminor_axis',
    }


def get_proj_params(proj_dict):
    """Returns dictionary of cartopy projection parameters"""
    ccrs_projparam = {}
    for k, v in keymap_projparam.items():
        if k in proj_dict:
            ccrs_projparam[v] = proj_dict[k]
    return ccrs_projparam


def get_globe_params(proj_dict):
    """Returns dictionary of cartopy globe parameters"""
    ccrs_globeparam = {
        'datum': None,
        'ellipse': None,
        }
    for k, v in keymap_globeparam.items():
        if k in proj_dict:
            ccrs_globeparam[v] = proj_dict[k]
    return ccrs_globeparam


def get_cartopy_projclass(proj_name):
    """Returns cartopy projection definition"""
    try:
        cartopy_projclass = keymap_projclass[proj_name]
        return cartopy_projclass
    except KeyError:
        print(f"{proj_name} is not available")


def to_cartopy(proj_crs):
    """Returns a cartopy crs"""
    proj_dict = proj_crs.to_dict()
    cartopy_projclass = get_cartopy_projclass(proj_dict['proj'])
    kw_proj = get_proj_params(proj_dict)
    kw_globe = get_globe_params(proj_dict)
    globe = ccrs.Globe(**kw_globe)
    cartopy_crs = cartopy_projclass(**kw_proj, globe=globe)
    return cartopy_crs


class Grid:
    """Basic grid class"""
    def __init__(self, grid_tuple):
        self.name = grid_tuple.name
        self.epsg = grid_tuple.epsg
        self.rows = grid_tuple.rows
        self.cols = grid_tuple.cols
        self.cell_width = grid_tuple.cell_width
        self.cell_height = grid_tuple.cell_height
        self.upper_left_x = grid_tuple.upper_left_x
        self.upper_left_y = grid_tuple.upper_left_y

        self.crs = CRS.from_epsg(grid_tuple.epsg)


    def __str__(self):
        return ("Grid object\n"
                f"name: {self.name}\n"
                f"EPSG: {self.epsg}\n"
                f"rows: {self.rows}\n"
                f"cols: {self.cols}\n"
                f"cell width: {self.cell_width}\n"
                f"cell height: {self.cell_height}\n"
                f"upper-left x: {self.upper_left_x}\n"
                f"upper-left y: {self.upper_left_y}\n"
                )


    def geotransform(self):
        """Return Affine matrix"""
        return Affine(
            self.cell_width,
            0.,
            self.upper_left_x,
            0.,
            -1. * self.cell_height,
            self.upper_left_y
            )


    def get_coordinates(self):
        """Return x and y coordinates for grid
        
        Note: for EASE-Grid these may be undefined"""
        c = np.arange(0.5, self.cols, 1.)
        r = np.arange(0.5, self.rows, 1.)
        x, y = self.geotransform() * (c, r)
        return x, y


    def get_latlon(self):
        """Return 2D grids of latitude and longitudes"""
        x, y = self.get_coordinates()
        x2d, y2d = np.meshgrid(x, y)
        proj2latlon = Transformer.from_crs(self.crs, self.crs.geodetic_crs)
        lat, lon = proj2latlon.transform(x2d, y2d)
        return lat, lon


    def to_cartopy(self):
        return to_cartopy(self.crs)

    
EASEGridNorth25km = Grid(grid_info.EASEGridNorth25km)
SSMI_PolarStereoNorth25km = Grid(grid_info.SSMI_PolarStereoNorth25km)

"""Classes for NSIDC Grids"""

import numpy as np

from pyproj import CRS, Transformer
from affine import Affine

import grid_info

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

    
EASEGridNorth25km = Grid(grid_info.EASEGridNorth25km)

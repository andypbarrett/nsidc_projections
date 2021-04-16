"""Contains proj4 CRS definitions for NSIDC projections"""

from pyproj import CRS
import grid_info

EASEGridNorth = CRS.from_epsg(grid_info.EASE_GRID_NORTH_EPSG)
EASEGridSouth = CRS.from_epsg(grid_info.EASE_GRID_SOUTH_EPSG)
EASEGridGlobal = CRS.from_epsg(grid_info.EASE_GRID_GLOBAL_EPSG)
EASEGrid2North = CRS.from_epsg(grid_info.EASE_GRID2_NORTH_EPSG)
EASEGrid2South = CRS.from_epsg(grid_info.EASE_GRID2_SOUTH_EPSG)
EASEGrid2Global = CRS.from_epsg(grid_info.EASE_GRID2_GLOBAL_EPSG)

PolarStereoNorth = CRS.from_epsg(grid_info.POLAR_STEREO_NORTH_EPSG)
PolarStereoSouth = CRS.from_epsg(grid_info.POLAR_STEREO_SOUTH_EPSG)
PolarStereoNorthWGS84 = CRS.from_epsg(grid_info.POLAR_STEREO_NORTH_WGS84_EPSG)
PolarStereoSouthWGS84 = CRS.from_epsg(grid_info.POLAR_STEREO_SOUTH_WGS84_EPSG)

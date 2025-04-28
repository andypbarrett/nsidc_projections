"""Contains projection and grid constants"""
from collections import namedtuple

import numpy as np

Grid = namedtuple(
    "Grid",
    [
        "name",
        "epsg",
        "cols",
        "rows",
        "cell_width",
        "cell_height",
        "upper_left_x",
        "upper_left_y"
        ]
)

# Original EASE Grid grid cell width and height are
# fraction of equatorial radius set to span equator with
# whole number of cells (Brodzik et al, 2012).  
EASE_GRID_MAP_SCALE = 200.5402e3  # km/map unit - N200correct.mpp
EASE_GRID_CELLS_PER_MAP_UNIT = 8  # For 25 km grid - Nl.gpd
EASE_GRID25_WIDTH = EASE_GRID_MAP_SCALE / EASE_GRID_CELLS_PER_MAP_UNIT
EASE_GRID25_HEIGHT = -1. * EASE_GRID_MAP_SCALE / EASE_GRID_CELLS_PER_MAP_UNIT


EASE_GRID_NORTH_EPSG = 3408
EASE_GRID_SOUTH_EPSG = 3409
EASE_GRID_GLOBAL_EPSG = 3410
EASE_GRID2_NORTH_EPSG = 6931
EASE_GRID2_SOUTH_EPSG = 6932
EASE_GRID2_GLOBAL_EPSG = 6933
POLAR_STEREO_NORTH_EPSG = 3411
POLAR_STEREO_SOUTH_EPSG = 3412
POLAR_STEREO_NORTH_WGS84_EPSG = 3413
POLAR_STEREO_SOUTH_WGS84_EPSG = 3976

IMS_NORTH_POLAR_STEREO_WKT = """PROJCRS["unknown",
    BASEGEOGCRS["unknown",
        DATUM["unknown",
            ELLIPSOID["unknown",6378137,291.505347349177,
                LENGTHUNIT["metre",1,
                    ID["EPSG",9001]]]],
        PRIMEM["Greenwich",0,
            ANGLEUNIT["degree",0.0174532925199433],
            ID["EPSG",8901]]],
    CONVERSION["unnamed",
        METHOD["Polar Stereographic (variant B)",
            ID["EPSG",9829]],
        PARAMETER["Latitude of standard parallel",60,
            ANGLEUNIT["degree",0.0174532925199433],
            ID["EPSG",8832]],
        PARAMETER["Longitude of origin",-80,
            ANGLEUNIT["degree",0.0174532925199433],
            ID["EPSG",8833]],
        PARAMETER["False easting",0,
            LENGTHUNIT["metre",1],
            ID["EPSG",8806]],
        PARAMETER["False northing",0,
            LENGTHUNIT["metre",1],
            ID["EPSG",8807]]],
    CS[Cartesian,2],
        AXIS["easting",south,
            ORDER[1],
            LENGTHUNIT["metre",1,
                ID["EPSG",9001]]],
        AXIS["northing",south,
            ORDER[2],
            LENGTHUNIT["metre",1,
                ID["EPSG",9001]]]]
"""

EASEGridNorth25km = Grid(
    name ="EASE-Grid North 25 km",
    epsg =EASE_GRID_NORTH_EPSG,
    cols =721,
    rows =721,
    cell_width = EASE_GRID25_WIDTH,
    cell_height = EASE_GRID25_HEIGHT,
    upper_left_x = np.round(-1 * EASE_GRID25_WIDTH * (721/2), 6),
    upper_left_y = np.round(-1 * EASE_GRID25_HEIGHT * (721/2), 6),
    )

EASEGridSouth25km = Grid(
    name = "EASE-Grid South 25 km",
    epsg = EASE_GRID_SOUTH_EPSG,
    cols = 721,
    rows = 721,
    cell_width = EASE_GRID25_WIDTH,
    cell_height = EASE_GRID25_HEIGHT,
    upper_left_x = np.round(-1 * EASE_GRID25_WIDTH * (721/2), 6),
    upper_left_y = np.round(-1 * EASE_GRID25_HEIGHT * (721/2), 6),
    )

EASEGridGlobal25km = Grid(
    name = "EASE-Grid Global 25 km",
    epsg = EASE_GRID_GLOBAL_EPSG,
    cols = 1383,
    rows = 586,
    cell_width = EASE_GRID25_WIDTH,
    cell_height = EASE_GRID25_HEIGHT,
    upper_left_x = np.round(-1 * EASE_GRID25_HEIGHT * (1383/2), 6),
    upper_left_y = np.round(-1 * EASE_GRID25_HEIGHT * (586/2), 6),
    )

EASEGrid2Global25km = Grid(
    name="EASE-Grid 2.0 Global 25 km",
    epsg=EASE_GRID2_GLOBAL_EPSG,
    cols=1388,
    rows=584,
    cell_width=25025.26,
    cell_height=-25025.26,
    upper_left_x=-17367530.45,
    upper_left_y=7307375.92
    )

EASEGrid2North25km = Grid(
    name="EASE-Grid 2.0 North 25 km",
    epsg=EASE_GRID2_NORTH_EPSG,
    cols=720,
    rows=720,
    cell_width=25000.,
    cell_height=-25000.,
    upper_left_x=-9000000.0,
    upper_left_y=9000000.0
    )

EASEGrid2South25km = Grid(
    name="EASE-Grid 2.0 South 25 km",
    epsg=EASE_GRID2_SOUTH_EPSG,
    cols=720,
    rows=720,
    cell_width=25000.,
    cell_height=-25000.,
    upper_left_x=-9000000.0,
    upper_left_y=9000000.0
    )

AVHRR_EASEGridNorth25km = Grid(
    name="AVHRR EASE-Grid North 25 km (Na25)",
    epsg=EASE_GRID_NORTH_EPSG,
    cols=361,
    rows=361,
    cell_width=EASE_GRID25_WIDTH,
    cell_height=EASE_GRID25_HEIGHT,
    upper_left_x=-4524683.8,
    upper_left_y=4524683.8
    )

AVHRR_EASEGridSouth25km = Grid(
    name="AVHRR EASE-Grid South 25 km (Sa25)",
    epsg=EASE_GRID_SOUTH_EPSG,
    cols=321,
    rows=321,
    cell_width=EASE_GRID25_WIDTH,
    cell_height=EASE_GRID25_HEIGHT,
    upper_left_x=-4023333.8,
    upper_left_y=4023333.8
    )

SSMI_PolarStereoNorth25km = Grid(
    name="SSM/I Polar Stereographic North 25 km (N3B)",
    epsg=POLAR_STEREO_NORTH_EPSG,
    cols=304,
    rows=448,
    cell_width=25000.,
    cell_height=-25000.,
    upper_left_x=-3850000.,
    upper_left_y=5850000.
    )

SSMI_PolarStereoSouth25km = Grid(
    name="SSM/I Polar Stereographic South 25 km (S3B)",
    epsg=POLAR_STEREO_SOUTH_EPSG,
    cols=316,
    rows=332,
    cell_width=25000.,
    cell_height=-25000.,
    upper_left_x=-3950000.,
    upper_left_y=4350000.,
    crs=None,
    )

IMS4km = Grid(
    name="IMS 4km",
    epsg=None,
    cols=6144,
    rows=6144,
    cell_width=4000.,
    cell_height=4000.,
    upper_left_x=-12288000.0,
    upper_left_y=-12288000.0,
    crs=IMS_NORTH_POLAR_STEREO_WKT,
    )

IMS1km = Grid(
    name="IMS 1km",
    epsg=None,
    cols=24576,
    rows=24576,
    cell_width=1000.,
    cell_height=1000.,
    upper_left_x=-12288000.0,
    upper_left_y=-12288000.0,
    crs=IMS_NORTH_POLAR_STEREO_WKT,
    )

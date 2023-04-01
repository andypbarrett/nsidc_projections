"""Constants for mapx grid definitions

These are parameters that are missing
"""
import numpy as np


km2m = 1e3


Expected_Missing_Radius = [
    "Azimuthal Equal-Area"
    ]

ELLIPSOID = {
    "International_1924_Authalic_Sphere": {
        "Radius": 6371228.,
        }
    }

MAP_EQUATORIAL_RADIUS = {
    "Azimuthal Equal-Area": ELLIPSOID.get("International_1924_Authalic_Sphere").get("Radius", np.nan),
    }

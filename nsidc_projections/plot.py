"""Code to plot extent"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyproj import CRS

def make_cartopy_crs(epsg_code):
    """Makes a cartopy crs using proj strings.  proj strings are returned from proj CRS
    This is done because defining CRS from epsg does no create correct bounds"""
    proj_params = CRS.from_epsg(epsg_code).to_dict()
    
    proj2ctopy = {'a': 'semimajor_axis', 'b': 'semiminor_axis'}  # Converts proj parameter names to cartopy Globe keywords

    # Make the globe instance
    globe = ccrs.Globe(**{**{'ellipse': None}, **{proj2ctopy[k]: v for k, v in proj_params.items() if k in ['a', 'b']}})  # Must set ellipse explicitly to None otherwise is wgs84
    crs = ccrs.Projection({k: v for k, v in proj_params.items() if k not in ['a', 'b']}, globe=globe)
    return crs


#def plot_projected_extent(crs):

    

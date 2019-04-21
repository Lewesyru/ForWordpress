# ---------------------------------------------------------------------------
# Author: Yi Ru
# Created on: 2017-12-06
# Description: Read raster images from the resources folder, then create NDVI
#              images for each of them. And then change the spatial resolution
#              to 90m, and finally reclassify each image into four classes.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy.sa import *

# Setup environment
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = "Z:\\Resources\\RasterData_Lab6"
arcpy.env.overwriteOutput = True

# Create a new folder to save the NDVI images
outputPath = arcpy.CreateFolder_management("Z:\\Personal\\yru", "output")
arcpy.env.scratchWorkspace = str(outputPath)    # Setting scratch workspace to save temp data

# Reading raster in the workspace
rasterlist = arcpy.ListRasters()
for IMG in rasterlist:
    Red = arcpy.Raster(IMG + "\\Layer_3")    # Assign band 3 to red band
    NIR = arcpy.Raster(IMG + "\\Layer_4")    # Assign band 4 to NIR band

    # Generating NDVI
    temp_num = Float(NIR - Red)     # Temp numerator
    temp_deno = Float(NIR + Red)    # Temp denominator
    ndvi = Con(temp_deno != 0, temp_num / temp_deno, -9999)
    ndvi.save(str(outputPath) + "\\%s_ndvi.tif" % IMG[:-4])     # Save image with a formatted name

    # Aggregate images
    aggr = Aggregate(ndvi, 3, "MEAN")   # Change resolution with 3 as the factor, 30 * "3" = 90 m
    aggr.save(str(outputPath) + "\\%s_aggr.tif" % IMG[:-4])

    # Reclassify images
    remap = RemapValue([[-1, -0.5, 1], [-0.5, 0, 2],
                        [0, 0.5, 3], [0.5, 1, 4]])     # Setting up the bins. Actually no value is
    reclass = Reclassify(aggr, "Value", remap)         # less than 0 in the ndvi image.
    reclass.save(str(outputPath) + "\\%s_reclass.tif" % IMG[:-4])



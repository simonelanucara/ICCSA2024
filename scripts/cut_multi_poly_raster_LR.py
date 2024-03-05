import os
from osgeo import gdal, ogr

#def ClipRasterWithPolygon():
#	os.system("gdalwarp -crop_to_cutline -cutline" + polyPath + rasterPath + outhPath)
#	os.system("gdalwarp -crop_to_cutline -cutline /home/jovyan/work/ClippingFeatures/106/clip.shp /home/jovyan/work/infolder/S2_20160718_022_32TQQ3_A_NDVI.tif /home/jovyan/work/ClippingFeatures/106/raster.tif")

def CreateClippingRastersPolygons(inPath, field):
    inPath = ('/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/mais_2023.shp')
    driverSHP = ogr.GetDriverByName("Esri Shapefile")
    ds = ogr.Open(inPath)
    if ds is None:
        print ('layer not open')
    else:
        lyr = ds.GetLayer()
        spatialRef = lyr.GetSpatialRef()
        for feature in lyr:
            fieldVal=feature.GetField('id_geom')
            os.mkdir("/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/ClippingFeatures/" + str(fieldVal))
            outds = driverSHP.CreateDataSource("/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/ClippingFeatures/" + str(fieldVal) + "/clip.shp")
            outlyr = outds.CreateLayer(str(fieldVal) + "/clip.shp", srs=spatialRef, geom_type=ogr.wkbPolygon)
            outDfn = outlyr.GetLayerDefn()
            ingeom = feature.GetGeometryRef()
            outFeat = ogr.Feature(outDfn)
            outFeat.SetGeometry(ingeom)
            outlyr.CreateFeature(outFeat)
            for sentinel in os.listdir('/home/jovyan/work/ICCSA2024/Data/32TQQ3/'):
                if sentinel.endswith('.tif'):
                    rastername = sentinel
                    raster = ('/home/jovyan/work/ICCSA2024/Data/32TQQ3/'+ str(rastername))
                    output = ("/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/ClippingFeatures/" + str(fieldVal) + "/" + str(fieldVal) + "_" +  str(rastername))
                    os.system("gdalwarp -crop_to_cutline -cutline " + "/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/ClippingFeatures/" + str(fieldVal) + "/clip.shp" + " " + raster + " " + output)

#run
os.mkdir("/home/jovyan/work/ICCSA2024/Data/piano_colturale_2023/ClippingFeatures")
CreateClippingRastersPolygons("nome_raster.shp", "nome_12")

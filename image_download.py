import urllib.request
import datetime
from calendar import monthrange
#Worldview NASA: every day
#time (December 2007 - February 2017)
years = range(2007,2018)
#years = [2008, 2009]
months = [1,2,12]
#months = [12]

PATH = '/local/S.Rasp/MPI_Aqua_v2/'

lon1 = -60; lon2 = -20
lat1 = 5; lat2 = 25
dlon = lon2 - lon1
dlat = lat2 - lat1
deg2pix = 1140/20
loc= (f'&extent={lon1},{lat1},{lon2},{lat2}')
size = (f'&width={int(dlon * deg2pix)}&height={int(dlat * deg2pix)}')
layer = ('&layers=MODIS_Aqua_CorrectedReflectance_TrueColor,Coastlines')

idate = datetime.datetime(2007,12,1)
for yr in years:
  for m in months:
    if yr == years[0] and m == 1:
      False
    elif yr == years[0] and m == 2:
      False
    elif yr == years[-1] and m == 12:
      False
    else: 
      nday = monthrange(yr,m)[1]
      #nday = 2
      for nd in range(1,nday+1):
        date = datetime.datetime(yr, m, nd)
        d = str(date.strftime('%j'))
        print(date.strftime('%y %m %d'))
        url = 'https://gibs.earthdata.nasa.gov/image-download?TIME='+str(yr)+d+loc+'&epsg=4326'+layer+'&opacities=1,1&worldfile=false&format=image/png'+size
        urllib.request.urlretrieve(url,PATH+'Aqua_CorrectedReflectance'+str(yr)+date.strftime('%m')+'{:02d}'.format(date.day)+'.png')

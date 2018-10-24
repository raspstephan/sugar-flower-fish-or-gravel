"""
Script to download images from NASA Worldview
"""
import urllib.request
import datetime
from calendar import monthrange
import fire
import os


def download_imgs(year_range, months, save_path, lon_range, lat_range,
                  deg2pix=100, satellite='Aqua', exist_skip=False):
    os.makedirs(save_path, exist_ok=True)

    lon1 = lon_range[0]; lon2 = lon_range[1]
    lat1 = lat_range[0]; lat2 = lat_range[1]
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    loc= (f'&extent={lon1},{lat1},{lon2},{lat2}')
    loc_str = f'_{lon1}-{lon2}_{lat1}-{lat2}'
    size = (f'&width={int(dlon * deg2pix)}&height={int(dlat * deg2pix)}')
    layer = (f'&layers=MODIS_{satellite}_CorrectedReflectance_TrueColor,Coastlines')

    for yr in range(year_range[0], year_range[1]):
        for m in months:
            nday = monthrange(yr,m)[1]
            for nd in range(1,nday+1):
                date = datetime.datetime(yr, m, nd)
                d = str(date.strftime('%j'))
                print(date.strftime('%y %m %d'))
                url = ('https://gibs.earthdata.nasa.gov/image-download?TIME='+
                       str(yr)+d+loc+'&epsg=4326'+layer+
                       '&opacities=1,1&worldfile=false&format=image/jpeg'+
                       size)
                save_str = (save_path+f'/{satellite}_CorrectedReflectance'+str(yr)+
                    date.strftime('%m')+'{:02d}'.format(date.day)+loc_str+
                    '.jpeg')
                if exist_skip and os.path.exists(save_str):
                    print('Skip')
                else:
                    try:
                        urllib.request.urlretrieve(url, save_str)
                    except:
                        print(f'Download failed for {save_str}')


if __name__ == '__main__':
    fire.Fire(download_imgs)

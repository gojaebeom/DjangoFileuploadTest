from PIL.ExifTags import TAGS

def getGPSInfo(info):
    taglabel = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        taglabel[decoded] = value
    print('GPS 정보')
    print(taglabel['GPSInfo'])
    exifGPS = taglabel['GPSInfo']
    # -------  위 부분까지 정보 추출 ---------

    # 추출한 정보를 가지고 위도와 경도를 얻는 연산을 한다
    latData = exifGPS[2]
    lonData = exifGPS[4]

    latDeg = latData[0]
    latMin = latData[1]
    latSec = latData[2]

    lonDeg = lonData[0]
    lonMin = lonData[1]
    lonSec = lonData[2]

    # correct the lat/lon based on N/E/W/S
    Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
    if exifGPS[1] == 'S': Lat = Lat * -1
    Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
    if exifGPS[3] == 'W': Lon = Lon * -1
    print(str(Lat)+","+str(Lon))

    return [Lat, Lon] 
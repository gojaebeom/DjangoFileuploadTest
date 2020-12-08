from django.shortcuts import render, redirect

# Create your views here.
from fileupload.models import ImageFile
from PIL import Image
from PIL.ExifTags import TAGS


# main 화면
def home(request):
    images = ImageFile.objects.all()
    return render(request, 'index.html', context={'images': images})


# 게시판 작성 화면
def create(request):
    return render(request, 'create.html')


# 이미지 한개 저장 : file upload 기본
def file_upload(request):
    # img = request.FILES.get('image')  # 파일형태인 image 를 받아온다

    image = ImageFile()  # 이미지 테이블 객체 생성
    image.img = img  # 생성된 객체의 img 컬럼에 파일 img 를 할당
    image.save()  # insert
    return redirect('/')


# # 1개 이상의 이미지 저장 : multi file upload
def multi_file_upload(request):
    imgs = request.FILES.getlist('images')  # 파일 리스트를 받아온다

    # 이미지 파일중 첫번 째 파일을 가져와 정보를 추출
    local_image = Image.open(imgs[0])
    info = local_image._getexif()

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
    # ----------- 연산 완료 ------------------

    # 데이터베이스에 데이터 저장하는 부분
    for img in imgs:  # 가져온 imgs 리스트의 크기만큼 루프를 돈다
        image = ImageFile()
        image.img = img
        image.imgX = Lat
        image.imgY = Lon
        image.save()

    # 데이터 저장 까지 끝나면 Image 라이브러리 종료
    local_image.close()

    return redirect('/')


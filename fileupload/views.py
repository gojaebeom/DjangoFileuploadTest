import os
from fileupload.services import getGPSInfo
from django.shortcuts import render, redirect
from uuid import uuid4

# Create your views here.
from fileupload.models import ImageFile
from PIL import Image



# main 화면
def home(request):
    images = ImageFile.objects.all()
    return render(request, 'index.html', context={'images': images})


# 게시판 작성 화면
def create(request):
    return render(request, 'create.html')



# # 1개 이상의 이미지 저장 : multi file upload
def multi_file_upload(request):
    imgs = request.FILES.getlist('images')  # 파일 리스트를 받아온다

    for img in imgs:
        print(img.name)

    # 이미지 파일중 첫번 째 파일을 가져와 정보를 추출
    local_image = Image.open(imgs[0])
    info = local_image._getexif()

    gpsData = getGPSInfo(info)

    print(gpsData[0])
    print(gpsData[1])

    # # 데이터베이스에 데이터 저장하는 부분
    for img in imgs:  # 가져온 imgs 리스트의 크기만큼 루프를 돈다
        # 길이 32 인 uuid 값
        uuid_name = uuid4().hex
        # 확장자 추출
        extension = os.path.splitext(img.name)[-1].lower()
        origin_name = img.name
        img.name = uuid_name + extension

        image = ImageFile()
        image.img = img
        image.origin_name = origin_name
        image.lat = gpsData[0]
        image.lon = gpsData[1]
        image.save()

    # 데이터 저장 까지 끝나면 Image 라이브러리 종료
    local_image.close()

    return redirect('/')


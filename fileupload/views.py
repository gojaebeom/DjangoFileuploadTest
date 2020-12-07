from django.shortcuts import render, redirect

# Create your views here.
from fileupload.models import Image


# main 화면
def home(request):
    images = Image.objects.all()
    return render(request, 'index.html', context={'images': images})


# 게시판 작성 화면
def create(request):
    return render(request, 'create.html')


# 이미지 한개 저장 : file upload 기본
def file_upload(request):
    img = request.FILES.get('image')  # 파일형태인 image 를 받아온다

    image = Image()  # 이미지 테이블 객체 생성
    image.img = img  # 생성된 객체의 img 컬럼에 파일 img 를 할당
    image.save()  # insert
    return redirect('/')


# 1개 이상의 이미지 저장 : multi file upload
def multi_file_upload(request):
    imgs = request.FILES.getlist('images')  # 파일 리스트를 받아온다

    for img in imgs:  # 가져온 imgs 리스트의 크기만큼 루프를 돈다
        image = Image()
        image.img = img
        image.save()

    return redirect('/')


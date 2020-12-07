# django - file upload 
#### 파일 업로드를 구현한 간단한 프로젝트 입니다. 



## 시작하기 전 안내사항
프로젝트는 항상 가상환경내에서 모듈들을 받아 사용하셔야 합니다.   
가상환경을 실행했다면 
```
pip install -r requirements.txt
```

명령어를 사용하여 필요한 의존라리브러리를 설치하실 수 있습니다.


## 시작하기 전 필요한 module
django에서 image 와 관련된 기능은 사용하기 위해선  
`pillow` 라는 라이브러리를 사용해야합니다.
```
# pillow 라이브러리를 미리 설치해주세요
pip install pillow
```
`pip install -r requirements.txt` 명령어로 프로젝트를 구성하셨다면 다시 설치하지 않아도 됩니다.


## 프로젝트 진행
프로젝트에서 보통 javascript, css 와 같은 정적 파일들은 static 폴더에서 보관합니다.   
반대로 사용자가 요청한 사진, 동영상, 그 밖의 파일등은 media 폴더에서 따로 관리 해주시는 것이 좋습니다.  

### 1. config/settings.py에  media 경로 등록
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
settings.py 하단부에 다음과 같은 설정을 등록합니다.  
지금은 단순히 media에 관련된 파일들은 media 폴더 하위경로에 저장하겠다고 이해하시면 됩니다.


### 2. 프로젝트에 fileupload app 생성
```
python manage.py startapp fileupload
```
위 명령어를 통해 새로운 app을 생성하고 settings.py에 앱을 등록해줍니다

### 3. config/urls.py 에 url 등록
```python
urlpatterns = [
    path('', views.home),  # 홈화면
    path('create', views.create),   # 게시물 생성 화면
    path('store', views.file_upload),  # 게시물 생성화면에서 생성 버튼 클릭시 요청되는 화면 없는 뷰
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # media 에 관련된 설정
```
테스트를 진행하기 위해 각 요청에 실행될 기능들을 연결해줍니다. (views는 fileupload app의 views 입니다)
urlpatterns 리스트 이후에 + static 설정 부분은 media 를 사용하기 위한 설정입니다.  


### 4. views 만들기
fileupload/views.py에 다음과 같은 함수들을 만들어줍니다.
```python
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
```
home, create 함수들은 단지 화면만 보여주기 때문에 생략하겠습니다.  
file_upload 함수는 '/store' 요청이 오면 실행되는 함수입니다.   
실행은 다음과 같습니다.  
1. 파일 타입의 image를 받아옵니다.  
2. 이미지 모델을 생성하여 이미지 값을 받아옵니다. 
3. 해당 래코드를 insert 시킵니다.
4. 메인 화면으로 되돌립니다.


아직 Image 모델이 정의되지 않았기 때문에 Image 모델을 만들도록 하겠습니다.
### 5. model 만들기
```python
from django.db import models


# Create your models here.
class Image(models.Model):
    img = models.ImageField(upload_to="%Y%m%d")

```
테스트용이기 때문에 간단하게 img 컬럼 하나만 추가 합니다.  
upload_to= 인자는 파일을 저장할 폴더 위치를 정합니다.  
위와 같이 %Y%m%d 를 입력하게 되면 파일을 받아올 때 현재 날짜를 폴더로 만들어 그 위치에 파일을 
저장하게 됩니다.( ex> [프로젝트명]/media/201207/cover.jsp )

### 6. 다중 파일 업로드의 경우
위와 같이 file_upload를 하는 경우는 하나의 파일만 저장할 수 있습니다.  
하지만 저희가 진행하는 프로젝트와는 맞지 않아 한개 이상의 파일을 업로드 하는 방법으로 대체합니다.

```python
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


# 1개 이상의 이미지 저장 : multi file upload
def multi_file_upload(request):
    imgs = request.FILES.getlist('images')  # 파일 리스트를 받아온다

    for img in imgs:  # 가져온 imgs 리스트의 크기만큼 루프를 돈다
        image = Image()
        image.img = img
        image.save()

    return redirect('/')
```
위의 코드에서 file_upload 함수를 multi_file_upload로 바꾸고 내용을 위와 같이 수정합니다.

```python
urlpatterns = [
    path('', views.home),  # 홈화면
    path('create', views.create),   # 게시물 생성 화면
    path('store', views.multi_file_upload),  # 게시물 생성화면에서 생성 버튼 클릭시 요청되는 화면 없는 뷰
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # media 에 관련된 설정
```
매칭되는 url도 변경시킵니다.


form에서 받아 오는 images 네임의 파일이 여러개일 경우 위와 같이 list 형태로 받아 올 수 있습니다.  
이 때 받아온 파일 리스트의 크기만큼 for문을 돌려 여러개의 파일에 대한 처리를 할 수 있습니다.

**create.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Create</title>
</head>
<body>
    <h1>Create</h1>
    <form action="/store" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="images"><br>
        <input type="file" name="images"><br>
        <input type="file" name="images"><br>
        <button type="submit">생성</button>
    </form>
</body>
</html>
```
지금은 input 태그 3개를 직접 입력하였지만 javascript를 이용하여 파일 업로드가 끝나면 계속하여  
input 태그를 추가하는 형식으로 다중 파일 업로드를 활용할 수 있습니다. 


그리고 file을 서버에 전송하기 위해선 위 처럼 form에 enctype 속성을 선언하여 `multipart/form-data`  
로 선언해 주셔야 합니다.
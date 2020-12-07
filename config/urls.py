"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config import settings
from fileupload import views

urlpatterns = [
    path('', views.home),  # 홈화면
    path('create', views.create),   # 게시물 생성 화면
    path('store', views.multi_file_upload),  # 게시물 생성화면에서 생성 버튼 클릭시 요청되는 화면 없는 뷰
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # media 에 관련된 설정

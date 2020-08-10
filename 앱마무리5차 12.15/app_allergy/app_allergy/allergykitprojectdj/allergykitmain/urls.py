from . import views
#from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'allergykitmain'

urlpatterns = [
    path('', views.main, name='main'),
    path('AL/logingo', views.loginpage, name="logingo"),
    path('AL/login', views.login, name="login"),
    path('AL/FindUsr', views.findusr, name="findusr"),
    path('AL/SignUpGo', views.signupgo, name="signupgo"),
    path('AL/SignUp', views.SignUp, name="SignUp"),

    path('AL/FindIDgo', views.find_id_go, name="find_id_go"),
    path('AL/FindPWgo', views.find_pw_go, name="find_pw_go"),

    path('AL/FindID', views.find_id, name="find_id"),
    path('AL/FindPW', views.find_pw, name="find_pw"),
    path('AL/Menu_choice', views.back_to_main, name="menu_choice"),
    #시트지 선택
    path('AL/Choice_Sheet', views.choice_sheet_paper, name="choice_sheet"),
    #사진 촬영
    path('AL/Take_Picture', views.take_pic, name="take_pic"),
    #사진 분석
    path('AL/Pic_Analysis', views.opencv_pic, name="opencv_pic"),
    #상세결과
    path('AL/Detail_result/<allergy_id>', views.inspection_detail_result, name="inspection_detail_result"),
    path('AL/Detail_result/<allergy_id>/<allergy_kinds>', views.detail_result, name="detail_result"),

    # 결과 조회 및 확인
    path('AL/Lookup_result', views.lookup_result, name="lookup_result"),
    #ajax
    path('ajax/idcheck', views.SignUp_idcheck, name="SignUp_idcheck"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
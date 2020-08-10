from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from datetime import datetime
import json, random, string
from .forms import *
from django.utils import timezone
from django.utils.encoding import smart_text
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#이메일 관련 import
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import AccountActivationTokenGenerator
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

#opencv
import cv2 as cv
import numpy as np

# 세션 관리
def addSessions(request, user):
    request.session['al_id'] = user.al_ID
    request.session['al_name'] = user.al_Name

# 접속자의 유저 객체 반환
def getInfo(request):
    user = User.objects.get(al_ID=request.session['al_id'])
    return user

#메인 페이지
def main(request):
    return render(request, 'allergykitmain/main.html')

#로그인
def loginpage(request):
    return render(request, 'allergykitmain/login/login.html')

def login(request):
    if request.method == 'POST':
        user_id = request.POST['al_id']
        user_pw = request.POST['al_pw']
        try:
            user = User.objects.get(al_ID=user_id)
            if user_pw == user.al_PW:
                addSessions(request, user)    
                return render(request, 'allergykitmain/menu/menu_choice.html', {
                    'user_info' : user,
                    })
            elif user_pw != user.al_PW:
                return render_to_response('allergykitmain/Error/Error.html', {
                    'alert_msg' : '비밀번호가 맞지 않습니다.',
                    'url' : '/'
                })
        except User.DoesNotExist:
            return render_to_response('allergykitmain/Error/Error.html', {
                    'alert_msg' : '해당 아이디가 없습니다.',
                    'url' : '/'
                })
    else:
        return render(request, 'allergykitmain/login/login.html', {
            'user_info' : getInfo(request),
             })

#유저정보찾기
def findusr(request):
    return render(request, 'allergykitmain/findusr/findusrinfo.html')

#회원가입
def signupgo(request):
    return render(request, 'allergykitmain/signup/signup.html')

#회원 가입
def SignUp(request):
    if request.method == "POST":
        #성별
        gendercheck = request.POST['usr_gender']
        
        user = User.objects.create(
        al_ID = request.POST['al_id'],
        al_PW = request.POST['al_pw'],
        al_Name = request.POST['al_name'],
        al_Gender = gendercheck,
        al_Email = request.POST['al_email'],
        al_Birth = request.POST['al_birth'],
        al_Height = request.POST['al_height'],
        al_Weight = request.POST['al_weight'],
        )
        return render(request, 'allergykitmain/login/login.html')

    return render(request, 'allergykitmain/signup/signup.html')


#회원가입시 유저 id 중복 방지
def SignUp_idcheck(request):
    id_check = request.POST['idcheck']
    UserList = User.objects.filter(al_ID=id_check)
    if not UserList:
        context = {  'msg' : 'Y',  }
    else:
        context = {  'msg' : 'N',  }

    return HttpResponse(json.dumps(context), content_type="application/json")

#아이디 비밀번호 찾기 이동
def find_id_go(request):
    return render(request, 'allergykitmain/findusr/find_usr_id.html')

def find_pw_go(request):
    return render(request, 'allergykitmain/findusr/find_usr_pw.html')

#아이디 비밀번호 찾기 기능
def find_id(request):
    try:
        user = User.objects.get(al_Name=request.POST['al_name'], al_Email=request.POST['al_email'])
        message = render_to_string('allergykitmain/findusr/find_usr_id_email.html',{
                'user': user,
        })
        mail_subject = "[알레르기케어 키트]] 아이디 찾기 메일입니다."
        user_email = user.al_Email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'allergykitmain/login/login.html')
    except Exception as e:
        print(e)
        messages.error(request, '해당하는 정보의 아이디가 없습니다.')
        return redirect('allergykitmain:find_id_go')
    
def find_pw(request):
    try:
        user = User.objects.get(al_Name=request.POST['al_name'], al_ID=request.POST['al_id'], al_Email=request.POST['al_email'])
        
        _LENGTH = 12 # 12자리
        # 숫자 + 대소문자
        string_pool = string.ascii_letters + string.digits
        # 랜덤한 문자열 생성
        update_usr_pw = "" 
        for i in range(_LENGTH) :
            update_usr_pw += random.choice(string_pool) # 랜덤한 문자열 하나 선택
        User.objects.filter(al_Name=request.POST['al_name']).filter(al_ID=request.POST['al_id']).filter(al_Email=request.POST['al_email']).update(
            al_PW = update_usr_pw,
        )
        message = render_to_string('allergykitmain/findusr/find_usr_pw_email.html', {
            'user_pw':update_usr_pw,
        })
        mail_subject = "[알레르기케어 키트] 임시 비밀번호 메일입니다."
        user_email = user.al_Email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'allergykitmain/login/login.html')
    except:
        messages.error(request, '해당하는 정보의 회원이 없습니다.')
        return redirect('allergykitmain:find_pw_go')

#시트지 선택 페이지
def choice_sheet_paper(request):
    user = User.objects.get(al_ID=request.session['al_id'])
    return render(request, 'allergykitmain/inspection/sheet_paper_choice.html', {'user_info': user,}) 

#사진 촬영 페이지
def take_pic(request):
    user = User.objects.get(al_ID=request.session['al_id'])
    return render(request, 'allergykitmain/inspection/img_preview.html', {'user_info': user,}) 

#사진 저장 및 opencv
def opencv_pic(request):
    try:
        user = User.objects.get(al_ID=request.session['al_id'])
        allergy_arr=[]
        arr_dict={
            1:{'fish_al':0},
            2:{'fish_al':0, 'flour_al':0},
            3:{'fish_al':0, 'flour_al':0, 'milk_al':0},
            4:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0},
            5:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0},
            6:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0,'cheese_al':0},
            7:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0,'cheese_al':0, 'alcohol_al':0},
            8:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0,'cheese_al':0, 'alcohol_al':0, 'egg_al':0},
            9:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0,'cheese_al':0, 'alcohol_al':0, 'egg_al':0, 'chicken_al':0},
            10:{'fish_al':0, 'flour_al':0, 'milk_al':0, 'meat_al':0, 'fruit_al':0,'cheese_al':0, 'alcohol_al':0, 'egg_al':0, 'chicken_al':0, 'vegetable_al':0},
        }
        if request.method == 'POST': # method가 POST 방식이라면 글이 써진 것
            usr_allergy = UsrAllergy.objects.create(
                User_Allergy = user,
                Al_CreateDate = datetime.now(),
                Al_Files = request.FILES['camera']
            )
            img = cv.imread("./media/"+str(usr_allergy.Al_Files))
            img = cv.resize(img,dsize=(600, 800), interpolation=cv.INTER_AREA)
            height, width, _ = img.shape

            roi = img[int(height/6*1):height, int(width/4*1):int(width/4*3)]

            roi_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)

            kernel = np.ones((5, 5))
            test_img = cv.Canny(roi_gray, 60, 150)
            test_img = cv.morphologyEx(test_img, cv.MORPH_CLOSE, kernel)

            j = 0
            nlabels, _, stats, __ = cv.connectedComponentsWithStats(test_img)

            for i in range(nlabels):

                if i < 2:
                    continue
                width = stats[i, cv.CC_STAT_WIDTH]
                height = stats[i, cv.CC_STAT_HEIGHT]

                ratio = width/height
                if width < 100 and height < 100 and width > 10 and height > 10 and ratio > 0.4 and ratio < 2 and j < 10:
                    j += 1
                    allergy_arr.append(round(width*height,2)/100)
            
            index=0
            try:
                for key in arr_dict[j]:
                    arr_dict[j][key]=allergy_arr[index]
                    index += 1
            except:
                messages.error(request, '사진을 다시 찍어주세요.')
                return redirect('allergykitmain:take_pic')

            UsrAllergy.objects.filter(id=usr_allergy.id).update(
                **arr_dict[j]
            )
            max_count = 0
            for a in allergy_arr:
                if a>=40:
                    max_count += 1

            return render(request, 'allergykitmain/inspection/inspection_result.html', {'user_info': user, 'usr_allergy':usr_allergy, 'allergy_count':j,'danger_allergy':max_count, 'allergy_list':arr_dict[j],})
    except:
        messages.error(request, '사진을 찍고 결과를 분석해주세요!')
        return redirect('allergykitmain:take_pic')
    return render(request, 'allergykitmain/inspection/img_preview.html', {'user_info': user,})

#상세 결과 페이지
def inspection_detail_result(request, allergy_id):
    user = User.objects.get(al_ID=request.session['al_id'])
    usr_allergy_info = UsrAllergy.objects.get(id=allergy_id)
    return render(request, 'allergykitmain/inspection/inspection_detail_result.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info,}) 

#상세 결과 
def detail_result(request, allergy_id, allergy_kinds):
    user = User.objects.get(al_ID=request.session['al_id'])
    usr_allergy_info = UsrAllergy.objects.get(id=allergy_id)
    if allergy_kinds == '1':
        fish_result = float(usr_allergy_info.fish_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/fish.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'fish':fish_result}) 
    elif allergy_kinds == '2':
        flour_result = float(usr_allergy_info.flour_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/flour.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'flour':flour_result}) 
    elif allergy_kinds == '3':
        milk_result = float(usr_allergy_info.milk_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/milk.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'milk':milk_result}) 
    elif allergy_kinds == '4':
        meat_result = float(usr_allergy_info.meat_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/meat.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'meat':meat_result}) 
    elif allergy_kinds == '5':
        fruit_result = float(usr_allergy_info.fruit_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/fruit.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'fruit':fruit_result}) 
    elif allergy_kinds == '6':
        cheese_result = float(usr_allergy_info.cheese_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/cheese.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'cheese':cheese_result}) 
    elif allergy_kinds == '7':
        alcohol_result = float(usr_allergy_info.alcohol_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/alcohol.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'alcohol':alcohol_result}) 
    elif allergy_kinds == '8':
        egg_result = float(usr_allergy_info.egg_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/egg.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'egg':egg_result}) 
    elif allergy_kinds == '9':
        chicken_result = float(usr_allergy_info.chicken_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/chicken.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'chicken':chicken_result}) 
    elif allergy_kinds == '10':
        vegetable_result = float(usr_allergy_info.vegetable_al)
        return render(request, 'allergykitmain/inspection/inspect_detail/vgt.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info, 'vgt':vegetable_result}) 

    return render(request, 'allergykitmain/inspection/inspection_detail_result.html', {'user_info': user, 'usr_allergy_info':usr_allergy_info,})

def back_to_main(request):
    user = User.objects.get(al_ID=request.session['al_id'])
    return render(request, 'allergykitmain/menu/menu_choice.html', {'user_info' : user,})

def lookup_result(request):
    user = User.objects.get(al_ID=request.session['al_id'])
    user_birth = user.al_Birth
    user_year = user_birth[0:4]
    user_month = user_birth[4:6]
    user_day = user_birth[6:8]

    now = datetime.now() 
    usr_age = int(now.year - int(user_year))
    if now.month > int(user_month):
        usr_age = usr_age - 1
    elif now.month == int(user_month) and now.day > int(user_day):
        usr_age = usr_age - 1

    try:
        allergy_result_list_lastest = UsrAllergy.objects.filter(User_Allergy=user).latest()
        allergy_result_list = UsrAllergy.objects.filter(User_Allergy=user).exclude(id=allergy_result_list_lastest.id)
        allergy_result_list_count = UsrAllergy.objects.filter(User_Allergy=user).count()
        allergy_add_all = float(allergy_result_list_lastest.fish_al)+float(allergy_result_list_lastest.flour_al)+float(allergy_result_list_lastest.milk_al)+float(allergy_result_list_lastest.meat_al)+float(allergy_result_list_lastest.fruit_al)+float(allergy_result_list_lastest.cheese_al)+float(allergy_result_list_lastest.alcohol_al)+float(allergy_result_list_lastest.egg_al)+float(allergy_result_list_lastest.chicken_al)+float(allergy_result_list_lastest.vegetable_al)
        print(allergy_add_all)
        allergy_count = 0
        if float(allergy_result_list_lastest.fish_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.flour_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.milk_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.meat_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.fruit_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.cheese_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.alcohol_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.egg_al) > 11:
            allergy_count = allergy_count + 1
        if float(allergy_result_list_lastest.chicken_al) > 11:
            allergy_count = allergy_count + 1 
        if float(allergy_result_list_lastest.vegetable_al) > 11:
            allergy_count = allergy_count + 1     
        not_allergy_count = 10-allergy_count
    except:
        messages.error(request, '해당하는 아이디의 검사 결과가 존재하지 않습니다.')
        return redirect('allergykitmain:menu_choice')
    
    return render(request, 'allergykitmain/inspection/inspect_lookup.html',{'usr_result_lastest':allergy_result_list_lastest,'usr_result_list':allergy_result_list, 'user_info':user, 'user_year':user_year, 'user_month':user_month,'user_day':user_day, 'user_age':usr_age, 'allergy_count':allergy_count, 'not_allergy_count':not_allergy_count, 'allergy_result_list_count':allergy_result_list_count, 'allergy_add_all':allergy_add_all})

from django.shortcuts import render,redirect,HttpResponse,reverse
from repository import models
import json,uuid,os
from io import BytesIO
from Utils.check_code import create_validate_code
from ..forms.account import LoginForm,RegisterForm
from Utils.rbac import MenuHelper

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects.filter(username=username, password=password).\
                values('nid', 'nickname',
                       'username', 'email','password','blog__nid','blog__site','avatar','blog__theme','blog__title').first()
            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                request.session['avatar'] = user_info['avatar']
                MenuHelper(request, user_info['username'])
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            if request.session.get('CheckCode').upper() != request.POST.get('check_code').upper():
                result['message'] = '验证码错误'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = RegisterForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            cpassword = form.cleaned_data.get('cpassword')
            email = form.cleaned_data.get('email')
            if password !=cpassword:
                result['message'] = '两次密码输入不一致'
            else:
                obj = models.UserInfo.objects.filter(username=username)
                if obj:
                    result['message'] = '用户名已存在'
                else:
                    models.UserInfo.objects.create(username=username,password=password,email=email)
                    result['status'] = True
        else:
            result['message'] = '输入为空或者格式不对'
        return HttpResponse(json.dumps(result))

def logout(request):
    request.session.clear()
    return redirect('/login.html')

def checkcode(request):

    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream,'PNG')
    request.session['Checkcode'] = code
    return HttpResponse(stream.getvalue())
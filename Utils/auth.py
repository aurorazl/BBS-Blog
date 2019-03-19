from django.shortcuts import render,redirect,HttpResponse,reverse

def check_auth(func):
    def inner(request,*args,**kwargs):
        v = request.session.get('user_info', None)
        if not v:
            return redirect('/login.html')
        return func(request,*args,**kwargs)
    return inner
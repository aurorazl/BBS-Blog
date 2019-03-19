from django.shortcuts import render,redirect,HttpResponse,reverse
from repository import models
from Utils import paginations
from ..forms.trouble import TroubleForm,TroubleDealForm
import datetime
from django.db.models import Q
from Utils.rbac import permission

@permission
def trouble_list(request,*args,**kwargs):
    user_id = request.session['user_info']['nid']
    result = models.Trouble.objects.filter(user_id=user_id).order_by('status').\
        only('title','status','ctime','processer')
    # only 只获取指定列数据
    val = request.COOKIES.get('per_page_count_self',10)
    page_obj = paginations.Page(int(request.GET.get('p', 1)), len(result), int(val))
    page_str = page_obj.page_str(reverse('trouble_list'))
    trouble_list = result[page_obj.start:page_obj.end]
    return render(request,'backend_trouble_list.html',{'result': trouble_list,'page_str':page_str,'list_count':len(result)})

@permission
def trouble_detail(request,trouble_id,*args,**kwargs):
    result = models.Trouble.objects.filter(tid=trouble_id).first()
    return render(request, 'backend_trouble_detail.html', {'result': result})

@permission
def trouble_create(request,*args,**kwargs):
    if request.method == 'GET':
        form = TroubleForm()
    else:
        form = TroubleForm(request.POST)
        if form.is_valid():
            # title,content
            # form.cleaned_data
            dic = {}
            dic['user_id'] = 1 # session中获取
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)
            models.Trouble.objects.create(**dic)
            return redirect('/backend/trouble-list.html')
    return render(request, 'backend_trouble_create.html',{'form':form})

@permission
def trouble_edit(request,nid,*args,**kwargs):
    if request.method == "GET":
        obj = models.Trouble.objects.filter(tid=nid, status=1).only('tid', 'title', 'detail').first()
        if not obj:
            return HttpResponse('已处理中的保单章无法修改..')
        # initial 仅初始化
        form = TroubleForm(initial={'title': obj.title,'detail': obj.detail})
        # 执行error会进行验证
        return render(request,'backend_trouble_edit.html',{'form':form,'tid':nid})
    else:
        form = TroubleForm(data=request.POST)
        if form.is_valid():
            # 受响应的行数
            v = models.Trouble.objects.filter(tid=nid, status=1).update(**form.cleaned_data)
            if not v:
                return HttpResponse('已经被处理')
            else:
                return redirect('/backend/trouble-list.html')
        return render(request, 'backend_trouble_edit.html', {'form': form, 'tid': nid})

@permission
def trouble_kill_list(request,*args,**kwargs):
    user_id = request.session['user_info']['nid']
    result = models.Trouble.objects.filter(Q(processer_id=user_id)|Q(status=1)).order_by('status')
    # 分页
    val = request.COOKIES.get('per_page_count_self', 10)
    page_obj = paginations.Page(int(request.GET.get('p', 1)), len(result), int(val))
    page_str = page_obj.page_str(reverse('trouble_list'))
    trouble_list = result[page_obj.start:page_obj.end]
    return render(request,'backend_trouble_kill_list.html',{'result':trouble_list,'page_str':page_str})

def trouble_deal(request,nid,*args,**kwargs):
    user_id = request.session['user_info']['nid']
    if request.method == 'GET':
        ret = models.Trouble.objects.filter(tid=nid, processer=user_id).count()
        # 以前未抢到
        if not ret:
            v = models.Trouble.objects.filter(tid=nid,status=1).update(processer=user_id,status=2)
            if not v:
                return HttpResponse('手速太慢...')
        obj = models.Trouble.objects.filter(tid=nid).first()
        form = TroubleDealForm(initial={'title': obj.title,'solution': obj.solution})
        return render(request,'backend_trouble_deal.html',{'obj':obj,'form': form,'tid':nid})
    else:
        ret = models.Trouble.objects.filter(tid=nid, processer=user_id,status=2).count()
        # status=2 防止修改以前的值
        if not ret:
            return HttpResponse('去你妈的')
        form = TroubleDealForm(request.POST)
        if form.is_valid():
            dic = {}
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            dic['ptime'] = datetime.datetime.now()
            models.Trouble.objects.filter(tid=nid, processer=user_id,status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
        obj = models.Trouble.objects.filter(tid=nid).first()
        return render(request, 'backend_trouble_deal.html', {'obj': obj, 'form': form, 'tid': nid})

@permission
def trouble_report(request,*args,**kwargs):
    return render(request,'backend_trouble_report.html')

def trouble_json_report(request):
    # 数据库中获取数据
    user_list = models.UserInfo.objects.filter(user2role__r__caption="管理员")
    response = []
    for user in user_list:
        from django.db import connection, connections
        cursor = connection.cursor()    # 原生SQL
        cursor.execute("""select strftime('%%s',strftime("%%Y-%%m-01",ctime)) * 1000,count(tid) from repository_trouble where processer_id = %s group by strftime("%%Y-%%m",ctime)""", [user.nid,])
        # 不用%()进行格式化;%%s 时间戳
        result = cursor.fetchall()
        print(result)
        temp = {
            'name': user.username,
            'data':result
        }
        response.append(temp)
    import json
    return HttpResponse(json.dumps(response))

















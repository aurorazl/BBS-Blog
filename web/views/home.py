from django.shortcuts import render,redirect,HttpResponse,reverse
from repository import models
import json,uuid,os
from django import forms
from django.forms.models import model_to_dict
from io import BytesIO
from Utils.check_code import create_validate_code
from Utils import paginations
from django.db import transaction
from Utils.xss import XSSFilter
from Utils.auth import check_auth
from django.http import JsonResponse
from django.db.models import F

def index(request):
    """
    博客首页，展示全部文章
    :param request:
    :return:
    """
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    if not val:
        val = '10'
    article = models.Article.objects.order_by('-nid').all()              #
    page_obj = paginations.Page(current_page,len(article),int(val))
    article_list = article[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("")

    return render(request,'index.html',{'article_list':article_list,'page_str':page_str})

def news(request):
    """
    新闻首页，展示全部新闻
    :param request:
    :return:
    """
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    if not val:
        val = '10'
    news = models.News.objects.all().order_by('-nid')             #
    page_obj = paginations.Page(current_page,len(news),int(val))
    news_list = news[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("")

    return render(request,'news.html',{'news_list':news_list,'page_str':page_str})

def pick(request):
    """
    新闻首页，展示全部新闻
    :param request:
    :return:
    """
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    if not val:
        val = '10'
    pick = models.Article.objects.all().filter(pick=True).order_by('-nid')             #
    page_obj = paginations.Page(current_page,len(pick),int(val))
    pick_list = pick[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("")

    return render(request,'pick.html',{'pick_list':pick_list,'page_str':page_str})

def photo(request):
    return render(request, 'photo.html')

def get_imgs(request):
    nid = request.GET.get('nid')
    img_list = models.Img.objects.filter(id__gt=nid).values('id', 'src', 'title')
    img_list = list(img_list)
    ret = {
        'status': True,
        'data': img_list
    }
    return JsonResponse(ret)

@check_auth
def home(request,site):
    """
    个人博客首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi/
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    if not val:
        val = '10'
    article = models.Article.objects.filter(blog=blog).order_by('-nid').all()              #
    page_obj = paginations.Page(current_page,len(article),int(val))
    article_list = article[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/'+site+'/')
    category_list = models.Article.category_choice
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request,'home.html',{
        'blog': blog,
        'article_list':article_list,
        'tag_list':tag_list,
        'category_list':category_list,
        'page_str':page_str,
        'date_list':date_list
    })

@check_auth
def filter(request,site,condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    p = request.COOKIES.get('per_page_count', 10)
    if not p:
        p = '10'
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Article.category_choice
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    template_name = "home.html"
    if condition == 'tag':
        article = models.Article.objects.filter(tags=val,blog=blog).all()
    elif condition == 'category':
        article = models.Article.objects.filter(category_id=val,blog=blog).all()
    elif condition == 'date':
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        article = models.Article.objects.all().extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    else:
        article = []

    page_obj = paginations.Page(current_page, len(article), int(p))
    article_list = article[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/'+site+'/')
    return render(
        request,template_name,
        {'blog': blog,
        'article_list': article_list,
         'tag_list': tag_list,
         'category_list': category_list,
         'page_str': page_str,
         'date_list': date_list}
    )

def article(request,site,article_id):
    """
    文章详细页
    :param request:
    :param site:
    :param article_id:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    category_list = models.Article.category_choice
    tag_list = models.Tag.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    article = models.Article.objects.filter(nid=article_id,blog=blog).select_related('detail').first()
    comment_list = models.Comment.objects.filter(article=article).select_related('reply')
    return render(
        request,
        'article.html',
        {
           'blog': blog,
            'article': article,
            'comment_list': comment_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
        }
    )

@check_auth
def up(request):
    """
    接收ajax请求，点赞or踩
    :param request:
    :return:
    """
    nid = int(request.GET.get('nid'))

    up = request.GET.get('up')
    if up==0:
        up=False
    else:
        up = True
    aid = int(request.session['user_info']['nid'])
    ret = {'status':False,'data':''}
    with transaction.atomic():
        if not models.UpDown.objects.filter(article_id=nid,user_id=aid):
            models.UpDown.objects.create(article_id=nid,user_id=aid,up=up)
            if up:
                models.Article.objects.filter(nid=nid).update(up_count=F('up_count')+1)
            else:
                models.Article.objects.filter(nid=nid).update(down_count=F('up_count') + 1)
            ret['status']=True
        else:
            models.UpDown.objects.filter(article_id=nid, user_id=aid).delete()
            if up:
                models.Article.objects.filter(nid=nid).update(up_count=F('up_count') - 1)
            else:
                models.Article.objects.filter(nid=nid).update(down_count=F('up_count')- 1)
    return HttpResponse(json.dumps(ret))

@check_auth
def comment(request):
    """
    评论ajax请求
    :param request:
    :return:
    """
    art_id = request.GET.get('art_id')
    text = request.GET.get('text')
    reply_id = request.GET.get('reply_id')
    if not reply_id:
        reply_id=None
        reply = ''
    else:
        com_obj = models.Comment.objects.filter(nid=reply_id).select_related('user').first()
        reply='@'+com_obj.user.nickname
    forloop_id = int(request.GET.get('forloop_id'))+1
    uid = request.session['user_info']['nid']
    nickname = request.session['user_info']['nickname']
    ret = {'status': False, 'data': ''}
    content = XSSFilter().process(text)
    with transaction.atomic():
        obj =  models.Comment.objects.create(content=content,reply_id=reply_id,user_id=uid,article_id=art_id)
        models.Article.objects.filter(nid=art_id).update(comment_count=F('comment_count')+1)
    if obj:
        ret['status']=True
        ret['data'] = """
                <div class="comment-item" loop_id="%s">
                    <div class="reply-title clearfix">
                        <div class="user-info">
                            <span>#%s  %s</span>
                            <span>%s</span>
                        </div>
                        <div class="reply">
                            <a href="javascript:void(0);">回复</a>
                        </div>
                    </div>
                    <div class="reply-body">
                        <div class="content">
                            %s
                        </div>
                    </div>
                </div>
            """ %(forloop_id,forloop_id,nickname,obj.create_time,content,)
    return JsonResponse(ret)
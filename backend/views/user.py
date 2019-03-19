from django.shortcuts import render,redirect,HttpResponse,reverse
from repository import models
import json,uuid,os
from django import forms
from django.forms.models import model_to_dict
from Utils import paginations
from django.db import transaction
from Utils.xss import XSSFilter
from ..forms.article import ArticleForm
from ..forms.baseinfo import BaseInfoForm
from Utils.rbac import permission
from Utils.auth import check_auth


@permission
def index(request,*args,**kwargs):
    action_list =  kwargs['action_list']
    return render(request,'backend_index.html',{'action_list':action_list})

@check_auth
def base_info(request):
    user_nid = request.session['user_info']['nid']
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = BaseInfoForm(initial=request.session['user_info'])
        return render(request, 'backend_base_info.html',{'form':obj})
    elif request.method == 'POST':
        obj = BaseInfoForm(request.POST)
        if obj.is_valid():
            with transaction.atomic():
                request.session['user_info'].update(obj.cleaned_data)
                ret = {}
                ret['title'] = obj.cleaned_data.pop('blog__title')
                ret['site'] = obj.cleaned_data.pop('blog__site')
                ret['theme'] = obj.cleaned_data.pop('blog__theme')
                models.UserInfo.objects.filter(nid=user_nid).update(**obj.cleaned_data)
                models.Blog.objects.filter(nid=blog_id).update(**ret)
            return redirect('/backend/index/')
        else:
            return render(request, 'backend_base_info.html', {'form': obj})

@check_auth
def avatar_upload(request):
    ret = {'status': False, 'data': None, 'message': None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())+ '.jpg'
            file_path = os.path.join('static/imgs/avatar/', file_name)
            f = open(file_path, 'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            ret['status'] = True
            ret['data'] = file_path
            avatar = '/'+file_path
            request.session['avatar']=avatar
            models.UserInfo.objects.filter(username=request.session['user_info']['username']).update(avatar=avatar)

    return HttpResponse(json.dumps(ret))

@check_auth
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    blog = models.Blog.objects.filter(site=request.session['user_info']['blog__site']).first()
    tag_list = models.Tag.objects.filter(blog=blog).all()
    return render(request, 'backend_tag.html',{'tag_list':tag_list})

@check_auth
def article(request,**kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    blog_id = request.session['user_info']['blog__nid']
    condition['blog_id'] = blog_id
    result = models.Article.objects.filter(**condition)
    val = request.COOKIES.get('per_page_count_self',10)
    page_obj = paginations.Page(int(request.GET.get('p', 1)), len(result), int(val))
    page_str = page_obj.page_str(reverse('article', kwargs=kwargs))
    article_list = models.Article.objects.filter(**condition)[page_obj.start:page_obj.end]
    tag_list = models.Tag.objects.filter(blog_id=blog_id).values('nid', 'caption')
    category_list = map(lambda item: {'nid': item[0], 'caption': item[1]}, models.Article.category_choice)
    kwargs['p'] = page_obj.current_page
    return render(
        request,
        'backend_article.html',
        {
            'result': article_list,
            'category': category_list,
            'tag': tag_list,
            'arg_dict': kwargs,
            'page_str': page_str,
            'data_count': len(result),
        })

@check_auth
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'GET':
        obj = ArticleForm(request=request)
        return render(request,'backend_add_article.html',{'form':obj})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                tags = form.cleaned_data.pop('tags')
                detail = form.cleaned_data.pop('detail')
                detail = XSSFilter().process(detail)
                a_obj = models.ArticleContent.objects.create(content=detail)
                form.cleaned_data['detail_id'] = a_obj.nid
                form.cleaned_data['author_id'] = request.session['user_info']['nid']
                obj = models.Article.objects.create(**form.cleaned_data)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
            return redirect('/')

@check_auth
def edit_article(request,article_id):
    """
    编辑文章
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        o = models.Article.objects.filter(nid=article_id,blog_id=blog_id).first()
        if not o:
            return render(request, 'backend_no_article.html')
        tags = o.tags.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'title':o.title,
            'content':o.content,
            'category_id':o.category_id,
            'tags':tags,
            'detail':o.detail.content
        }
        obj = ArticleForm(request=request,initial=init_dict)
        return render(request, 'backend_edit_article.html', {'form':obj, 'article_id':article_id})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=article_id,blog_id=blog_id).first()
            with transaction.atomic():
                detail = form.cleaned_data.pop('detail')
                detail = XSSFilter().process(detail)
                tags = form.cleaned_data.pop('tags')
                models.Article.objects.filter(nid=article_id).update(**form.cleaned_data)
                models.ArticleContent.objects.filter(article=obj).update(content=detail)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'nid': article_id})

@check_auth
def delete_article(request,article_id):

    with transaction.atomic():
        models.Article.objects.filter(nid=article_id).delete()
        models.ArticleContent.objects.filter(article__nid=article_id).delete()
    return redirect('/backend/article-0-0.html')


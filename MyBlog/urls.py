"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('web.urls')),
    url(r'^backend/',  include('backend.urls')),

    # url(r'^home.html', views.home),
    # url(r'^backend_layout.html$', views.selfhome),
    # url(r'^backend_base_info.html$', views.self_info),
    # url(r'^avatar_upload.html$', views.avatar_upload),
    # url(r'^self_info_edit.html$', views.self_info_edit),
    # url(r'^self_blog/article-(?P<category_id>\d+)-(?P<tags__nid>\d+).html', views.self_blog,name='self_blog'),
    # url(r'^login.html$', views.login),
    # url(r'^logout.html$', views.logout),
    # url(r'^register.html$', views.register),
    # url(r'^search-(?P<category_id>\d+)-(?P<tags__nid>\d+).html', views.search,name='search'),
    # url(r'^article/(?P<article_id>\d+).html', views.article,name='article_id'),
    # url(r'^backend_add_article.html', views.publish,name='publish'),
    # url(r'^check_code.html', views.checkcode,name='checkcode'),
    # url(r'^article_edit/(?P<article_id>\d+).html', views.article_edit,name='article_edit'),
    # url(r'^article_del/(?P<article_id>\d+).html', views.article_delete,name='article_delete'),
    # url(r'^(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', views.filter),

    # url(r'^trouble-list.html', views_backend.trouble_list, name='trouble_list'),
    # url(r'^trouble-create.html', views_backend.trouble_create, name='trouble_create'),
    # url(r'^trouble_edit/(\d+).html', views_backend.trouble_edit, name='trouble_edit'),
    #
    # url(r'^trouble_deal_list.html', views_backend.trouble_deal_list, name='trouble_deal_list'),
    # url(r'^trouble_deal/(\d+).html', views_backend.trouble_deal, name='trouble_deal'),
    #
    # url(r'^backend_trouble_report.html', views_backend.trouble_report, name='trouble_report'),
    # url(r'^trouble_json_report.html', views_backend.trouble_json_report, name='trouble_json_report'),
]

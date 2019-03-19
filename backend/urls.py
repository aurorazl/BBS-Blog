from django.conf.urls import url
from django.conf.urls import include
from .views import user,celery_task_use
from .views import trouble
from rest_framework import routers
from .views import rest_views

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),

    url(r'^index/$', user.index),
    url(r'^base_info.html$', user.base_info),
    url(r'^avatar_upload.html$', user.avatar_upload),
    url(r'^tag.html$', user.tag),

    url(r'^article-(?P<category_id>\d+)-(?P<tags__nid>\d+).html', user.article, name='article'),
    url(r'^add_article.html', user.add_article, name='add_article'),
    url(r'^edit_article/(?P<article_id>\d+).html', user.edit_article, name='edit_article'),
    url(r'^del_article/(?P<article_id>\d+).html', user.delete_article, name='delete_article'),

    url(r'^trouble-list.html$', trouble.trouble_list,name='trouble_list'),
    url(r'^trouble-detail/(?P<trouble_id>\d+).html$', trouble.trouble_detail),
    url(r'^trouble-create.html$', trouble.trouble_create),
    url(r'^trouble-edit/(\d+).html$', trouble.trouble_edit),

    url(r'^trouble-kill-list.html$', trouble.trouble_kill_list),
    url(r'^trouble-deal/(\d+).html$', trouble.trouble_deal),
    url(r'^trouble-report.html$', trouble.trouble_report),
    url(r'^trouble-json-report.html$', trouble.trouble_json_report),

    url(r'^celery_pub.html$', celery_task_use.celery_pub),
    url(r'^celery_get.html$', celery_task_use.celery_get),
]


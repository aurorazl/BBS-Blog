#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def category_all(arg_dict):
    tag_id = arg_dict['tags__nid']
    category_id = arg_dict['category_id']
    p = arg_dict['p']
    url = reverse('article', kwargs={'category_id': 0, 'tags__nid':tag_id })
    if category_id == 0:
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)


@register.simple_tag
def category_combine(obj_list, arg_dict):
    li = []
    tag_id = arg_dict['tags__nid']
    category_id = arg_dict['category_id']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('article', kwargs={'category_id': obj['nid'], 'tags__nid': tag_id})
        if obj['nid'] == int(category_id):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['caption'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['caption'])
        li.append(temp)
    return mark_safe(''.join(li))


@register.simple_tag
def article_type_all(arg_dict):
    tag_id = arg_dict['tags__nid']
    category_nid = arg_dict['category_id']
    p = arg_dict['p']
    url = reverse('article', kwargs={'tags__nid': 0, 'category_id': category_nid})
    if tag_id == 0:
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)

@register.simple_tag
def article_type_combine(obj_list, arg_dict):
    li = []
    tag_id = arg_dict['tags__nid']
    category_nid = arg_dict['category_id']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('article', kwargs={'tags__nid': obj['nid'], 'category_id': category_nid})
        if obj['nid'] == int(tag_id):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['caption'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['caption'])
        li.append(temp)
    return mark_safe(''.join(li))
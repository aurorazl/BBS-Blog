#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets
from repository import models

class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'}),
        error_messages = {'required': '标题不能为空.'}
    )
    content = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'}),
        error_messages={'required': '简介不能为空.'}
    )
    detail = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'}),
        error_messages={'required': '内容不能为空.'}
    )
    category_id = django_fields.IntegerField(
        widget=django_widgets.RadioSelect(choices=models.Article.category_choice),
        error_messages = {'required': '请选择一个分类.'}
    )
    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple,
        error_messages = {'required': '请选择标签.'}
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'caption')
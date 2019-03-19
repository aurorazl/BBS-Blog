#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets


class TroubleForm(django_forms.Form):
    title = django_fields.CharField(max_length=32,
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '报障标题'}),
        error_messages = {'required': '标题不能为空.'}
    )
    detail = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content','id':'detail','placeholder': '请输入要解决的具体情况。。。'}),
        error_messages={'required': '内容不能为空.'}
    )

class TroubleDealForm(django_forms.Form):

    solution = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content','id':'solution'}),
        error_messages={'required': '内容不能为空.'}
    )

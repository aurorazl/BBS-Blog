from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets
from repository import models

class BaseInfoForm(forms.Form):
    username = forms.CharField(max_length=16,error_messages={'required':'用户名不能为空','max_length':'长度不能大于16'},label="用户名：",)
    nickname = forms.CharField(max_length=16,label="昵称：",error_messages={'required':'昵称不能为空','max_length':'长度不能大于16'})
    password = forms.CharField(min_length=6,max_length=12,error_messages={'required':'密码不能为空','min_length':'长度不能小于6'},label="密码：")
    email = forms.EmailField(error_messages={'invalid':'格式错误','required':'邮箱不能为空'},label="邮箱：")
    blog__site = forms.CharField(min_length=4,max_length=8,error_messages={'required':'博客地址不能为空','min_length':'长度不能小于4','max_length':'长度不能大于8'})
    blog__theme = forms.ChoiceField(choices=((1, '默认主题'), (2, '红色火焰'),(3, '嘿嘿哈嘿'),(4, '哈哈哈嘿哈'),(5, '编不出来了')))
    blog__title = forms.CharField(widget=django_widgets.Textarea(),error_messages={'required': '内容不能为空.'})

    username.widget.attrs.update({'class': 'form-control'})
    nickname.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    blog__site.widget.attrs.update({'class': 'form-control','id':"blogUrl",'placeholder':'如：wupeiqi,则个人博客为http://www.xxx.com/wupeiqi.html'})
    blog__theme.widget.attrs.update({'class': 'form-control','id':"blogTheme"})
    blog__title.widget.attrs.update({'class': 'form-control','id':"blogTitle",'placeholder':'来一杯鸡汤...','style':'min-height: 100px'})

    def __init__(self, *args, **kwargs):
        super(BaseInfoForm, self).__init__(*args, **kwargs)
        # blog_id = request.session['user_info']['blog__nid']
        self.fields['blog__theme'].choices = choices=((1, '默认主题'), (2, '红色火焰'),(3, '嘿嘿哈嘿'),(4, '哈哈哈嘿哈'),(5, '编不出来了'))
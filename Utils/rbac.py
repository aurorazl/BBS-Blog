from django.shortcuts import render,HttpResponse,redirect
from repository import models
import re

class MenuHelper(object):

    def __init__(self,request,username):
        # 当前请求的request对象
        self.request = request
        # 当前用户名
        self.username = username
        # 获取当前URL，不包括url中传参，可以再定义一个字段用来接收url参数，判断参数是否在action_list中
        self.current_url = request.path_info

        # 获取当前用户的所有权限
        self.permission2action_dict = None
        # 获取在菜单中显示的权限
        self.menu_leaf_list = None
        # 获取所有菜单
        self.menu_list = None

        self.session_data()

    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
            # user_obj = models.User.objects.filter(username=u)
            # role_list = models.Role.objects.filter(user2role__u=user_obj)
            # 获取当前用户的角色列表
            role_list = models.Role.objects.filter(user2role__u__username=self.username)

            # models.Permission2Action2Role.objects.filter(r__in=role_list)
            # 获取用户所有权限列表
            permission2action_list = models.Permission2Action.objects.filter(
                permission2action2role__r__in=role_list).values('p__url', 'a__code').distinct()

            permission2action_dict = {}
            for item in permission2action_list:
                if item['p__url'] in permission2action_dict:
                    permission2action_dict[item['p__url']].append(item['a__code'])  # 把同一个URL的操作放在一个列表中
                else:
                    permission2action_dict[item['p__url']] = [item['a__code'], ]

            # url_list = models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).values('p__url','p__caption').distinct()

            # 获取菜单的叶子节点，即：菜单的最后一层应该显示的权限
            # 去掉exclude（p__menu__isnull=True）,能显示所有的菜单
            menu_leaf_list = list(models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).values('p_id', 'p__url', 'p__caption', 'p__menu').distinct())

            # 获取所有的菜单列表
            menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))

            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }

    def menu_data_list(self):

        # 所有的菜单
        menu_list = models.Menu.objects.values('id', 'caption', 'parent_id')
        menu_dict = {}
        menu_id = 0
        for item in menu_list:
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item  # 每个菜单现在有自己的key
            menu_id = item['id']+100

        # 将子叶menu_leaf_list的字典转化为同菜单键的字典
        menu_leaf_dict = {}
        open_parent_id = None
        for item in self.menu_leaf_list:
            item = {
                'id': item['p_id'],
                'url': item['p__url'],
                'caption': item['p__caption'],
                'parent_id': item['p__menu'],
                'child': [],
                'status': True,  # 不创建无权限的菜单
                'open': False    # 决定哪个菜单展示
            }
            # 4：{}的形式，为上一步得到的字典对应一个key，key指挂在哪个菜单下
            if item['parent_id']:
                if item['parent_id'] in menu_leaf_dict:
                    menu_leaf_dict[item['parent_id']].append(item)
                else:
                    menu_leaf_dict[item['parent_id']] = [item, ]
            else:
                # 说明该item为根菜单
                item['open'] = True
                menu_dict[menu_id]=item
                menu_id +=1
            # 判断访问url是否是菜单中的权限
            import re
            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_parent_id = item['parent_id']


        # 将显示的权限挂在所属的菜单下
        for k, v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            parent_id = k
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']

        while open_parent_id:
            menu_dict[open_parent_id]['open'] = True
            open_parent_id = menu_dict[open_parent_id]['parent_id']

        # 将有parent_id的挂在父id的菜单下
        result = []  # 存储根节点，根节点的child引用了子节点的内存
        for row in menu_dict.values():
            if not row['parent_id']:
                result.append(row)
            else:
                menu_dict[row['parent_id']]['child'].append(row)
        # for item in result:
        #     print(item['caption'])
        #     for r in item['child']:
        #         print('-----',r['caption'])
        #         for i in r['child']:
        #             print('----------',i['caption'])
        return result

    def menu_content(self,child_list):
        response = ""
        tpl = """
            <div class="menu-item %s">
                <i class="fa fa-cogs" aria-hidden="true"></i>
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in child_list:      # child为空时不循环
            if not row['status']:  # 如果没有标记，则不显示在页面上
                continue
            if 'url' in row:
                response += """<a class="menu-item" href='%s'>
                               <i class="fa fa-cogs" aria-hidden="true"></i>
                               <span>%s</span>
                           </a>""" % (row['url'], row['caption'])
            else:
                active = ''
                if row['open']:
                    active = 'active'
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (active, title, content)
        return response

    def menu_tree(self):
        response = ""
        tpl = """
            <div class="menu-item %s">
                <a>
                <i class="fa fa-cogs" aria-hidden="true"></i>
                <span class="menu-title">%s</span>
                </a>
                <span class="menu-content">%s</span>
            </div>
        """
        for row in self.menu_data_list():
            if not row['status']:
                continue
            if 'url' in row:
                response += """<a class='menu-item' href='%s'>
                               <i class="fa fa-cogs" aria-hidden="true"></i>
                               <span>%s</span>
                           </a>""" % (row['url'], row['caption'])
                continue
            active = ''
            if row['open']:
                active = 'active'
            title = row['caption']
            content = self.menu_content(row['child'])
            response += tpl % (active, title, content)
        return response

    def actions(self):
        """
        检查当前用户是否对当前URL有权访问，并获取对当前URL有什么权限
        """
        action_list = []
        # 当前所有权限
        # {
        #     '/index.html': ['GET',POST,]
        # }
        for k,v in self.permission2action_dict.items():
            if re.match(k,self.current_url):
                action_list = v # ['GET',POST,]
                break
        return action_list

# def order(request):
#     u = request.GET.get('u')
#     user_request_url = '/money.html'
#     obj = MenuHelper(u,user_request_url)
#     # obj.permission2action_list
#     string = obj.menu_tree()
#     return render(request,'index.html',{'string':string})

def permission(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login.html')
        obj = MenuHelper(request, user_info['username'])
        action_list = obj.actions()
        if request.path_info != '/backend/index/':
            if not action_list:                     # 对当前url的get，post，put，delete方法中任一个都没权限
                return HttpResponse('无权限访问')
        menu_string = obj.menu_tree()
        kwargs['action_list']=action_list
        kwargs['menu_string']=menu_string
        # 储存在session中用于渲染模板
        request.session['menu_string']=menu_string
        return func(request,*args,**kwargs)
    return inner

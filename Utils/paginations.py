from django.utils.safestring import mark_safe
class Page:

    def __init__(self,current_page,all_count,per_page_count=10,pager_num=7):
        self.current_page = current_page
        self.all_count = all_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
    @property
    def start(self):
        return (self.current_page-1)*self.per_page_count
    @property
    def end(self):
        return (self.current_page)*self.per_page_count
    @property
    def total_count(self):
        v, y = divmod(self.all_count, self.per_page_count)
        if y:
            v += 1
        return v

    def pager_num_range(self):
        # 方式一：返回起始页码，尾页码
        # if self.total_count < self.pager_num:
        #     start_index = 1
        #     end_index = self.total_count + 1
        # else:
        #     if self.current_page <= (self.pager_num + 1) / 2:
        #         start_index = 1
        #         end_index = self.pager_num + 1
        #     else:
        #         start_index = self.current_page - (self.pager_num - 1) / 2
        #         end_index = self.current_page + (self.pager_num + 1) / 2
        #         if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
        #             end_index = self.total_count + 1
        #             start_index = self.total_count - self.pager_num + 1

        # 方式二：返回页码范围range
        if self.total_count < self.pager_num:
            return range(1,self.total_count+1)
        # 总页数特别多
        part = int(self.pager_num/2)
        if self.current_page <= part:
            return range(1,self.pager_num+1)
        if (self.current_page + part) > self.total_count:
            return range(self.total_count-self.pager_num+1,self.total_count+1)
        return range(self.current_page-part,self.current_page+part+1)

    def page_str(self, base_url):
        page_list = []

        first = '<ul class="pagination pagination-sm no-margin">'
        page_list.append(first)

        if self.current_page == 1:
            prev = '<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            prev = '<li><a href="%s?p=%s"aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' %(base_url,self.current_page - 1)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?p=%s">%s</a></li>' % (base_url,i, i)
            else:
                temp = '<li><a href="%s?p=%s">%s</a></li>' % (base_url,i, i)
            page_list.append(temp)
        if self.current_page == self.total_count:
            next = '<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            next = '<li><a href="%s?p=%s"aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (base_url,self.current_page + 1)
        page_list.append(next)
        '''
        jump = """
            <input type="text" class="jump"/><a onclick='jumpto(this);'>GO</a>
            <script>
                function jumpto(ths){
                    var val = ths.previousSibling.value;
                    location.href = "%s?p=" + val;
                }
            </script>    
        """ % (base_url)
        page_list.append(jump)
        '''
        # 页码概要
        end_html = "<li><a href='javascript:void(0)' >共 %d页 / %d 条数据</a></li>" % (self.total_count, self.all_count, )
        page_list.append(end_html)

        last = '</ul>'
        page_list.append(last)

        page_str = ''.join(page_list)
        page_str = mark_safe(page_str)
        return page_str
from django.http import HttpResponse
from celery.result import AsyncResult
from .celery_task import add

task_id=None
def celery_pub(request):
    task = add.delay(22,23)
    global task_id
    task_id = task.id
    # 拿到任务id即可返回，不用等待get获取值，以后再调用id拿值
    return HttpResponse(task.id)

def celery_get(request):
    global task_id
    result = AsyncResult(id=task_id)
    return HttpResponse(result.get())
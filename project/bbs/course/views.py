"""
author: Edgar
课程路由下的页面显示
TODO: 如何显示课程，怎么样显示
"""
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from user.models import ExpData
import time
import os


def index(request):
    """课程界面的首页"""
    return render(request, 'course/index.html')


@require_http_methods(["POST"])
def upload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        exp_type = request.POST.get("type")
        pre_path = os.path.join(os.path.join(settings.BASE_DIR, "media"), "experiment_data/")
        alias = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime()) + file.name
        path = pre_path + alias
        with open(path, "wb") as f:
            for chuck in file.chunks():
                f.write(chuck)
        ExpData.objects.create(user_id=request.user.id,
                               exp_type=exp_type,
                               download_times=0,
                               path=path,
                               name=file.name).save()
        return JsonResponse({"status": "success"})

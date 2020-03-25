from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def login(request):
    """登录处理"""
    if request.method == "POST":
        pass
    else:
        print(request.path)
        print(request.get_host())
        return render(request, 'user/login.html', locals())


@require_http_methods(["GET", "POST"])
def signup(request):
    """注册处理"""
    return render(request, 'user/signup.html', locals())


def forget(request):
    """密码寻回"""
    return HttpResponse("forget")
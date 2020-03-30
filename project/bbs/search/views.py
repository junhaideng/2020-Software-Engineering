"""
author: Edgar
对搜索界面的显示进行处理
TODO: 用户输入的数据后回车，或者点击按钮的界面进行处理 此时url中有参数 keyword， 收集课程的信息
"""
from django.shortcuts import render
from django.http import JsonResponse
from course.models import Course


def search(request):
    """搜索相关"""
    if request.method == 'POST':  # 处理ajax对应的事件，可以实时的获取信息
        value = request.POST.get("value")
        data = []
        if value:
            courses = Course.objects.filter(name__contains=value)  # 查询
            for course in courses:
                data.append({"name": course.name, "id": course.id})
        return JsonResponse({"data": data})  # 返回数据，前端处理显示
    if request.method == "GET":  #
        keyword = request.GET.get("keyword")
        if keyword:  # 如果含有keyword处理 点击search按钮之后的事件
            data = None
            return render(request, 'search/search.html', context={"keyword": keyword, "data": data})
        return render(request, 'search/index.html')  # 否则只是简单的访问该网页

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def search(request):
    """搜索相关"""
    if request.method == 'POST':  # 处理ajax对应的事件，可以实时的获取信息
        return JsonResponse({"data": ["success", "course"]})
    if request.method == "GET":  #
        keyword = request.GET.get("keyword")
        if keyword:  # 如果含有keyword处理 点击search按钮之后的事件
            data = None
            return render(request, 'search/search.html', context={"keyword":keyword, "data":data})
        return render(request, 'search/index.html')  # 否则只是简单的访问该网页

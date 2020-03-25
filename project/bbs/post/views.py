from django.shortcuts import render


def index(request):
    """发帖的界面"""
    return render(request, "post/index.html")

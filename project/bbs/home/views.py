from django.shortcuts import render


# Create your views here.
def home(request):
    """主页面"""
    return render(request, 'home/index.html')

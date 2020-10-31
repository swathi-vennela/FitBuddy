from django.shortcuts import render
def index_view(request):
    return render(request, "home/home.html")
def gallery_view(request):
    return render(request, "home/gallery.html")

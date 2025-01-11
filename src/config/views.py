import pathlib
from django.shortcuts import render
from django.http import HttpResponse
from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent


def home_view(request, *args, **kwargs):
    return about_view(request, *args, **kwargs)


def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    template_name = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, template_name, my_context)

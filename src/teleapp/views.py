import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.first_name)

    return about_view(request, *args, **kwargs)


def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0
    my_title = "My page"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)


def my_old_home_page_view(requests, *args, **kwargs):
    my_title = "My Pages"
    my_context = {
        "page_title": my_title

    }
    html_ = """
        <!DOCTYPE html>
        <html>
            <head>
            
            </head>
            <body>
                <h1> {page_title} </h1>
            </body>
        </html>
    """.format(**my_context)

    # html_file_path = this_dir / "home.html"
    # html_ = html_file_path.read_text()

    return HttpResponse(html_)

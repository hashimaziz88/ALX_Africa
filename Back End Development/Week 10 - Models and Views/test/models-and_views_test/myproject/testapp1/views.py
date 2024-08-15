from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView


class HelloView(TemplateView):
    template_name = "hello.html"


def hello_view(request):
    return HttpResponse("Hello, World")
# Create your views here.

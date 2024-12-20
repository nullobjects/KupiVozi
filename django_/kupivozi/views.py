from django.shortcuts import render
from django.http import HttpResponse, request


def default(request):
    return render(request, 'main.html')

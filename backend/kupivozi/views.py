from django.shortcuts import render

def default(request):
    print("se povika view")
    return render(request, 'main.html')
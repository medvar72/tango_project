from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Rango says Hello World! <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse("Here is the about page <a href='/rango/'>Index<a/>")


from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
# Import the Category model
from rango.models import Category

def index(request):
    # return HttpResponse("Rango says: Hello World! <a href='/rango/about'>About Page</a>")
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # Query the DataBase for a List of All categories currentely stored
    # Order the categories by no. Likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to teh template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {'categories':category_list}

    # Return a rendered response to send to the client.
    # we make use of the shortcut function to make our lives more easier.
    # Note the first parameter is the template we wish to use.
    return render_to_response('rango/index.html',context_dict,context)


def about(request):
    #return HttpResponse("Rango says : Here is the about page <a href='/rango/'>Index Page<a/>")
    context = RequestContext(request)
    context_dict = {'var1': "Value1"}
    return render_to_response('rango/about.html',context_dict,context)


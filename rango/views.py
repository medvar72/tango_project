from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
# Import the Category model
from rango.models import Category,Page
from rango.forms import CategoryForm
from rango.forms import PageForm


#helper function
def encode_decode(category_name_url,encode):
    # Replace " "  by "_" to make category_name url friendly
    if encode:
        category_name_url = category_name_url.replace(' ', '_')
    # Replace "_"  by " " to get the category name without "_"
    else:
        category_name_url = category_name_url.replace('_', ' ')
    return category_name_url

# The add_category() view function can handle three different scenarios:
# showing a new, blank form for adding a category;
# saving form data provided by the user to the associated model, and rendering the Rango homepage; and
# if there are errors, redisplay the form with error messages.

def add_category(request):
    # Get a Context from Request
    context = RequestContext(request)
    # A HTTP POST? There are some data to save
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # Is a valid form?
        if form.is_valid():
            # Save the new Catgory to the Database
            form.save(commit=True)

            # Now we call the index() view
            return index(request)
        else:
            # The supplied form contains errors - just print to the terminal
            print form.errors
    else:
        #  if the request was not a POST was a GET, display the form to enter data. Show a new Blank Form
        form = CategoryForm()

    # Bad form (or form details ), no form supplied...
    return render_to_response('rango/add_category.html',{'form':form},context)

# The add_page() view function can handle three different scenarios:
# showing a new, blank form for adding a page;
# saving form data provided by the user to the associated model, and rendering the Rango homepage; and
# if there are errors, redisplay the form with error messages.

def add_page(request,category_name_url):
    # Get a Context from Request
    context = RequestContext(request)
    # Get Category name from category_name_url
    category_name = encode_decode(category_name_url,False)
    # A HTTP POST? There are some data to save
    if request.method == "POST":
        form = PageForm(request.POST)

        # Is a valid form?
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist :
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)

        else:
            # The supplied form contains errors - just print to the terminal
            print form.errors
    else:
        #  if the request was not a POST was a GET, display the form to enter data. Show a new Blank Form
        form = PageForm()

    # Bad form (or form details ), no form supplied...
    return render_to_response('rango/add_page.html',
        {'category_name_url': category_name_url,
        'category_name': category_name,'form': form},
        context)




def index(request):
    # return HttpResponse("Rango says: Hello World! <a href='/rango/about'>About Page</a>")
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Take the dirs from Settings
    basedir = settings.BASE_DIR
    projectdir = settings.PROJECT_PATH
    templatedir = settings.TEMPLATE_DIRS
    mediadir = settings.MEDIA_ROOT
    # Query the DataBase for a List of All categories currentely stored
    # Order the categories by no. Likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to teh template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list     = Page.objects.order_by('-views')[:5]
    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {'categories':category_list}
    context_dict['pages']= page_list

    context_dict['basedir'] = basedir
    context_dict['projectdir'] =  projectdir
    context_dict['templatedir'] = templatedir
    context_dict['mediadir'] =  mediadir

    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encode URL (eg. spaces replaced with underscores).
    for category in category_list:
         # category.url = category.name.replace(' ', '_')
         category.url = encode_decode(category.name,True)

    # Return a rendered response to send to the client.
    # we make use of the shortcut function to make our lives more easier.
    # Note the first parameter is the template we wish to use.
    return render_to_response('rango/index.html',context_dict,context)


def about(request):
    #return HttpResponse("Rango says : Here is the about page <a href='/rango/'>Index Page<a/>")
    context = RequestContext(request)
    context_dict = {'var1': "Value1"}
    return render_to_response('rango/about.html',context_dict,context)

# Show the several categories with it pages
def category(request,category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # category_name = category_name_url.replace('_', ' ')
    category_name = encode_decode(category_name_url,False)

    # Create a context dictionary which we can pass to the template rendering engine
    # we start by containing the name of category passed by user
    context_dict= {'category_name' : category_name}
    context_dict['category_name_url'] =  category_name_url

    # Can we find a category with with the given name?
    # If we can't the .get method raise a DoesNotExist exception
    # So .get method returns one model instance or raise an Exception.
    try:
        # category = Category.objects.get(name=category_name)
        category = get_object_or_404(Category,name=category_name)

        #Retrieve all pages related to the Category
        # pages = Page.objects.filter(category = category)
        pages = get_list_or_404(Page,category = category)

        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages

        # We also add the category object from the database to the dictionary
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specific category
        # Don't do anything - the template display the "no category" message for us.
        # pass
        return render_to_response('rango/add_category.html', {}, context)

    # Go render the response and return it to the client
    return render_to_response('rango/category.html',context_dict,context)


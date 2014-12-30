from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from datetime import datetime
from rango.bing_search import run_query
from django.core.urlresolvers import reverse
from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView
from datetime import datetime



#helper function
def encode_decode(category_name_url,encode):
    # Replace " "  by "_" to make category_name url friendly
    if encode:
        category_name_url = category_name_url.replace(' ', '_')
    # Replace "_"  by " " to get the category name without "_"
    else:
        category_name_url = category_name_url.replace('_', ' ')
    return category_name_url


def index(request):
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
    # Get the number of visits to the site
    # we use COOKIES.get() function to obtain the visits cookie
    # if the cookie exists, the value returned is casted to an integer
    # if the cookie does not exists, we default to zero and cast that.
    # Cookies in the client side
    # visits = int(request.COOKIES.get('visits',0))

    # Cookies in the server side
    visits = request.session.get('visits')
    if not visits:
        visits = 0
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    # Does the cookie last_visit exists?
    # if 'last_visit' in request.COOKIES:
    if last_visit:
        # Yes it does!, Get the cookie's value
        # last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
        # If it is been more than a day since the last visit ...
        # if (datetime.now() - last_visit_time).days > 0:
        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encode URL (eg. spaces replaced with underscores).
    for category in category_list:
        # category.url = category.name.replace(' ', '_')
        category.url = encode_decode(category.name,True)

    # Return a rendered response to send to the client.
    # we make use of the shortcut function to make our lives more easier.
    # Note the first parameter is the template we wish to use.
    if (request.user.is_authenticated()):
        # return render(request,'rango/index.html',context_dict)
        # Obtain our response objet early so we can add cookie information
        context_dict['visits'] = visits
        request.session['visits'] = visits
        if reset_last_visit_time:
            # response.set_cookie('last_visit',datetime.now())
            request.session['last_visit']= str(datetime.now())
        response = render(request,'rango/index.html',context_dict)
        return response
    # Just in case we want to use the view Index to login
    return HttpResponseRedirect("/accounts/login/")


def about(request):
    # Test a cookie
    # if request.session.test_cookie_worked():
    #     print ">>>> TEST COOKIE WORKED!"
    #     request.session.delete_test_cookie()
    visits = request.session.get('visits')
    if not visits:
        visits = 0
    context_dict = {}
    context_dict['visits'] = visits
    return render(request,'rango/about.html',context_dict)

# Show the several categories with it pages
def category(request,category_name_url):
    # category_name_url is category.slug
    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # category_name = encode_decode(category_name_url,False)

    # Can we find a category with with the given name?
    # If we can't the .get method raise a DoesNotExist exception
    # So .get method returns one model instance or raise an Exception.
    context_dict = {}
    context_dict['result_list']= None
    context_dict['query']= None
    # result_list = []
    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            # run the bing_search
            result_list = run_query(query)
            context_dict['result_list']= result_list
            context_dict['query']= query
    try:
        category = get_object_or_404(Category,slug=category_name_url)
        category_name = category.name
        context_dict['category_name'] = category_name
        context_dict['category_name_url'] =  category_name_url
        # We also add the category object from the database to the dictionary
        context_dict['category'] = category

        # Retrieve all pages related to the Category
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        # We get here if we didn't find the specific category
        # Don't do anything - the template display the "no category" message for us.
        # pass
        category = None
        return render(request,'rango/add_category.html', {})
    if not context_dict['query']:
        context_dict['query'] = category.name

    # Go render the response and return it to the client
    return render(request,'rango/category.html',context_dict)

# The add_category() view function can handle three different scenarios:
# showing a new, blank form for adding a category;
# saving form data provided by the user to the associated model, and rendering the Rango homepage; and
# if there are errors, redisplay the form with error messages.
@login_required
def add_category(request):
    # # Get a Context from Request
    # context = RequestContext(request)
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
    return render(request,'rango/add_category.html',{'form':form})

# The add_page() view function can handle three different scenarios:
# showing a new, blank form for adding a page;
# saving form data provided by the user to the associated model, and rendering the Rango homepage; and
# if there are errors, redisplay the form with error messages.
@login_required
def add_page(request,category_name_url):
    # Wrap the code in a try block - check if the category actually exists!
    try:
        # cat = Category.objects.get(name=category_name)
        cat = Category.objects.get(slug=category_name_url)
    except Category.DoesNotExist :
        # If we get here, the category does not exist.
        # Go back and render the add category form as a way of saying the category does not exist.
        # return render_to_response('rango/add_category.html', {}, context)
        cat = None
    # A HTTP POST? There are some data to save
    if request.method == "POST":
        form = PageForm(request.POST)

        # Is a valid form?
        if form.is_valid():
            if cat:

                # This time we cannot commit straight away.
                # Not all fields are automatically populated!
                page = form.save(commit=False)

                page.category = cat

                # Also, create a default value for the number of views.
                page.views = 0

                page.first_visit = datetime.now()
                page.last_visit = datetime.now()

                # With this, we can then save our new model instance.
                page.save()

                # Now that the page is saved, display the category instead.
                return category(request, category_name_url)
            else:
                form = PageForm()
        else:
            # The supplied form contains errors - just print to the terminal
            print form.errors
    else:
        #  if the request was not a POST was a GET, display the form to enter data. Show a new Blank Form
        form = PageForm()

    # Bad form (or form details ), no form supplied...
    context_dict = {'form': form,'category':cat,'category_name_url':category_name_url,'category_name':cat.name}
    return render(request,'rango/add_page.html',context_dict)


# Method to implement the register processs
def register(request):
    # # get the context request
    # context = RequestContext(request)
    # a boolean vallue to telling the template whether the registration was sucessfull.
    # Set to False initially. Code Chancges value to True when the registration succeds.
    registered = False

    # if it is a HTTP POST we are interested in processing form data.
    if request.method == 'POST':
        # Attemp to grab information from the raw form information
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if both form are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user data to  database.
            user = user_form.save()

            # We hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=false
            # This delays saving the model until we are ready to avoid integrity problems
            user_profile = profile_form.save(commit=False)
            user_profile.user = user

            # Did the user provide a profile picture?
            #  If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            user_profile.save()

            # Update our variable to tell the template registration was sucesfull
            registered = True

        # Invalid  form or forms - mistakes or something else
        # print the problems to the terminal
        # They will also shown to the user
        else:
            print user_form.errors, profile_form.errors
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # these forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on Context
    if not registered:
        return render(request,'rango/register.html',
            {'user_form':user_form,'profile_form':profile_form, 'registered':registered})
    else:
        return HttpResponseRedirect('/accounts/register/complete/')



@login_required
def content_restricted(request):
    return render(request,'rango/restricted.html',{})

# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)

#     # take the user back to the homepage
#     return HttpResponseRedirect('/rango/')

@login_required
def profile(request):
    return render(request,template_name='rango/profile.html')

def register_profile(request):
    # # get the context request
    # context = RequestContext(request)
    # a boolean value to telling the template whether the registration was sucessfull.
    # Set to False initially. Code Chancges value to True when the registration succeds.
    registered = False

    # if it is a HTTP POST we are interested in processing form data.
    if request.method == 'POST':
        # Attemp to grab information from the raw form information
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=false
            # This delays saving the model until we are ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            # profile.user = user

            # Did the user provide a profile picture?
            #  If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to tell the template registration was sucesfull
            registered = True

        # Invalid  form or forms - mistakes or something else
        # print the problems to the terminal
        # They will also shown to the user
        else:
            print profile_form.errors
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # these forms will be blank, ready for user input
    else:
        profile_form = UserProfileForm()

    # Render the template depending on Context
    return render(request,'rango/profile_registration.html',
        {'profile_form':profile_form, 'registered':registered})

def search(request):
    result_list = []

    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            # run the bing_search
            result_list = run_query(query)
    return render(request,'rango/search.html',{'result_list':result_list})

def track_url(request):
    page_id = None
    url='/rango/'
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views+=1
                if (page.views == 1):
                    page.first_visit = datetime.now()
                else:
                    page.last_visit = datetime.now()
                page.save()
                url = page.url
                print url
            except:
                pass
    return HttpResponseRedirect(url)

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        if 'category_id' in request.GET:
            cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes+1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

# helper function to get a Category List
def get_category_list(max_results=0,starts_with=''):
    cat_list = []

    if len(starts_with.strip()) > 0:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    context_dict = {}
    starts_with = ''
    max_results = 8 #Top Results
    if request.method == 'GET':
        if 'suggestion' in request.GET:
            starts_with = request.GET['suggestion']
    cat_list = get_category_list(max_results,starts_with)
    context_dict['cats'] = cat_list
    return render(request,'rango/cats.html',context_dict)


@login_required
def auto_add_page(request):
    cat_id = None
    pag_title = None
    pag_url = None
    context_dict = {}
    if request.method == 'GET':
        if 'category_id' in request.GET:
            cat_id = request.GET['category_id']
            print 'cat_id: ' + cat_id
        if 'page_title' in request.GET:
            pag_title = request.GET['page_title']
            print 'page_title: ' + pag_title
        if 'page_url' in request.GET:
            pag_url = request.GET['page_url']
            print 'page_url: '+  pag_url

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        p = Page.objects.get_or_create(category=cat,title=pag_title,url=pag_url)
        pages = Page.objects.filter(category=cat).order_by('-views')
        context_dict['pages'] = pages
    return render(request,'rango/page_list.html',context_dict)








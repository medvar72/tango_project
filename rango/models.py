from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from registration.signals import user_registered


# Create your models here.
class Category(models.Model):
    name  = models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug  = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)

        if self.views >= 0:
            super(Category, self).save(*args, **kwargs)
        else:
            self.views = self.views * (-1)
            # raise ValueError('Negative Value to Views')



    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links userProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to = 'profile_images',null=True,blank=True)

    # Override the __unicode__() method to return something meaningful!
    def __unicode__(self):
        return self.user.username

def user_registered_callback(sender,user,request,**kwargs):
    profile = UserProfile(user=user)
    profile.website = request.POST["website"]
    if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
    profile.save()

user_registered.connect(user_registered_callback)

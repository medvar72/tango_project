from django.contrib import admin
from rango.models import Category, Page, UserProfile
# Register your models here.

# To edit Model Page into Category Form
class PageInline(admin.TabularInline):
     model = Page
     extra = 3


class PageAdmin(admin.ModelAdmin):
      fieldsets = [
        (None, {'fields':['title']}),
        ('Details',{'fields':['category','url','views','first_visit','last_visit'],'classes':['collapse']}),
    ]
      list_display = ('title','category','url','views','first_visit','last_visit')
      list_filter = ['title','category']
      search_fields = ['title']

class CategoryAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug':('name',)}
      fieldsets = [
        ('Category ', {'fields':['name','views','likes']}),
    ]
      inlines = [PageInline] # To edit Model Page into Category Form
      list_display = ('name',)
      list_filter = ['name']
      search_fields = ['name']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)

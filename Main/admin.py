from django.contrib import admin
from Main.models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tweet)
admin.site.register(Following)
admin.site.register(Follower)
admin.site.register(Favourite)
admin.site.register(Retweet)
admin.site.register(Notification)

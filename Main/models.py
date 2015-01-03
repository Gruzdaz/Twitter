from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

	      
class Favourite(models.Model):
	favourite = models.CharField(max_length=140)
	def __unicode__(self):
		return self.favourite
		
class Retweet(models.Model):
	retweet = models.CharField(max_length=140)
	def __unicode__(self):
		return self.retweet
		
class Follower(models.Model):
	follower = models.CharField(max_length=140)
	def __unicode__(self):
		return self.follower
	
class Following(models.Model):
    following = models.CharField(max_length=140) 
    def __unicode__(self):
		return self.following
	     
class Tweet(models.Model):
	text = models.CharField(max_length=140)
	date = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=140)
	favourite = models.ManyToManyField(Favourite)
	retweet = models.ManyToManyField(Retweet)
	replies = models.ManyToManyField('Tweet')
	is_ret = models.BooleanField(default=False)
	retweeter = models.CharField(max_length=140, default = "username")

        
	def __unicode__(self):
		return self.username

class Notification(models.Model):
	notification = models.CharField(max_length=140)
	user = models.CharField(max_length=140)
	tweet_id = models.CharField(max_length=140)
	def __unicode__(self):
		return self.tweet_id
	      
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    website = models.URLField()
    followers = models.ManyToManyField(Follower)
    following = models.ManyToManyField(Following)
    tweets = models.ManyToManyField(Tweet)
    notification = models.ManyToManyField(Notification)
    
    def __unicode__(self):	
		return self.user.username
        

		

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages

from Main.models import *

from Twitter.forms import UserForm, UserProfileForm, TweetForm

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()


            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
            
def home_page(request):
  # Obtain the context for the user's request.
  context = RequestContext(request)
  
  # If the request is a HTTP POST, try to pull out the relevant information.
  if request.method == 'POST':
    
    if request.POST.get('reply'):
      return HttpResponseRedirect('/reply/' + request.POST['idtweet'])
    
      
    # Whether the user clicked "Favourite" button
    if request.POST.get('favourite'):
      user_object = Favourite(favourite = request.user.username) # Getting user's username
      tweet_id = request.POST['idtweet'] # Getting exactly tweet
      tweet_object = Tweet.objects.get(id=tweet_id)
      in_list = False
      
      # Checking if user is already favourited the tweet
      for user in tweet_object.favourite.all():
	if user.favourite == request.user.username:
	  in_list = True
      
      if in_list:
	return HttpResponse("Your already have favourited this tweet.")
      
      if not in_list:
	user_object.save() 
	tweet_object.favourite.add(user_object) # Adding username to tweet
	return HttpResponseRedirect(reverse('home_page'))
      
    if request.POST.get('retweet'):
	retweet_object = Retweet(retweet = request.user.username) # Getting user's username
	tweet_id = request.POST['idtweet'] # Getting exactly tweet
	tweet_object = Tweet.objects.get(id=tweet_id)
	in_list = False
	
	# Checking if user is already favourited the tweet
	for user in tweet_object.retweet.all():
	  if user.retweet == request.user.username:
	    in_list = True
	
	if in_list:
	  return HttpResponse("Your already have retweeted this tweet.")
	
	if not in_list:
	  retweet_object.save() 
	  tweet_object.retweet.add(retweet_object) # Adding username to tweet
	  
	  user_object = UserProfile.objects.get(user__username__iexact=request.user.get_username())
	  new_tweet = Tweet.objects.create(text = tweet_object.text, date = tweet_object.date, username = tweet_object.username, is_ret = True, retweeter = user_object.user.username)
	  for retweet in tweet_object.retweet.all():
	    new_tweet.retweet.add(retweet)
	  
	  for favourite in tweet_object.favourite.all():
	    new_tweet.favourite.add(favourite)
	  
	  new_tweet.save()
	  user_object.tweets.add(new_tweet)
	  
	  # Making notifiaction
	  notification = Notification(notification = " have retweeted your", user = request.user.username, tweet_id = tweet_id)
	  notification.save()
	  star_user = UserProfile.objects.get(user__username=tweet_object.username)
	  star_user.notification.add(notification)
	  
	  return HttpResponseRedirect(reverse('home_page'))
      
    if request.POST.get('tweet'):
      form = TweetForm(request.POST)
      if form.is_valid():
	author = form.save(commit=False)
	author.username = request.user.username  # use your own profile here
	author.save()
	user_object = UserProfile.objects.get(user__username__iexact=request.user.get_username())
	tweet_object = Tweet.objects.get(pk=author.pk)
	user_object.tweets.add(tweet_object)
	
	#Making notification
	
	return HttpResponseRedirect(reverse('home_page'))
    else:
	# Gather the username and password provided by the user.
	# This information is obtained from the login form.
      username = request.POST['username']
      password = request.POST['password']
	# Use Django's machinery to attempt to see if the username/password
	#combination is valid - a User object is returned if it is.
      user = authenticate(username=username, password=password)
	# If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
      if user:
	  # Is the account active? It could have been disabled.
	if user.is_active:
	    # If the account is valid and active, we can log the user in.
	    # We'll send the user back to the homepage.
	  login(request, user)
	  return HttpResponseRedirect(reverse('home_page'))
	else:
	    # An inactive account was used - no logging in!
	  return HttpResponse("Your Rango account is disabled.")
      else:
      # Bad login details were provided. So we can't log the user in.
	print "Invalid login details: {0}, {1}".format(username, password)
	return HttpResponse("Invalid login details supplied.")
  else:  # No POST request data
    form = TweetForm()
    if request.user.is_authenticated(): # Is the user logged in
      object1 = UserProfile.objects.get(user__username__iexact=request.user.get_username()) # User's nickname
      tweets = []
      
      for user in object1.following.all(): # Who user is following
	object2 = UserProfile.objects.get(user__username = user.following)
	user_tweets = object2.tweets.all() # Getting following people tweets
	for tweet in user_tweets:
	  tweets.append(tweet)
	  
      for i in range(len(tweets)): # Ordering tweets with "Bubble" strategy by date
	for j in range(i+1, len(tweets)):
	  if tweets[j].date > tweets[i].date:
	    tweets[j], tweets[i] = tweets[i], tweets[j]
      return render_to_response('login.html', {'tweets':tweets, 'form':form}, context)
    else:
      return render_to_response('login.html', {}, context)


@login_required # Only logged in user's can see this page
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('home_page'))

      
      
def timeline(request, username):
  # Obtain the context for the user's request.
  context = RequestContext(request)
  try:
    user = UserProfile.objects.get(user__username__iexact=username) # If there is such user?
  except:
    return HttpResponse("User not found") # Nope..
  
  # If yes:
  object1 = UserProfile.objects.get(user__username__iexact=username)
  tweets = object1.tweets.all() # All user's tweets
  count = len(tweets.all()) # How many tweets?
  foll1 = len(user.followers.all()) # How many followers?
  foll2 = len(user.following.all()) # How many following?
  if request.user.is_authenticated():
    user_object = UserProfile.objects.get(user__username__iexact=request.user.get_username()) # Logged in user
    
    if request.GET.get('follow'): # If user clicked button "Follow"
      in_list = False
      
      # Checking if user is already following that user
      for follower in user.followers.all():
	if follower.follower == request.user.username:
	  in_list = True
	  
      # If not
      if not in_list:
	follower = Follower(follower = request.user.username)
	following = Following(following = user.user.username)
	follower.save()
	following.save()
	user.followers.add(follower)
	user_object.following.add(following)
	return HttpResponseRedirect(reverse('home_page'))
	
      # If yes
      if in_list: return HttpResponse("You already following this user")
  return render_to_response('timeline.html', {'tweets': reversed(tweets), 'count':count, 'username':user.user.username, 'foll2':foll2,
	'foll1':foll1, 'useris':object1}, context)

def favourited(request, tweetsid):
  user_objects = []
  tweet = Tweet.objects.get(id = tweetsid)
  for user in tweet.favourite.all():
    user_objects.append(user)
  return render_to_response('favourite.html', {'users':user_objects})

def retweeted(request, tweetsid):
  user_objects = []
  tweet = Tweet.objects.get(id = tweetsid)
  for user in tweet.retweet.all():
    user_objects.append(user)
  return render_to_response('retweet.html', {'users':user_objects})

def following(request, usersid):
  user_objects = []
  user = UserProfile.objects.get(id = usersid)
  for user in user.following.all():
    user_objects.append(user)
  return render_to_response('following.html', {'users':user_objects})

def followers(request, usersid):
  user_objects = []
  user = UserProfile.objects.get(id = usersid)
  for user in user.followers.all():
    user_objects.append(user)
  return render_to_response('followers.html', {'users':user_objects})

@login_required 
def reply(request, tweetsid):
  context = RequestContext(request)
  tweet = Tweet.objects.get(id = tweetsid)
  if request.method == 'POST':
    form = TweetForm(request.POST)
    if form.is_valid():
      author = form.save(commit=False)
      author.username = request.user.username  # use your own profile here
      author.save()
      reply_object = Tweet.objects.get(pk=author.pk)
      tweet.replies.add(reply_object)
      return HttpResponseRedirect(reverse('home_page'))
  else:
    form = TweetForm()
    replies = []
    for reply in tweet.replies.all():
      replies.append(reply)
  return render_to_response('reply.html', {'tweet':tweet, 'replies':replies, 'form':form}, context)



def notification(request):
  context = RequestContext(request)
  user_object = UserProfile.objects.get(user__username=request.user.get_username())
  notifications = []
  for notif in user_object.notification.all():
    notifications.append(notif)
    
  return render_to_response('notification.html', {'notif':notifications}, context)


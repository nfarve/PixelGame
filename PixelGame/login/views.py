from django.shortcuts import render
from django.shortcuts import render_to_response
from login.forms import UserForm
from django.contrib.auth.models import User
from django import forms
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from game.models import UserProfile

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid():
            user = user_form.save()
            holder = user.password
            user.set_password(user.password)
            user.save()
            userProfile = UserProfile()
            userProfile.user=user
            userProfile.save()
            registered = True
            userLogin = authenticate(username=user.username, password=holder)
            if userLogin:
            # Is the account active? It could have been disabled.
                if userLogin.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, userLogin)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("Your account is disabled.")    
            else:
            # Bad login details were provided. So we can't log the user in.
                print "Invalid login details: {0}, {1}".format(user.username, user.password)
                return HttpResponse("Invalid login details supplied.")    
        else:
            print user_form.errors
            return HttpResponse(user_form.errors)

    else:
        user_form = UserForm()
        return render_to_response(
            'register.html',
            {'user_form': user_form, 'registered': registered},context_instance=RequestContext(request) )

def user_login(request):
	 # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
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
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def logout_user(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
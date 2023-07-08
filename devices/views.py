from django.shortcuts import render
from django.http import Http404
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user


    title = 'Home'

    return render(request, 'all-posts/home.html',
                  { "title": title, "user": current_user, })


@login_required(login_url='/accounts/login/')
def profile(request,id):
    '''	
    View function to display the profile of the logged in user when they click on the user icon	
    '''
    current_user = request.user

    try:

        single_profile = Profile.objects.get(user=current_user.id)

        title = f'{current_user.username}\'s'

        posts = Post.objects.filter(user=current_user.id)

        return render(request, 'all-posts/my_profile.html', {"title":title,"single_profile":single_profile,"current_user":current_user,"posts":posts})

    except ObjectDoesNotExist:
        raise Http404()
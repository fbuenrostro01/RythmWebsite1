from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import random



from app.models import *



# Create your views here.

def login_func(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            print("tes for the ternminal t")
            return redirect("game_page")
        else:
            messages.info(request,"username or password incorrect")
            
    context={}
    return render(request,"login.html",context)



# kicks user out when they click on log out
#termintes teh seccsion 
def logout_func(request):
    logout(request)
    return redirect('login_page')


#they can only biew the page if the are logg otheriwse i have them redirect to login 
@login_required(login_url='login_page')  
def high_score_func(request):
    if request.method=='POST':
    #this is for checking if they are admin user currenly only habe Admin coded for it
        if request.user.is_superuser and 'username_to_delete' in request.POST:
            username_to_delete=request.POST.get('username_to_delete')
        
            user_to_delete=User.objects.get(username=username_to_delete)
            user_scores=UserHighScore.objects.filter(user=user_to_delete)
            if user_scores.exists():
                user_scores.delete()
                messages.success(request,f"Scores for {user_to_delete.username} have been deleted.")
            else:
                messages.info(request,f"No scores found for {user_to_delete.username}.")
        
        elif not request.user.is_superuser:
            user_scores=UserHighScore.objects.filter(user=request.user)
            if user_scores.exists():
                user_scores.delete()
                messages.success(request, "All your scores have been successfully deleted.")
            else:
                messages.info(request, "You don't have any scores to delete.")

        return redirect('high_scores_page')

  
    user_score=UserHighScore.objects.filter(user=request.user).first()
    all_scores=UserHighScore.objects.all().order_by('-score')
    all_users= User.objects.all()

    return render(request, 'HighScores.html', {
        'user_score': user_score,
        'all_scores': all_scores,
        'all_users': all_users,
    })


def register_func(request):
    form=CreateUserForm()

    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get("username")
           
            return redirect("game_page")

    context={'form':form}
    return render(request,"register.html",context)




#sit whows the the high scores to the main game page table
#only tirgres if they a logged othewise i kick them to the login page

@login_required(login_url='login_page')
def show_game_func(request):
    if request.method=="POST" and "test_score" in request.POST:
        user_score, created=UserHighScore.objects.get_or_create(user=request.user)
        user_score.score=random.randint(1000, 5000)
        user_score.save()
       
        return redirect("game_page")
    #dont think inee to use try but for erros might as welll
    try:
        user_score=UserHighScore.objects.get(user=request.user)
    except UserHighScore.DoesNotExist:
        user_score=None

    return render(request, "Game.html", {'user_score': user_score})


    


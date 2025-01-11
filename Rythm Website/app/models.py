from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.


class CreateUserForm(UserCreationForm):
    password2=forms.CharField(
        label="Confirm Password",  
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
        error_messages={
            'password_mismatch': "Passwords do not match. Please try again."
        },
    )

    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]

class UserHighScore(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    #datetime field for letting me automattically record the date the score was made
    #i can overwrite it if they make a new score 
    #remever to implement into score table if i have time
    date_played=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"User: {self.user.username}  Score: {self.score}"


#testing the score they get form teh game remever to removed
#currently manually assiging score

class UserHighScoreForm(forms.ModelForm): 
    class Meta:
        model=UserHighScore
        fields=['score']

   

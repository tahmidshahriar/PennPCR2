from django import forms
from newcourse.models import ClassComment, UserProfile, ProfComment
from django.contrib.auth.models import User


class ClassCommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, help_text="Enter Comment")
    bookuseful = forms.CharField(help_text="Would you recommend buying the textbook?", required=False)
    yourprof = forms.CharField(help_text="Please name your professor")
    class Meta:
        model = ClassComment
        fields = ('description', 'bookuseful', 'yourprof')

class ProfCommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, help_text="Enter Comment")
    whichclass = forms.CharField(help_text="Which class did you take")

    class Meta:
        model = ProfComment
        fields = ('description', 'whichclass')



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="Alphanumeric Only.")
    email = forms.CharField(help_text="Penn Email")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def clean_email(self):
        User.email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(("This email address is already in use. Please supply a different email address."))

        User.username = self.cleaned_data["username"]

        if not ((User.email)).endswith('.upenn.edu'):
            raise forms.ValidationError(("Not a valid Penn email"))


        if not User.username.isalnum():
            raise forms.ValidationError(("Contains non-alphanumberic characters."))

        return self.cleaned_data['email']

class UserProfileForm(forms.ModelForm):
    activation_key = forms.CharField(widget=forms.HiddenInput(), initial=0)
    school = forms.CharField(widget=forms.HiddenInput(), required =False)
    class Meta:
        model = UserProfile
        fields = ('activation_key',)

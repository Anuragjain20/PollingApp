
from django import forms
from .models import *



class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Password") 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Confirm Password")    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email',  'phone']
        
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
      
        
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ForgetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True)    

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return self.cleaned_data
        else:
            raise forms.ValidationError("This email is not registered")    


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Password") 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Confirm Password") 

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data        

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True)        
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered")
        else:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Password is incorrect")
            elif not user.is_verified:
                raise forms.ValidationError("User is not verified")    
            else:
                return self.cleaned_data


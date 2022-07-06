
from .models import *
from django import forms

widgets = forms.TextInput(attrs={'class':'form-control'})
class PollAddForm(forms.ModelForm):
    choice1 = forms.CharField(max_length=255,min_length=1,required=True,label="Choice 1",widget= widgets)
    choice2 = forms.CharField(max_length=255,min_length=1,required=True,label="Choice 2",widget= widgets)
    choice3 = forms.CharField(max_length=255,min_length=1,required=True,label="Choice 3",widget= widgets)
    choice4 = forms.CharField(max_length=255,min_length=1,required=True,label="Choice 4",widget= widgets)



    class Meta:
        model = Poll
        fields = ['text','choice1','choice2','choice3','choice4']
        widgets = {
            'text': forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20}),
        
        }
        labels = {
            'text':'Poll Question',
        }
        


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text' ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
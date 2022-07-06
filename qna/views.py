from email import message
from ftplib import all_errors
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from accounts.models import *
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
@login_required(login_url = '/accounts/login/')
def index(request):


    all_polls = Poll.objects.filter(active = True).order_by('-created_at')



    paginator = Paginator(all_polls, 6) 
    page = request.GET.get('page')
    polls = paginator.get_page(page)


    context = {
        'polls': polls,
       
    }
    return render(request, 'index.html', context)

@login_required(login_url = '/accounts/login/')
def add_poll(request):
    try:
        if request.user.number_of_question_allowed <0:
            messages.error(request,"You have reached your limit of polls.")
            return redirect('/profile/')
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            if form.is_valid():
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                for i in range(1,5):
                    Choice.objects.create(poll = poll, choice_text = form.cleaned_data[f"choice{i}"])

                request.user.number_of_question_allowed -= 1
                request.user.save()
                
                messages.success(request,"Poll created successfully")
                return redirect('/profile/')
        else:

            form = PollAddForm()
        return render(request, 'add_poll.html', {'form': form})
    except Exception as e:
        print(e)
        form = PollAddForm()
        messages.error(request,"Something went wrong with your poll creation. Please try again")
        return render(request, 'add_poll.html', {'form': form})



@login_required(login_url = '/accounts/login/')
def profile(request):
    user = request.user
    polls = user.polls.all()

    context = {
        'user': user,
        'polls': polls,
        
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/accounts/login/')
def edit_poll(request, id):
    try:
        poll = Poll.objects.get(id = id)
        if request.user != poll.owner:
            messages.error(request,"You are not allowed to edit this poll")
            return redirect('/')
        if request.method == 'POST':
            form = EditPollForm(request.POST, instance=poll)
            if form.is_valid():
                poll = form.save(commit=False)
                poll.save()
                messages.success(request,"Poll edited successfully")
                return redirect('/profile/')
        else:
            form = EditPollForm(instance=poll)
            choices = poll.choice.all()
            context = {
                'form': form,
                'choices': choices,
               
            }
         
        return render(request, 'edit_poll.html', context)
    except Exception as e:
        print(e)
        
        messages.error(request,"Something went wrong with your poll editing. Please try again")
        return redirect('/profile/')

@login_required(login_url='/accounts/login/')
def edit_choices(request,id):
    try:
        choice = Choice.objects.get(id=id)
        if request.method == 'POST':
            form = EditChoiceForm(request.POST, instance=choice)
            if form.is_valid():
                choice = form.save(commit=False)
                choice.save()
                messages.success(request,"Choice edited successfully")
                return redirect('/profile/')
        else:
            form = EditChoiceForm(instance=choice)
        return render(request, 'edit_choices.html', {'form': form})
    except Exception as e:
        print(e)
        messages.error(request,"Something went wrong with your choice editing. Please try again")
        return redirect('/profile/')




def poll_detail(request, id):
    poll = get_object_or_404(Poll, id=id)

    if not poll.active:
        return render(request, 'poll_result.html', {'poll': poll})
    choices = poll.choice.all()
    context = {
        'poll': poll,
        'choices': choices
    }
    return render(request, 'poll_detail.html', context)


@login_required
def poll_vote(request, id):
    try:
        poll = get_object_or_404(Poll, id=id)
        choice_id = request.POST.get('choice')
    
        if not poll.user_can_vote(request.user):
            messages.error(
                request, "You already voted this poll!")
            return redirect("/")
  
        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            vote = Vote(user=request.user, poll=poll, choice=choice)
            vote.save()
            messages.success(request, "You voted successfully!")
            return render(request, 'poll_result.html', {'poll': poll})
        else:
            messages.error(
                request, "No choice selected!")
            return redirect(f"/poll/{poll.id}/")
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong!")
        return redirect("/")        
 

def result_view(request,id):
    poll = get_object_or_404(Poll,id=id)
    context = {
        'poll': poll
    }
    return render(request, 'poll_result.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name = "public-chat")
    chat_messages = chat_group.chat_messages.all()[:30] # Get the latest 30 messages since the ordering is based on '-created' in models.py

    form = ChatMessageCreateForm()

    # if request.method == "POST":
    if request.htmx: # Both if POST and if htmx also works, decided to use if htmx
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            # If you call save() with commit=False , then it will return an object that hasn't yet been saved to the database.
            # Saving with commit=False gets you a model object, then you can add your extra data and save it.
            message = form.save(commit = False) 
            message.author = request.user # Add author to the message object
            message.group = chat_group # Add chat group to the message object
            message.save()

            # return redirect('home')
            '''
            return redirect('home') requires refresh of the entire page every time a new message is sent
            We only want to load the new message, and keep the rest of the page the same. Therefore, we
            need to render partials/chat_message_p.html
            '''

            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form})


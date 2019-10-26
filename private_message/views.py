from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from main_app.utils import get_friends
from private_message.models import getAllMessages, Private_Message
from users.models import CustomUser
# Create your views here.

def friends_message(request):
    my_friends = get_friends(request.user)
    context = {'my_friends': my_friends}
    context['display_message_box'] = False
    if request.method=='POST':
        friend_username = request.POST.get("friend_username", "null")
        friend_user = CustomUser.objects.get(username=friend_username)

        # if request.POST.get("button_clicked", "null") == "send_message":
        #     message_text = request.POST.get("message_text", "null")
        #     Private_Message.objects.create(sender=request.user, receiver=friend_user, message=message_text)

        context['friend_username'] = friend_username
        context['chats'] = getAllMessages(user1=request.user, user2=friend_user)
        context['display_message_box'] = True

    return render(request, 'private_message.html', context)

def send_message(request):
    friend_username = request.POST.get('friend_username', 'null')
    friend_user = CustomUser.objects.get(username=friend_username)
    message_text = request.POST.get("message_text", "null")
    my_friends = get_friends(request.user)
    Private_Message.objects.create(sender=request.user, receiver=friend_user, message=message_text)
    context = {'my_friends': my_friends}
    context['chats'] = getAllMessages(user1=request.user, user2=friend_user)
    context['friend_username'] =friend_username
    context['display_message_box'] = True
    return redirect('private_message:friends_message')
    # return render(request, 'private_message.html', context)

def chat(request):
    user1 = request.user
    user2_id = request.POST.get("user_id")
    user2 = CustomUser.objects.get(id=user2_id)
    messages = getAllMessages(user1, user2)
    context = {"messages": messages}
    return render(request, 'chat.html', context)
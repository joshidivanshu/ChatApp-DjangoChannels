from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ChatForm
from .models import ChatGroup
from tortoise import Tortoise
from django.conf import settings
from asgiref.sync import sync_to_async
# Create your views here.
from .tortoise_models import ChatMessage

def index(request):
    return render(request, 'chat/index.html')


def get_participants(group_id=None, group_obj=None, user=None):
    """ function to get all participants that belong the specific group """
    
    if group_id:
        chatgroup = ChatGroup.objects.get(id=id)
    else:
        chatgroup = group_obj

    temp_participants = []
    for participants in chatgroup.user_set.values_list('username', flat=True):
        if participants != user:
            temp_participants.append(participants.title())
    temp_participants.append('You')
    return ', '.join(temp_participants)


def room(request, group_id):
    if request.user.groups.filter(id=group_id).exists():
        chatgroup = ChatGroup.objects.get(id=group_id)
        #TODO: make sure user assigned to existing group
        assigned_groups = list(request.user.groups.values_list('id', flat=True))

        # accessing users
        users = User.objects.select_related('logged_in_user')
        for user in users:
            user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
        

        groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)
        return render(request, 'chat/room.html', {
            'roomName': chatgroup,
            'participants': get_participants(group_obj=chatgroup, user=request.user.username),
            'groups_participated': groups_participated,
            'users': users,
        })
    else:
        return HttpResponseRedirect(reverse("unauthorized"))


class RegisterView(View):
    def get(self, request):
        return render(request, "chat/register.html", {"form": UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse("login"))

        return render(request, "chat/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        return render(request, "chat/login.html", {"form": AuthenticationForm})

    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(
                    request, "chat/login.html", {"form": form, "invalid_creds": True}
                )

            login(request, form.get_user())

            return redirect(reverse("index"))

        return render(request, "chat/login.html", {"form": form})


class LogoutViewClass(LogoutView):
    template_name = "chat/room.html"


class AddView(View):
    def get(self, request):
        return render(request, "chat/addgroup.html", {"form": ChatForm()})
    

    def post(self, request):
        form = ChatForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse("login"))

        return render(request, "chat/register.html", {"form": form})


def unauthorized(request):
    return render(request, 'chat/unauthorized.html', {})


async def history(request, room_id):

    await Tortoise.init(**settings.TORTOISE_INIT)
    chat_message = await ChatMessage.filter(room_id=room_id).order_by('date_created').values()
    await Tortoise.close_connections()

    return await sync_to_async(JsonResponse)(chat_message, safe=False)


async def delete_chat(request,room_id, id):
    await Tortoise.init(**settings.TORTOISE_INIT)
    delete_message = await ChatMessage.filter(id=int(id)).delete()
    chat_message = await ChatMessage.filter(room_id=room_id).order_by('date_created').values()
    await Tortoise.close_connections()
    
    return await sync_to_async(JsonResponse)(chat_message, safe=False)
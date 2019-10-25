from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from groups.models import Groups, giveMyGroups, getOwnedGroups, giveGroupMembers, giveOtherGroups, Group_Members, \
    getMyPendingRequests, getPendingRequests
from .forms import GroupCreateForm


class ShowGroups(TemplateView):
    template_name = 'groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_groups'] = giveMyGroups(self.request.user)
        context['other_groups'] = giveOtherGroups(self.request.user, context['member_groups'])
        context['sent_requests'] = getMyPendingRequests(self.request.user)
        # print(context['member_groups'])
        return context


class MyGroups(TemplateView):
    template_name = 'group_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_groups'] = getOwnedGroups(self.request.user)
        # print(context['my_groups'])
        return context


def groupsView(request):
    group_id = request.POST.get("group_id", "default")
    obj = Groups.objects.get(pk=group_id)
    x = giveGroupMembers(obj)
    pending_requests = getPendingRequests(obj)
    context = {'members': x, 'group_id': group_id, 'member_requests': pending_requests}
    return render(request, 'group_view.html', context)


def AddJoinRequest(request):
    group_id = request.POST.get("group_id", "default")
    new_member = Group_Members.objects.create(member=request.user, group_id=group_id, confirmed=False)
    new_member.save()
    return HttpResponseRedirect(reverse('groups:group'))


def addgroup(request):
    if request.method == "POST":
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            description = form.cleaned_data['description']
            fees = form.cleaned_data['fees']
            obj = Groups.objects.create(group_name=group_name, description=description, fees=fees, admin_id=request.user.id)
            obj.save()
            return HttpResponseRedirect(reverse('groups:add_group'))
    else:
        form = GroupCreateForm()
    return render(request, 'create_group.html', {'form': form})


def cancelJoinRequest(request):
    group_id = request.POST.get("group_id", "default")
    # print(group_id, request.user)
    Group_Members.objects.filter(member=request.user, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group'))


def removeFromGroup(request):
    group_id = request.POST.get("group_id", "default")
    Group_Members.objects.filter(member=request.user, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group'))


def acceptJoinRequest(request):
    group_id = request.POST.get("group_id", "default")
    member_id = request.POST.get("member_id", "default")
    # print(group_id, member_id)
    obj = Group_Members.objects.get(member_id=member_id, group_id=group_id)
    obj.confirmed = True
    obj.save()
    return HttpResponseRedirect(reverse('groups:group_admin'))


def rejectJoinRequest(request):
    group_id = request.POST.get("group_id", "default")
    member_id = request.POST.get("member_id", "default")
    Group_Members.objects.get(member_id=member_id, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group_admin'))
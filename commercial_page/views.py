from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from commercial_page.models import getAllPages, CommercialPage, getAllPosts, CommercialPagePosts


def page_list(request):
    pages = getAllPages(request.user)
    context = {'pages' : pages}
    return render(request, 'page_list.html', context=context)

def page_timeline(request, page_id):
    # page_id = request.POST.get("page_id", "null")
    page = CommercialPage.objects.get(id=page_id)
    context = {}
    context['page'] = page
    context['posts'] = getAllPosts(page).order_by('-date')
    return render(request, 'page_timeline.html', context=context)

def add_post(request):
    page_id = request.POST.get("page_id", "null")
    page = CommercialPage.objects.get(id=page_id)
    post_text = request.POST.get("post_text", "null")
    CommercialPagePosts.objects.create(page=page, post_text=post_text)
    return HttpResponseRedirect(reverse('commercial_page:page_timeline', kwargs={'page_id' : page_id}))
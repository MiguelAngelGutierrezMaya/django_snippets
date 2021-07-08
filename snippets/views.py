# Python
import datetime

# Pygments
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


# Django confs
from django.conf import settings

# Django libraries
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic.base import View
from django.contrib.auth import (
    login as logIn, logout as logOut, authenticate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Models
from snippets.models import Language
from snippets.models import Snippet


def login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'site': {'baseurl': settings.STATIC_URL, 'docs_version': settings.APP_VERSION}})
        else:
            return redirect(settings.LOGIN_REDIRECT_URL)
    elif request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            logIn(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'login.html', {
                'site': {
                    'baseurl': settings.STATIC_URL,
                    'docs_version': settings.APP_VERSION
                },
                'form': {
                    'error': {
                        'msg': 'Credenciales inválidas',
                        'username': request.POST['username']
                    }
                }
            })


@login_required
def logout(request):
    logOut(request)
    return redirect(settings.LOGIN_URL)


# Aux functions
def addAgoSnippets(snippets):
    for snippet in snippets:
        duration = (datetime.datetime.now() -
                    snippets[0].created.replace(tzinfo=None))
        if duration.days == 0:
            duration_in_s = int(duration.total_seconds())
            days = divmod(duration_in_s, 86400)
            ago = str(divmod(days[1], 3600)[0]) + ' horas'
        elif duration.days == 1:
            ago = str(duration.days) + ' dia'
        else:
            ago = str(duration.days) + ' dias'
        snippet.ago = ago
    return snippets


class LanguageSnippetView(View):
    """Snipped Detail view"""

    def get(self, request, slug):
        snippets = Snippet.objects.filter(language__slug=slug, public=True)
        snippets = addAgoSnippets(snippets)
        return render(request, 'index.html', {'today': datetime.datetime.now(), 'snippets': snippets})


class UserSnippetView(View):
    """User Snippet view"""

    def get(self, request, username):
        if not request.user.is_authenticated or (request.user.is_authenticated and request.user.username != username):
            snippets = Snippet.objects.filter(
                user__username=username, public=True)
        elif request.user.username == username:
            snippets = Snippet.objects.filter(user=request.user)
        snippets = addAgoSnippets(snippets)
        return render(request, 'snippets/user_snippets.html', {'snippets': snippets, 'username': username})

    def post(self, request, username):
        '''Post request for delete snippet'''
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        Snippet.objects.get(pk=request.POST['snippet_id']).delete()
        return redirect(reverse('user_snippets', kwargs={'username': username}))


class UserSnippedDetailView(View):
    """Snipped Detail view"""

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        lexer = get_lexer_by_name(snippet.language.name.lower(), stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="source")
        snippet.snippet = highlight(snippet.snippet, lexer, formatter)
        return render(request, 'snippets/snippet.html', {'snippet': snippet, 'show_code': True, 'hide_show': True})


class SnippedDetailView(View):
    """Snipped Detail view"""

    def get(self, request):
        snippets = Snippet.objects.filter(public=True)
        snippets = addAgoSnippets(snippets)
        return render(request, 'index.html', {'today': datetime.datetime.now(), 'snippets': snippets})


class CreateSnippedView(LoginRequiredMixin, View):
    """Create Snipped view"""

    languages = Language.objects.all()

    def get(self, request):
        return render(request, 'snippets/snippet_add.html', {'languages': self.languages})

    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        if not data['name'].rstrip() or not data['snippet'].rstrip():
            return render(request, 'snippets/snippet_add.html', {
                'languages': self.languages,
                'form': {
                    'error': {
                        'msg': 'Faltan campos obligatorios',
                        'name': request.POST['name'],
                        'description': request.POST['description'],
                        'snippet': request.POST['snippet'],
                        'language_id': request.POST['language_id'],
                        'public': request.POST['public']
                    }
                }
            })
        else:
            public = data.pop('public')
            data['public'] = public == 'public'
            data['user_id'] = request.user.id
            data['profile_id'] = request.user.profile.id
            Snippet.objects.create(**data)
            return redirect(settings.LOGIN_REDIRECT_URL)


class SnippetUpdateView(LoginRequiredMixin, View):
    """Snipped Update view"""

    languages = Language.objects.all()

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        return render(request, 'snippets/snippet_edit.html', {'snippet': snippet, 'languages': self.languages})

    def post(self, request, pk):
        snippet = Snippet.objects.filter(pk=pk)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        if not data['name'].rstrip() or not data['snippet'].rstrip():
            return render(request, 'snippets/snippet_edit.html', {
                'snippet': snippet[0],
                'languages': self.languages,
                'form': {
                    'error': {
                        'msg': 'Faltan campos obligatorios'
                    }
                }
            })
        else:
            public = data.pop('public')
            data['public'] = public == 'public'
            snippet.update(**data)
            return redirect(reverse('user_snippets', kwargs={'username': snippet[0].user.username}))

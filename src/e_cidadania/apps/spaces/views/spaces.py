# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadanía Coop.
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

import datetime
import itertools

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.template import RequestContext
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db import connection
from django.core.mail import send_mail

from e_cidadania.apps.spaces.models.spaces import Space, Entity, Intent
from e_cidadania.apps.spaces.models.documents import Document
from e_cidadania.apps.spaces.models.events import Event
from e_cidadania.apps.news.models import Post
from e_cidadania.apps.spaces.forms import SpaceForm, EntityFormSet
from e_cidadania.apps.proposals.models import Proposal
from e_cidadania.apps.staticpages.models import StaticPage
from e_cidadania.apps.debate.models import Debate
from django.conf import settings


class SpaceFeed(Feed):

    """
    Returns a space RSS feed with the content of various applciations. In the
    future this function must detect applications and returns their own feeds.
    """

    def get_object(self, request, space_name):
        current_space = get_object_or_404(Space, url=space_name)
        return current_space

    def title(self, obj):
        return _("%s feed") % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _("All the recent activity in %s ") % obj.name

    def items(self, obj):
        results = itertools.chain(
            Post.objects.all().filter(space=obj).order_by('-pub_date')[:10],
            Proposal.objects.all().filter(space=obj).order_by('-pub_date')[:10],
            Event.objects.all().filter(space=obj).order_by('-pub_date')[:10],
        )

        return sorted(results, key=lambda x: x.pub_date, reverse=True)

#
# INTENT VIEWS
#

@login_required
def add_intent(request, space_name):
    """
    Returns a page where the logged in user can click on a "I want to
    participate" button, which after sends an email to the administrator of
    the space with a link to approve the user to use the space.

    :attributes:  space, intent, token
    :rtype: Multiple entity objects.
    :context: space_name, heading
    """
    import hashlib
    space = get_object_or_404(Space, url=space_name)
    try:
        intent = Intent.objects.get(user=request.user, space=space)
        heading = _("Access has been already authorized")
    except Intent.DoesNotExist:
        token = hashlib.md5("%s%s%s" % (request.user, space,
                                        datetime.datetime.now())).hexdigest()
        intent = Intent(user=request.user, space=space, token=token)
        intent.save()
        subject = _("New participation request")
        body = _("User %s wants to participate in space %s.\n \
                  Plese click on the link below to approve.\n %s"\
        % (request.user.username, space.name,
           intent.get_approve_url()))
        heading = _("Your request is being processed.")
        send_mail(subject=subject, message=body,
            from_email="noreply@ecidadania.org",
            recipient_list=[space.author.email])


    return render_to_response('space_intent.html',\
            {'space_name': space_name, 'heading': heading},\
        context_instance=RequestContext(request))

@staff_member_required
def validate_intent(request, space_name, token):
    """
    Adds the user to the space, validates the request to participate.
    :attributes: space, intent
    :rtype: Multiple entity objects.
    :context: space_name, heading
    """
    space = get_object_or_404(Space, url=space_name)
    try:
        intent = Intent.objects.get(token=token)
        intent.user.profile.spaces.add(space)
        intent.delete()
        heading = _("The user has been authorized to participate in space \"%s\"." % space.name)
    except Intent.DoesNotExist:
        heading = _("The requested intent does not exist!")

    return render_to_response('validate_intent.html',\
            {'space_name': space_name, 'heading': heading},\
        context_instance=RequestContext(request))


# SPACE VIEWS
#

# Please take in mind that the create_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
@permission_required('spaces.add_space')
def create_space(request):

    """
    Returns a SpaceForm form to fill with data to create a new space. There
    is an attached EntityFormset to save the entities related to the space. Only
    site administrators are allowed to create spaces.

    :attributes: - space_form: empty SpaceForm instance
                 - entity_forms: empty EntityFormSet
    :rtype: Space object, multiple entity objects.
    :context: form, entityformset
    """
    space_form = SpaceForm(request.POST or None, request.FILES or None)
    entity_forms = EntityFormSet(request.POST or None, request.FILES or None,
        queryset=Entity.objects.none())

    if request.user.is_staff:
        if request.method == 'POST':
            if space_form.is_valid() and entity_forms.is_valid():
                space_form_uncommited = space_form.save(commit=False)
                space_form_uncommited.author = request.user

                new_space = space_form_uncommited.save()
                space = get_object_or_404(Space, name=space_form_uncommited.name)

                ef_uncommited = entity_forms.save(commit=False)
                for ef in ef_uncommited:
                    ef.space = space
                    ef.save()
                    # We add the created spaces to the user allowed spaces

                request.user.profile.spaces.add(space)
                #messages.success(request, _('Space %s created successfully.') % space.name)
                return redirect('/spaces/' + space.url)

        return render_to_response('spaces/space_add.html',
                {'form': space_form,
                 'entityformset': entity_forms},
            context_instance=RequestContext(request))
    else:
        return render_to_response('not_allowed.html',
            context_instance=RequestContext(request))


class ViewSpaceIndex(DetailView):

    """
    Returns the index page for a space. The access to spaces is restricted and
    filtered in the get_object method. This view gathers information from all
    the configured modules in the space.

    :attributes: space_object, place
    :rtype: Object
    :context: get_place, entities, documents, proposals, publication
    """
    context_object_name = 'get_place'
    template_name = 'spaces/space_index.html'

    def get_object(self):
        space_name = self.kwargs['space_name']
        space_object = get_object_or_404(Space, url = space_name)

        if space_object.public == True or self.request.user.is_staff:
            if self.request.user.is_anonymous():
                messages.info(self.request, _("Hello anonymous user. Remember \
                                              that this space is public to view, but \
                                              you must <a href=\"/accounts/register\">register</a> \
                                              or <a href=\"/accounts/login\">login</a> to participate."))
            return space_object

        if self.request.user.is_anonymous():
            messages.info(self.request, _("You're an anonymous user. \
                          You must <a href=\"/accounts/register\">register</a> \
                          or <a href=\"/accounts/login\">login</a> to access here."))
            self.template_name = 'not_allowed.html'
            return space_object

        for i in self.request.user.profile.spaces.all():
            if i.url == space_name:
                return space_object

        messages.warning(self.request, _("You're not registered to this space."))
        self.template_name = 'not_allowed.html'
        return space_object

    # Get extra context data
    def get_context_data(self, **kwargs):
        context = super(ViewSpaceIndex, self).get_context_data(**kwargs)
        place = get_object_or_404(Space, url=self.kwargs['space_name'])
        context['entities'] = Entity.objects.filter(space=place.id)
        context['documents'] = Document.objects.filter(space=place.id)
        context['proposals'] = Proposal.objects.filter(space=place.id).order_by('-pub_date')
        context['publication'] = Post.objects.filter(space=place.id).order_by('-pub_date')[:10]
        context['page'] = StaticPage.objects.filter(show_footer=True).order_by('-order')
        context['messages'] = messages.get_messages(self.request)
        context['debates'] = Debate.objects.filter(space=place.id).order_by('-date')
        context['event'] = Event.objects.filter(space=place.id).order_by('-event_date')
        return context


# Please take in mind that the edit_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
@permission_required('spaces.edit_space')
def edit_space(request, space_name):

    """
    Returns a form filled with the current space data to edit. Access to
    this view is restricted only to site and space administrators. The filter
    for space administrators is given by the edit_space permission and their
    belonging to that space.

    :attributes: - place: current space intance.
                 - form: SpaceForm instance.
                 - form_uncommited: form instance before commiting to the DB,
                   so we can modify the data.
    :param space_name: Space URL
    :rtype: HTML Form
    :context: form, get_place
    """
    place = get_object_or_404(Space, url=space_name)

    form = SpaceForm(request.POST or None, request.FILES or None, instance=place)
    entity_forms = EntityFormSet(request.POST or None, request.FILES or None,
        queryset=Entity.objects.all().filter(space=place))

    if request.method == 'POST':
        if form.is_valid() and entity_forms.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.author = request.user

            new_space = form_uncommited.save()
            space = form_uncommited.url

            ef_uncommited = entity_forms.save(commit=False)
            for ef in ef_uncommited:
                ef.space = space
                ef.save()

            #messages.success(request, _('Space edited successfully'))
            return redirect('/spaces/' + space)

    for i in request.user.profile.spaces.all():
        if i.url == space_name or request.user.is_staff:
            return render_to_response('spaces/space_edit.html',
                    {'form': form, 'get_place': place,
                     'entityformset': entity_forms},
                context_instance=RequestContext(request))

    return render_to_response('not_allowed.html', context_instance=RequestContext(request))


class DeleteSpace(DeleteView):

    """
    Returns a confirmation page before deleting the space object completely.
    This does not delete the space related content. Only the site administrators
    can delete a space.

    :rtype: Confirmation
    """
    context_object_name = 'get_place'
    success_url = '/'

    @method_decorator(permission_required('spaces.delete_space'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSpace, self).dispatch(*args, **kwargs)

    def get_object(self):
        return get_object_or_404(Space, url = self.kwargs['space_name'])


class GoToSpace(RedirectView):

    """
    Sends the user to the selected space. This view only accepts GET petitions.
    GoToSpace is a django generic :class:`RedirectView`.

    :Attributes: **self.place** - Selected space object
    :rtype: Redirect
    """
    def get_redirect_url(self, **kwargs):
        self.place = get_object_or_404(Space, name = self.request.GET['spaces'])
        return '/spaces/%s' % self.place.url


class ListSpaces(ListView):

    """
    Return a list of spaces in the system (except private ones) using a generic view.
    The users associated to a private spaces will see it, but not the other private
    spaces. ListSpaces is a django generic :class:`ListView`.

    :rtype: Object list
    :contexts: object_list
    """
    paginate_by = 10

    def get_queryset(self):
        public_spaces = Space.objects.all().filter(public=True)

        if not self.request.user.is_anonymous():
            user_spaces = self.request.user.profile.spaces.all()
            return public_spaces | user_spaces

        return public_space


#
# NEWS RELATED
#

class ListPosts(ListView):

    """
    Returns a list with all the posts attached to that space. It's similar to
    an archive, but without classification or filtering.

    :rtype: Object list
    :context: post_list
    """
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'news/news_list.html'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_name'])

        if settings.DEBUG:
            messages.set_level(self.request, messages.DEBUG)
            messages.debug(self.request, "Succesful query.")

        return Post.objects.all().filter(space=place).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListPosts, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        context['messages'] = messages.get_messages(self.request)
        return context
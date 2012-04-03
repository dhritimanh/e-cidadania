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

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from e_cidadania.apps.spaces.models.spaces import Space
from e_cidadania.apps.spaces.models.events import Event
from e_cidadania.apps.spaces.forms import EventForm

class AddEvent(FormView):

    """
    Returns an empty MeetingForm to create a new Meeting. Space and author fields
    are automatically filled with the request data.

    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = EventForm
    template_name = 'spaces/event_add.html'

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        return '/spaces/' + self.space.url

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        form_uncommited = form.save(commit=False)
        form_uncommited.event_author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        return super(AddEvent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context


class ViewEvent(DetailView):

    """
    View the content of a event.

    :rtype: Object
    :context: event, get_place
    """
    context_object_name = 'event'
    template_name = 'spaces/event_detail.html'

    def get_object(self):
        space_name = self.kwargs['space_name']

        if self.request.user.is_anonymous():
            self.template_name = 'not_allowed.html'
            return get_object_or_404(Space, url = space_name)

        return get_object_or_404(Event, pk = self.kwargs['event_id'])

    def get_context_data(self, **kwargs):
        context = super(ViewEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context


class EditEvent(UpdateView):

    """
    Returns a MeetingForm filled with the current Meeting data to be edited.

    :rtype: HTML Form
    :context: event, get_place
    """
    model = Event
    template_name = 'spaces/event_edit.html'

    def get_object(self):
        cur_event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return cur_event

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        return '/spaces/' + self.space.name

    def get_context_data(self, **kwargs):
        context = super(EditEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context

    @method_decorator(permission_required('spaces.edit_event'))
    def dispatch(self, *args, **kwargs):
        return super(EditEvent, self).dispatch(*args, **kwargs)


class DeleteEvent(DeleteView):

    """
    Returns a confirmation page before deleting the Meeting object.

    :rtype: Confirmation
    :context: get_place
    """

    def get_object(self):
        return get_object_or_404(Event, pk = self.kwargs['event_id'])

    def get_success_url(self):
        current_space = self.kwargs['space_name']
        return '/spaces/{0}'.format(current_space)

    def get_context_data(self, **kwargs):
        context = super(DeleteEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context


class ListEvents(ListView):

    """
    List all the events attached to a space.

    :rtype: Object list
    :context: event_list, get_place
    """
    paginate_by = 25
    context_object_name = 'event_list'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_name'])
        objects = Event.objects.all().filter(space=place.id).order_by\
            ('event_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListEvents, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context
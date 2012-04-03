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

from django.conf.urls.defaults import *

from e_cidadania.apps.spaces.views.events import ListEvents, DeleteEvent, ViewEvent, \
                                          AddEvent, EditEvent

urlpatterns = patterns('e_cidadania.apps.spaces.views.events',

    url(r'^add/$', AddEvent.as_view(), name='add-event'),

    url(r'^(?P<event_id>\d+)/edit/$', EditEvent.as_view(), name='edit-event'),

    url(r'^(?P<event_id>\d+)/delete/$', DeleteEvent.as_view(), name='delete-event'),

    url(r'^(?P<event_id>\d+)/$', ViewEvent.as_view(), name='view-event'),

    url(r'^event/$', ListEvents.as_view(), name='list-events'),

)
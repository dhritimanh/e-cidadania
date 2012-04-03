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

from e_cidadania.apps.spaces.views.spaces import GoToSpace, ViewSpaceIndex, \
                                                 ListSpaces, DeleteSpace, \
                                                 SpaceFeed, ListPosts

urlpatterns = patterns('',
    # News
    (r'^(?P<space_name>\w+)/news/', include('e_cidadania.apps.news.urls')),

    # Proposals
    (r'^(?P<space_name>\w+)/proposal/', include('e_cidadania.apps.proposals.urls')),

    # Events
    (r'^(?P<space_name>\w+)/event/', include('e_cidadania.apps.spaces.urls.events')),

    # Documents
    (r'^(?P<space_name>\w+)/docs/', include('e_cidadania.apps.spaces.urls.documents')),

    # Calendar
    (r'^(?P<space_name>\w+)/calendar/', include('e_cidadania.apps.cal.urls')),

    # Debates
    (r'^(?P<space_name>\w+)/debate/', include('e_cidadania.apps.debate.urls')),

)

# Spaces URLs
urlpatterns += patterns('e_cidadania.apps.spaces.views.spaces',

    # RSS Feed
    url(r'^(?P<space_name>\w+)/rss/$', SpaceFeed(), name='space-feed'),

    # Space actions
    url(r'^(?P<space_name>\w+)/edit/$', 'edit_space', name='edit-space'),

    url(r'^(?P<space_name>\w+)/delete/$', DeleteSpace.as_view(), name='delete-space'),

    url(r'^(?P<space_name>\w+)/news/', ListPosts.as_view(), name='list-space-news'),

    url(r'^add/$', 'create_space', name='create-space'),

    url(r'^$', ListSpaces.as_view(), name='list-spaces'),

    url(r'^go/', GoToSpace.as_view(), name='goto-space'),

    url(r'^(?P<space_name>\w+)/$', ViewSpaceIndex.as_view(), name='space-index'),

    # Intent URLs
    url(r'^(?P<space_name>\w+)/intent/$', 'add_intent', name='add-intent'),

    url(r'^(?P<space_name>\w+)/intent/approve/(?P<token>\w+)/$', 'validate_intent', name='validate-intent'),

)
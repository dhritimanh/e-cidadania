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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from spaces import Space
from e_cidadania.apps.spaces.fields.file_validation import ContentTypeRestrictedFileField

class Event(models.Model):

    """
    Meeting data model. Every space (process) has N meetings. This will
    keep record of the assistants, meeting name, etc.
    """
    title = models.CharField(_('Event name'), max_length=100)
    space = models.ForeignKey(Space, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name=_('Users'))
    pub_date = models.DateTimeField(auto_now_add=True)
    event_author = models.ForeignKey(User, verbose_name=_('Created by'),
        blank=True, null=True,
        related_name='meeting_author')
    event_date = models.DateField(verbose_name=_('Event date'))
    description = models.TextField(_('Description'), blank=True, null=True)
    location = models.TextField(_('Location'), blank=True, null=True)

    class Meta:
        app_label = _('Event')
        ordering = ['event_date']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        get_latest_by = 'event_date'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view-event', (), {
            'space_name': self.space.url,
            'event_id': str(self.id)})
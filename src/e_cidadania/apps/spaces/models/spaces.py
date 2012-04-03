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

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from e_cidadania.apps.spaces.fields.image import StdImageField

class Space(models.Model):

    """     
    Spaces model. This model stores a "space" or "place" also known as a
    participative process in reality. Every place has a minimum set of
    settings for customization.
    """
    name = models.CharField(_('Name'), max_length=250, unique=True,
                            help_text=_('Max: 250 characters'))
    url = models.CharField(_('URL'), max_length=100, unique=True,
                            validators=[RegexValidator(
                                        regex='^[a-z0-9_]+$',
                                        message='Invalid characters in the space URL.'
                                       )],
                            help_text=_('Valid characters are lowercase, digits and \
                                         underscore. This will be the accesible URL'))
    description = models.TextField(_('Description'),
                                    default=_('Write here your description.'))
    date = models.DateTimeField(_('Date of creation'), auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True,
                                verbose_name=_('Space creator'))

    logo = StdImageField(upload_to='spaces/logos', size=(100, 75, False), 
                         help_text = _('Valid extensions are jpg, jpeg, png and gif'))
    banner = StdImageField(upload_to='spaces/banners', size=(500, 75, False),
                           help_text = _('Valid extensions are jpg, jpeg, png and gif'))
    public = models.BooleanField(_('Public space'))
    #theme = models.CharField(_('Theme'), m)
    
    # Modules
    mod_debate = models.BooleanField(_('Debate'))
    mod_proposals = models.BooleanField(_('Proposals'))
    mod_news = models.BooleanField(_('News'))
    mod_cal = models.BooleanField(_('Calendar'))
    mod_docs = models.BooleanField(_('Documents'))

    class Meta:
        app_label = _('Space')
        ordering = ['name']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        get_latest_by = 'date'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('space-index', (), {
           'space_name': self.url})


class Entity(models.Model):

    """
    This model stores the name of the entities responsible for the creation
    of the space or supporting it.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    website = models.CharField(_('Website'), max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='spaces/logos', verbose_name=_('Logo'),
                             blank = True, null = True)
    space = models.ForeignKey(Space, blank=True, null=True)
    
    class Meta:
        app_label = _('Entity')
        ordering = ['name']
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __unicode__(self):
        return self.name


class Intent(models.Model):
    """
    Data model for user intents to access a space. This models is for the action
    "I want to participate" in private spaces.
    """
    user = models.ForeignKey(User)
    space = models.ForeignKey(Space)
    token = models.CharField(max_length=32)
    requested_on = models.DateTimeField(auto_now_add=True)

    def get_approve_url(self):
        from django.contrib.sites.models import Site
        site = Site.objects.all()[0]
        return "http://%s%sintent/approve/%s" % (site.domain, self.space.get_absolute_url(), self.token)

    class Meta:
        app_label = _('Entity')
        verbose_name = _('Intent')
        verbose_name_plural = _('Intents')
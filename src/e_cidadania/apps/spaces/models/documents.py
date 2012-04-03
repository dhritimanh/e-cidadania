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

ALLOWED_CONTENT_TYPES = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.openofficeorg.extension',
    ]

class Document(models.Model):

    """
    This models stores documents for the space, like a document repository,
    There is no restriction in what a user can upload to the space
    """
    title = models.CharField(_('Document title'), max_length=100)
    space = models.ForeignKey(Space, blank=True, null=True)
    docfile = ContentTypeRestrictedFileField(_('File'),
        upload_to='spaces/documents/%Y/%m/%d',
        content_types=ALLOWED_CONTENT_TYPES,
        max_upload_size=26214400
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
        null=True)

    def get_file_ext(self):
        filename = self.docfile.name
        extension = filename.split('.')
        return extension[1].upper()

    def get_file_size(self):
        if self.docfile.size < 1023:
            return str(self.docfile.size) + " Bytes"
        elif self.docfile.size >= 1024 and self.docfile.size <= 1048575:
            return str(round(self.docfile.size / 1024.0, 2)) + " KB"
        elif self.docfile.size >= 1048576:
            return str(round(self.docfile.size / 1024000.0, 2)) + " MB"

    class Meta:
        app_label = _('Document')
        ordering = ['pub_date']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = 'pub_date'

    # There is no 'view-document' view, so I'll leave the get_absolute_url
    # method without permalink. Remember that the document files are accesed
    # through the url() method in templates.
    def get_absolute_url(self):
        return '/spaces/%s/docs/%s' % (self.space.url, self.id)
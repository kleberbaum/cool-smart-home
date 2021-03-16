import graphene
from django.core import validators
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.search import index

from bifrost.helpers import register_paginated_query_field
from bifrost.models import (
    GraphQLCollection,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLStreamfield,
    GraphQLString,
    GraphqlDatetime,
)
from esite.utils.edit_handlers import ReadOnlyPanel
from esite.utils.models import TimeStampMixin
from esite.colorfield.fields import ColorField

from .blocks import AttendeeBlock, TagBlock
from .validators import validate_audio_file


class Sensor(models.Model):
    title = models.CharField(null=False, blank=False, max_length=32)
    topic = models.CharField(null=False, blank=False, max_length=32, default="server/mqtt-test/COMMAND")
    temperature = models.FloatField(null=True, blank=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)], default=0.5)
    humidity = models.FloatField(null=True, blank=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)], default=0.5)
    dew_point = models.FloatField(null=True, blank=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)], default=0.5)

    graphql_fields = [
        GraphQLString("title"),
        GraphQLString("topic"),
        GraphQLString("temperature"),
        GraphQLString("humidity"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("topic"),
        index.SearchField("temperature"),
        index.SearchField("humidity"),
        index.SearchField("dew_point"),
    ]

    panels = [
        FieldPanel("title"),
        FieldPanel("topic"),
        FieldPanel("temperature"),
        FieldPanel("humidity"),
        FieldPanel("dew_point"),
    ]

    def __str__(self):
        return f"{self.title}"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Florian Kleber

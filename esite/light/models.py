import graphene
import paho.mqtt.client as mqtt
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


class Light(models.Model):
    title = models.CharField(null=False, blank=False, max_length=32)
    topic = models.CharField(null=False, blank=False, max_length=64, default="test_bulb/light/test_bulb/command")
    hcolor = ColorField(null=False, blank=False, help_text="Select color that fitd your mood.")
    brightness = models.FloatField(null=True, blank=True, validators=[validators.MaxValueValidator(255), validators.MinValueValidator(0)], default=100)
    color_temperature = models.IntegerField(null=True, blank=True, validators=[validators.MaxValueValidator(6500), validators.MinValueValidator(2700)], default=2700)
    color_from_temperature = models.BooleanField(null=False, blank=False)
    effect = models.CharField(null=True, blank=True, choices=[("rainbow", "Rainbow"), ("blink", "Blink")], max_length=32)

    graphql_fields = [
        GraphQLString("title"),
        GraphQLString("topic"),
        GraphQLString("hcolor"),
        GraphQLString("brightness"),
        GraphQLString("color_temperature"),
        GraphQLString("color_from_temperature"),
        GraphQLString("effect"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("topic"),
        index.SearchField("hcolor"),
        index.SearchField("brightness"),
        index.SearchField("color_temperature"),
        index.SearchField("color_from_temperature"),
        index.SearchField("effect"),
    ]

    panels = [
        FieldPanel("title"),
        FieldPanel("topic"),
        FieldPanel("hcolor"),
        FieldPanel("brightness"),
        FieldPanel("color_temperature"),
        FieldPanel("color_from_temperature"),
        FieldPanel("effect"),
    ]

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        client = mqtt.Client()
        
        hexc= self.hcolor.lstrip('#')
        rgbc = tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))
        
        client.connect("10.1.0.1", 1883, 60)
        client.publish(self.topic, '{"state":"ON",'+f'"brightness":{self.brightness},' + '"color":{'+f'"r":{rgbc[0]},"g":{rgbc[1]},"b":{rgbc[2]}'+'}}', qos=1)
        # "white_value":255,"color_temp":370

        super(Light, self).save(*args, **kwargs)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Florian Kleber

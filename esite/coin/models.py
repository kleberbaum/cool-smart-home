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

config_default = """[
    {"symbol": ""},
    {"name": " Name: "},
    {"price_btc": " Price in BTC: "},
    {"price": " Price: "},
    {"percent_change_24h": " - 24 Hour Percent Change: "},
    {"market_cap": " Market Cap: "},
    {"volume_24h": " 24 Hour Volume: "},
    {"url_shares": " URL Shares: "},
    {"reddit_posts": " Reddit Posts: "},
    {"tweets": " Tweets: "},
    {"news": " News: "},
]"""

class Sensor(models.Model):
    coin = models.CharField(null=False, blank=False, max_length=255)
    config = models.TextField(blank=True, default=config_default)

    graphql_fields = [
        GraphQLString("coin"),
        GraphQLString("config"),
    ]

    search_fields = [
        index.SearchField("coin"),
        index.SearchField("config"),
    ]

    panels = [
        FieldPanel("coin"),
        FieldPanel("config"),
    ]

    def __str__(self):
        return f"{self.coin}"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Florian Kleber

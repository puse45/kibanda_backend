import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.manager import BaseManager


class AccessUrl(models.Model):
    name = models.CharField(max_length=50, default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.DurationField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    url = models.URLField()
    url_type = models.CharField(
        max_length=10,
        choices=(
            ("SHORT", "SHORTENED URL"),
            ("FRONTEND", "FRONTEND URL"),
            ("MEDIA", "MEDIA URL"),
            ("STREAM", "STREAM URL"),
        ),
    )
    description = models.TextField(default="")
    active = models.BooleanField(default=False)

    @property
    def asset_type(self):
        return self.content_type.name

    class Meta:
        unique_together = ("content_type", "object_id", "url_type")

    def __str__(self):
        return str(self.url)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    is_archived = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, null=True, blank=True)
    access_urls = GenericRelation(AccessUrl)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ("-updated_at", "-created_at")

    @property
    def type_name(self):
        return f"{self._meta.app_label}.{self._meta.model_name}"

    @property
    def item_content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def item_content_type_id(self):
        return self.item_content_type.id

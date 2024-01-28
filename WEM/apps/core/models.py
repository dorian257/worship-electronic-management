from crequest.middleware import CrequestMiddleware
from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="%(app_label)s_%(class)s_updated",
        related_query_name="%(app_label)s_%(class)s_updates",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="%(app_label)s_%(class)s_created",
        related_query_name="%(app_label)s_%(class)s_creations",
        null=True,
        blank=True,
    )

    # Default Manager is Used
    objects = models.Manager()

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["created_at", "updated_at"]

    def save(self, request=None, *args, **kwargs):
        created = self.pk is None
        if not request:
            request = CrequestMiddleware.get_request()

        if created:
            self.created_by = request.user

        self.updated_by = request.user

        return super().save(*args, **kwargs)

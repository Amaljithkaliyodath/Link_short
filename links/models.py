from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)
    code = models.SlugField(max_length=16, unique=True, db_index=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # 1%: expiring links
    title = models.CharField(max_length=255, blank=True)      # 1%: OpenGraph title
    image_url = models.URLField(max_length=2048, blank=True)  # 1%: OpenGraph image

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} -> {self.original_url}"

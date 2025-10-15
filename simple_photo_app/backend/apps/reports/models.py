from django.db import models
from django.conf import settings


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #"カスタムユーザー紐付け"
    image = models.ImageField(upload_to='photos/')
    checksum = models.CharField(max_length=64, db_index=True, blank=True, null=True)  # 追加
    file_size = models.PositiveBigIntegerField(blank=True, null=True)                 # 任意
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'checksum'], name='unique_user_checksum')
        ]

    def __str__(self):
        return f"Photo {self.id} - {self.uploaded_at}"
    


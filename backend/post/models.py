from django.db import models
import uuid
from account.models import User
from django.utils.timesince import timesince
# Create your models here.
class Like(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='like',on_delete=models.CASCADE)

class Comment(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    body=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='comment',on_delete=models.CASCADE)
    def created_at_formatted(self):
        return timesince(self.created_at)

class PostAttachments(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    image=models.ImageField(upload_to='post_attachments')
    created_by=models.ForeignKey(User,related_name='post_attachments',on_delete=models.CASCADE)


class Post(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    body=models.TextField(blank=True,null=True)
    attachments=models.ManyToManyField(PostAttachments,blank=True)
    like=models.ManyToManyField(Like,blank=True)
    like_count=models.IntegerField(default=0)
    comment=models.ManyToManyField(Comment,blank=True)
    comment_count=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='post',on_delete=models.CASCADE)
    class Meta:
        ordering=('-created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)
# Create your models here.

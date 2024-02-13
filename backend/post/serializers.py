from rest_framework import serializers
from .models import Post,Comment
from account.serializers import UserSerailzier
class PostSerailzier(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    class Meta:
        model=Post
        fields=('id','body','created_at_formatted','created_by','like_count','comment_count')
    
class CommentSerailizer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    class Meta:
        model=Comment
        fields=('id','body','created_at_formatted','created_by')

class PostDetailSerializer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    comment=CommentSerailizer(read_only=True,many=True)
    class Meta:
        model=Post
        fields=('id','body','created_at_formatted','created_by','like_count','comment','comment_count')
        
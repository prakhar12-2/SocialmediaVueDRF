from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from .models import Post,Like,Comment
from .serializers import PostSerailzier,PostDetailSerializer,CommentSerailizer
from .forms import PostForm
from account.models import User,FriendshipRequest
from account.serializers import UserSerailzier
@api_view(['GET'])
def PostView(request):
    #posts=Post.objects.all()
    post_ids=[request.user.id]
    for friend in request.user.friends.all():
        post_ids.append(friend.id)
    posts=Post.objects.filter(created_by_id__in=list(post_ids))
    serializers=PostSerailzier(posts,many=True)
    return JsonResponse(serializers.data,safe=False)

@api_view(['GET'])
def post_list_profile(request,id):
    posts=Post.objects.filter(created_by_id=id)
    user=User.objects.get(pk=id)
    pserializers=PostSerailzier(posts,many=True)
    userializers=UserSerailzier(user)
    return JsonResponse({'posts':pserializers.data,
                         'user':userializers.data},safe=False)

@api_view(['POST'])
def post_create(request):
    form=PostForm(request.data)
    if form.is_valid():
        post=form.save(commit=False)
        post.created_by=request.user
        post.save()
        serializers=PostSerailzier(post)
        return JsonResponse(serializers.data,safe=True)
    else:
       return JsonResponse({'error':'enter something else'})

@api_view(['POST'])
def post_like(request,pk):
    post=Post.objects.get(pk=pk)
    #post.like_count=1
    #post.save()
    #print(post.like_count)
    #print(post.like.filter(created_by=request.user))
   
    if not post.like.filter(created_by=request.user):
        like=Like.objects.create(created_by=request.user)
        post=Post.objects.get(pk=pk)
        post.like_count=post.like_count+1
        post.like.add(like)
        post.save()
        return JsonResponse({'message':'Liked the post'})
    else:
        return JsonResponse({'message':'Liked already'})

@api_view(['GET'])
def post_detail(request,pk):
    post=Post.objects.get(pk=pk)
    return JsonResponse({
        'post':PostDetailSerializer(post).data
    })

@api_view(['POST'])
def comment_create(request,pk):
    post=Post.objects.get(pk=pk)
    comment=Comment.objects.create(body=request.data.get('body'),created_by=request.user)
    post.comment.add(comment)
    post.comment_count=post.comment_count+1
    post.save()
    comment.save()
    serializer=CommentSerailizer(comment)
    return JsonResponse(serializer.data,safe=True)    
    #print(request.data)
    #print(post.id)
    #return JsonResponse({'message':'new comment added'})
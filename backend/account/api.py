from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from .forms import SignupForm
from .models import User,FriendshipRequest
from .serializers import UserSerailzier,FriendshipRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET"])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name':request.user.name,
        'email':request.user.email
    })

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()
    else:
        message = form.errors.as_json()
        #message='error'
    
    print(message)

    return JsonResponse({'message': message}, safe=False)

@api_view(['POST'])
def friendRequest(request,pk):
    user=User.objects.get(pk=pk)
    friendRequestmod=FriendshipRequest.objects.create(created_by=request.user,created_for=user,status='Sent')
    check1=FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    check2=FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    if check1 or check2:
        return JsonResponse({'message':'Request has been sent already'})
    else:
       return JsonResponse({'message':'Request Sent successfully'})
    z
@api_view(['GET'])
def friends(request,pk):
    user=User.objects.get(pk=pk)
    requests=[]

    if user==request.user:
        requests=FriendshipRequest.objects.filter(created_for=request.user,status=FriendshipRequest.SENT)
        requests=FriendshipRequestSerializer(requests,many=True)
        requests=requests.data

    friends=user.friends.all()
    return JsonResponse({
        'user':UserSerailzier(user).data,
        'friends':UserSerailzier(friends, many=True).data,
        'requests':requests,
    },safe=True)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def handle_request(request,pk,status):
    user=User.objects.get(pk=pk)#who sent the request
    friend_Request=FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friend_Request.status=status
    friend_Request.save()
    user.friends.add(request.user)
    user.friends_count=user.friends_count+1
    user.save()
    request_user=request.user
    request_user.friends_count=request_user.friends_count+1
    request_user.save()
    return JsonResponse({'Job':'done'})
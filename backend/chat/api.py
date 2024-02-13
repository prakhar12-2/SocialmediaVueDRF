from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .models import Conversation,ConversationMessage
from .serializers import ConversationDetailSerializer,ConversationMessageSerializer,ConversationSerializer
from django.http import JsonResponse

api_view(['GET'])
def conversation_list(request):
    print(request.user)
    conversations=Conversation.objects.filter(users=request.user)
    print(conversations)
    return JsonResponse({'hdb':'syghsud'})
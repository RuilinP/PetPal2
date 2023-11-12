from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Shelter, Application
from .serializers import CommentSerializer, ReplySerializer



class ApplicationCommentDetailView(APIView):
    # needs additional checks: user submits application and shelter receives application
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id, comment_id):
        get_object_or_404(Application, pk=application_id)
        content_type = ContentType.objects.get_for_model(Application)
        comment = get_object_or_404(Comment, content_type=content_type, object_id=application_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, application_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Application, pk=application_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Application)
            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, object_id=application_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ShelterCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shelter_id, comment_id):
        get_object_or_404(Shelter, pk=shelter_id)
        content_type = ContentType.objects.get_for_model(Shelter)
        comment = get_object_or_404(Comment, content_type=content_type, object_id=shelter_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, shelter_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Shelter, pk=shelter_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Shelter)
            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, object_id=shelter_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShelterCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shelter_id):
        get_object_or_404(Shelter, pk=shelter_id)
        content_type = ContentType.objects.get_for_model(Shelter)
        comments = Comment.objects.filter(object_id=shelter_id, content_type=content_type)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, shelter_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Shelter, pk=shelter_id)
            content_type = ContentType.objects.get_for_model(Shelter)
            serializer.save(content_object=content_object, object_id=shelter_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ShelterDashboardCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shelter_id = self.kwargs['shelter_id']
        content_type = ContentType.objects.get_for_model(Shelter)
        return Comment.objects.filter(object_id=shelter_id, content_type=content_type)


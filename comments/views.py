from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from application.models import Application
from accounts.models import Shelter, Seeker, CustomUser
from .serializers import CommentSerializer, ReplySerializer


class ApplicationCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id, comment_id):
        # check that the user and application exist
        author = get_object_or_404(CustomUser, pk=request.user.id)
        application = get_object_or_404(Application, pk=application_id)

        # check if author is a seeker/shelter relevant to the application
        if application.seeker.id != author.id and application.shelter.id != author.id :
            # user not relevant to the application, unauthorize
            Response({"detail": "You do not have permission to access this application."},
                    status=status.HTTP_403_FORBIDDEN)
        
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, application_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Application, pk=application_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Application)

            author = get_object_or_404(CustomUser, pk=request.user.id)
            # check if author is a seeker/shelter relevant to the application
            if content_object.seeker.id != author.id and content_object.shelter.id != author.id :
                # user not relevant to the application, unauthorize
                Response({"detail": "You do not have permission to access this application."},
                        status=status.HTTP_403_FORBIDDEN)
            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, 
                            author = author,
                            object_id=application_id, content_type=content_type)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ApplicationCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        # check that the user and application exist
        author = get_object_or_404(CustomUser, pk=request.user.id)
        application = get_object_or_404(Application, pk=application_id)

        if application.seeker.id != author.id and application.shelter.id != author.id :
            # user not relevant to the application, unauthorize
            Response({"detail": "You do not have permission to access this application."},
                    status=status.HTTP_403_FORBIDDEN)
            
        # filter for comments associated with the application
        content_type = ContentType.objects.get_for_model(Application)
        comments = Comment.objects.filter(content_type=content_type, object_id=application_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, application_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Application, pk=application_id)
            content_type = ContentType.objects.get_for_model(Application)

            # check if author is a seeker/shelter relevant to the application
            author = get_object_or_404(CustomUser, pk=request.user.id)
            if content_object.seeker.id != author.id and content_object.shelter.id != author.id :
                # user not relevant to the application, unauthorize
                Response({"detail": "You do not have permission to access this application."},
                        status=status.HTTP_403_FORBIDDEN)

                
            serializer.save(content_object=content_object, 
                            author = author,
                            object_id=application_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ShelterCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shelter_id, comment_id):
        # check the user and shelter exist
        get_object_or_404(Shelter, pk=shelter_id)
        get_object_or_404(CustomUser, pk=request.user.id)

        comment = get_object_or_404(Comment, pk = comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, shelter_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Shelter, pk=shelter_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Shelter)

            # check that the comment belongs to the shelter
            if comment.object_id != shelter_id:
                return Response({"detail": "You do not have permission to access this application."},
                        status=status.HTTP_403_FORBIDDEN)
            
            author = get_object_or_404(CustomUser, pk=request.user.id)            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, 
                            author = author,
                            object_id=shelter_id, content_type=content_type)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShelterCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shelter_id):
        # check the user and shelter exist
        get_object_or_404(Shelter, pk=shelter_id)
        get_object_or_404(CustomUser, pk=request.user.id)
        
        # filter for comments made to the shelter
        content_type = ContentType.objects.get_for_model(Shelter)
        comments = Comment.objects.filter(object_id=shelter_id, content_type=content_type)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, shelter_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_type = ContentType.objects.get_for_model(Shelter)
            serializer.save(content_object=get_object_or_404(Shelter, pk=shelter_id), 
                            object_id=shelter_id, content_type=content_type, 
                            author = get_object_or_404(CustomUser, pk=request.user.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ShelterDashboardCommentsView(generics.ListAPIView): # for shelter comments only, if shelter wants to view application comments: in application --> reply --> application comment details page
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         shelter_id = self.kwargs['shelter_id']
#         content_type = ContentType.objects.get_for_model(Shelter)
#         return Comment.objects.filter(object_id=shelter_id, content_type=content_type)

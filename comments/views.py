from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Application
from accounts.models import Shelter, Seeker, CustomUser
from .serializers import CommentSerializer, ReplySerializer

def is_shelter(user_id):
    cur_user = get_object_or_404(CustomUser, pk=user_id)
    if hasattr(cur_user, 'seeker'):
        return False
    return True


class ApplicationCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, application_id, comment_id):
        # check that the user and application exist
        author = get_object_or_404(CustomUser, pk=user_id)
        get_object_or_404(Application, pk=application_id)

        # implement this: check if author is a seeker who submitted the application by getting the application obj with application id -> get the seeker field in that instance

            

        # implement this: check if author is a shelter that reveived the application


        
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, user_id, application_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Application, pk=application_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Application)
            if is_shelter(user_id): # if the current user is a shelter
                author = get_object_or_404(Shelter, pk=user_id)
            else:
                author = get_object_or_404(Seeker, pk= user_id)
            # implement this: check if author is a seeker who submitted the application by getting the application obj with application id -> get the seeker field in that instance

            

            # implement this: check if author is a shelter that reveived the application


            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, 
                            author = author,
                            object_id=application_id, content_type=content_type)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ApplicationCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id, user_id):
        # check that the user and application exist
        author = get_object_or_404(CustomUser, pk=user_id)
        application = get_object_or_404(Application, pk=application_id)

        # implement this: check if author is a seeker who submitted the application by getting the application obj with application id -> get the seeker field in that instance

            

        # implement this: check if author is a shelter that reveived the application


            
        # filter for comments associated with the application
        content_type = ContentType.objects.get_for_model(Application)
        comments = Comment.objects.filter(content_type=content_type, object_id=application_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, application_id, user_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # implement this: check if author is a seeker who submitted the application by getting the application obj with application id -> get the seeker field in that instance

            

            # implement this: check if author is a shelter that reveived the application


           
            content_object = get_object_or_404(Application, pk=application_id)
            content_type = ContentType.objects.get_for_model(Application)

            if is_shelter(user_id):
                author = get_object_or_404(Shelter, pk=user_id)
            else:
                author = get_object_or_404(Seeker, pk= user_id)
                
            serializer.save(content_object=content_object, 
                            author = author,
                            object_id=application_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ShelterCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, shelter_id, comment_id):
        # check the user and shelter exist
        get_object_or_404(Shelter, pk=shelter_id)
        get_object_or_404(CustomUser, pk=user_id)

        comment = get_object_or_404(Comment, pk = comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, user_id, shelter_id, comment_id):
        serializer = ReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_object = get_object_or_404(Shelter, pk=shelter_id)
            comment = get_object_or_404(Comment, pk=comment_id)
            content_type = ContentType.objects.get_for_model(Shelter)
            
            if is_shelter(user_id):
                author = get_object_or_404(Shelter, pk=user_id)
            else:
                author = get_object_or_404(Seeker, pk= user_id)
            
            # save the new reply with the comment related to the application
            serializer.save(comment=comment, content_object=content_object, 
                            author = author,
                            object_id=shelter_id, content_type=content_type)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShelterCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, shelter_id):
        # check the user and shelter exist
        get_object_or_404(Shelter, pk=shelter_id)
        get_object_or_404(CustomUser, pk=user_id)
        
        # filter for comments made to the shelter
        content_type = ContentType.objects.get_for_model(Shelter)
        comments = Comment.objects.filter(object_id=shelter_id, content_type=content_type)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, shelter_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            content_type = ContentType.objects.get_for_model(Shelter)
            serializer.save(object_id=shelter_id, content_type=content_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ShelterDashboardCommentsView(generics.ListAPIView): # for shelter comments only, if shelter wants to view application comments: in application --> reply --> application comment details page
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         shelter_id = self.kwargs['shelter_id']
#         content_type = ContentType.objects.get_for_model(Shelter)
#         return Comment.objects.filter(object_id=shelter_id, content_type=content_type)

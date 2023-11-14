from rest_framework import serializers
from .models import Comment, Reply




class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.USERNAME_FIELD')
    comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reply
        fields = [
            'id', 'text', 'author', 'created_at', 'comment',
            'object_id', 'content_type'
        ]
        read_only_fields = ['author', 'comment', 'created_at', 'object_id', 'content_type']

    def create(self, validated_data):
        # set the author to the current user
        user = self.context['request'].user
        validated_data['author'] = user

        return Reply.objects.create(**validated_data)



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.USERNAME_FIELD')
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'rating', 'text', 'author', 'created_at', 
            'object_id', 'content_type', 'replies'
        ]
        read_only_fields = ['author', 'created_at', 'object_id', 'content_type']

    def create(self, validated_data):
        # set the author to the current user
        user = self.context['request'].user
        validated_data['author'] = user

        return Comment.objects.create(**validated_data)
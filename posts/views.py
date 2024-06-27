from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import Candidate
from authentication.serializers import CandidateSerializer



# Create a new post
# @permission_classes([IsAuthenticated])  

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all posts
@api_view(['GET'])
def list_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# Read details of a specific post
@api_view(['GET'])
def retrieve_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post)
    return Response(serializer.data)

# Update an existing post
@api_view(['PUT'])
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete an existing post
@api_view(['DELETE'])
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Find candidates by its post
@api_view(['GET'])
def findCandidate(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        candidates = Candidate.objects.filter(application__post=post)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
 
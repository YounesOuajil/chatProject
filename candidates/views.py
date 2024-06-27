from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import Candidate,Application
from authentication.serializers import CandidateSerializer,ApplicationSerializer
from rest_framework import status
from posts.models import Post

# Create a new candidate

@api_view(['POST'])
def create_candidate(request):
    serializer = CandidateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email')

        # Check if user already exists
        if Candidate.objects.filter(username=username).exists():
            return Response({'error': 'Candidate with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating a new user with encrypted password
        user =Candidate.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active=True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all candidates
@api_view(['GET'])
def list_candidates(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

# Read details of a specific candidate
@api_view(['GET'])
def retrieve_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    serializer = CandidateSerializer(candidate)
    return Response(serializer.data)

# Update an existing candidate
@api_view(['PUT'])
def update_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    serializer = CandidateSerializer(candidate, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete an existing candidate
@api_view(['DELETE'])
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    candidate.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def apply_for_job(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():

        candidate_object = serializer.validated_data['candidate'] #here we return un object not just geting the id
        post_object = serializer.validated_data['post']


        # Accessing IDs from candidate and post objects
        candidate_id = candidate_object.id
        post_id = post_object.id

        try:
            # Retrieve candidate and post objects based on the provided IDs
            candidate = Candidate.objects.get(pk=candidate_id)
            post = Post.objects.get(pk=post_id)

            application_status = serializer.validated_data.get('status')
            additional_documents = serializer.validated_data.get('additional_documents')

            # Check if the candidate has already applied to this post
            if Application.objects.filter(post=post, candidate=candidate).exists():
                return Response({'message': 'You have already applied to this offer'}, status=status.HTTP_409_CONFLICT)

            # Create a new application if the candidate hasn't already applied
            Application.objects.create(post=post, candidate=candidate, status=application_status, additional_documents=additional_documents)
            return Response({'message': 'Application submitted successfully'}, status=status.HTTP_201_CREATED)

        except Candidate.DoesNotExist:
            return Response({'message': 'Candidate does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















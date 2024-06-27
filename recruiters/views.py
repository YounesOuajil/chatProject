from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import Recruiter,Candidate,Application
from authentication.serializers import RecruiterSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, DateTimeField, Q
from django.db.models.functions import TruncMonth
from rest_framework.response import Response



@api_view(['POST'])
def create_recruiter(request):
    serializer = RecruiterSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email= serializer.validated_data.get('email')
        # Check if user already exists
        if Recruiter.objects.filter(username=username).exists():
            return Response({'error': 'User with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creating a new user with encrypted password
        user = Recruiter.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_recruiters(request):
    recruiters = Recruiter.objects.all()
    serializer = RecruiterSerializer(recruiters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    serializer = RecruiterSerializer(recruiter)
    return Response(serializer.data)

@api_view(['PUT'])
def update_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    serializer = RecruiterSerializer(recruiter, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    recruiter.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
def candidates_applied_to_RHposts(request, recruiter_id): 
    try:
        # Retrieve the recruiter
        recruiter = Recruiter.objects.get(pk=recruiter_id)
        
        # Calculate the datetime 6 months ago
        six_months_ago = timezone.now() - timedelta(days=30 * 6)
        
        # Filter posts associated with the recruiter
        posts = Post.objects.filter(recruiter=recruiter)
        
        # Aggregate the number of candidates who applied each month for each post over the last 6 months
        applications_data = (
            Application.objects
            .filter(post__in=posts, date__gte=six_months_ago)
            .annotate(month=TruncMonth('date', output_field=DateTimeField()))
            .values('month', 'post')
            .annotate(total_candidates=Count('candidate'))
            .order_by('month', 'post')
        )
        
        # Format the data for each month
        response_data = {}
        for data in applications_data:
            month_str = data['month'].strftime('%m')
            post_id = data['post']
            total_candidates = data['total_candidates']
            
            if month_str not in response_data:
                response_data[month_str] = {}
            
            response_data[month_str][post_id] = {
                'total_candidates': total_candidates,
            }
        
        return Response(response_data)
        
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found for this recruiter'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def candidates_by_gender_per_recruiter(request, recruiter_id): 
    try:
        # Retrieve the recruiter
        recruiter = Recruiter.objects.get(pk=recruiter_id)
        # Calculate the datetime 6 months ago
        six_months_ago = timezone.now() - timedelta(days=30 * 6)
        # Filter posts associated with the recruiter
        posts = Post.objects.filter(recruiter=recruiter)
        # Aggregate the number of male and female candidates who applied for each post over the last 6 months
        applications_data = (
            Application.objects
            .filter(post__in=posts, date__gte=six_months_ago)
            .annotate(month=TruncMonth('date'))
            .values('month', 'post')
            .annotate(male=Count('candidate', filter=Q(candidate__gender='m')),
                      female=Count('candidate', filter=Q(candidate__gender='f')))
            .order_by('month', 'post')
        )
        # Format the data for each month
        response_data = {}
        for data in applications_data:
            month_str = data['month'].strftime('%m')
            post_id = data['post']
            male_count = data.get('male', 0) 
            female_count = data.get('female', 0)  
            
            month_data = response_data.setdefault(month_str, {})
            post_data = month_data.setdefault(str(post_id), {})
            post_data.update({
                'male': male_count,
                'female': female_count,
            })
        
        return Response(response_data)
        
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found for this recruiter'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def total_application_on_recruiter_posts(request, recruiter_id): 
    try:
        # Retrieve the recruiter
        recruiter = Recruiter.objects.get(pk=recruiter_id)
        
        # Filter posts associated with the recruiter
        posts = Post.objects.filter(recruiter=recruiter)
        
        # Aggregate the number of applications for each post
        post_applications = []
        for post in posts:
            total_applications = Application.objects.filter(post=post).count()
            post_applications.append({
                'post_id': post.id,
                'post_title': post.title,
                'total_applications': total_applications
            })
        
        return Response(post_applications)
        
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found for this recruiter'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def total_application_and_post(request, recruiter_id):
    try:
        # Retrieve the recruiter
        recruiter = Recruiter.objects.get(pk=recruiter_id)
        
        # Filter posts associated with the recruiter
        posts = Post.objects.filter(recruiter=recruiter)
        
        # Get total applications on recruiter's posts
        total_applications = Application.objects.filter(post__in=posts).count()

        # Get total number of posts made by the recruiter
        total_posts = posts.count()

        return Response({
            'total_applications': total_applications,
            'total_posts': total_posts
        })
        
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)
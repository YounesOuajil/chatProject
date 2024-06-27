from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Internship,Intern
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import InternshipSerializer,InternSerializer
from django.http import JsonResponse
import json

from authentication.models import Recruiter



@api_view(['POST'])
def create_Internship(request):
    serializer = InternshipSerializer(data=request.data)
    if serializer.is_valid():
        recruiter_id = serializer.validated_data.get('recruiter')
        try:
            recruiter = Recruiter.objects.get(pk=recruiter_id)
        except recruiter.DoesNotExist:
            return Response({'error': 'Recruiter does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_Internship(request):
    interns = Internship.objects.all()
    serializer = InternshipSerializer(interns, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_Internship(request, Internship_id):
    intern = get_object_or_404(Internship, pk=Internship_id)
    serializer = InternshipSerializer(intern)
    return Response(serializer.data)

@api_view(['PUT'])
def update_Internship(request, Internship_id):
    intern = get_object_or_404(Internship, pk=Internship_id)
    serializer = InternshipSerializer(intern, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_Internship(request, Internship_id):
    intern = get_object_or_404(Internship, pk=Internship_id)
    intern.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_Intern(request):
    interns = Intern.objects.all()
    serializer = InternSerializer(interns, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_Intern(request):
    serializer = InternSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def retrieve_Intern(request, intern_id):
    try:
        intern = Intern.objects.get(pk=intern_id)
    except Intern.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InternSerializer(intern)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InternSerializer(intern, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        intern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['Post'])
# def create_interns_from_json(request, json_file_path=None):
#     if json_file_path is None:
#         json_file_path = request.query_params.get('json_file_path')

#     if json_file_path:
#         try:
#             with open(json_file_path, 'r') as file:
#                 data = json.load(file)
#                 interns_data = data.get('interns', []) 

#                 for intern_data in interns_data:
#                     intern = Intern(
#                         name=intern_data.get('name'),
#                         email=intern_data.get('email'),
#                         phone=intern_data.get('phone'),
#                         skills=intern_data.get('skills'),
#                         education=intern_data.get('education'),
#                     )
#                     intern.save()  

#             return Response({'message': 'Interns created successfully'})
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)
#     else:
#         return Response({'error': 'No JSON file path provided'}, status=400)



# @api_view(['POST'])
# def create_Internship(request,recruiter_id):
#     if request.method == 'POST':
#         get_object_or_404(Recruiter,pk=recruiter_id)
#         # Load access token data from JSON file
#         with open(r'C:\Users\youne\OneDrive\Desktop\project4\backend_django-master\backend_django-master\utils\test.json', 'r') as f:
#             access_token_data = json.load(f)

#         # Create Intern instance
#         internship = Internship.objects.create(
#             access_token=access_token_data,
#             recruiter_id=recruiter_id
#         )
        
#         return JsonResponse({'message': 'Intern created successfully'}, status=201)
    
#     return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['GET'])
def all_Internship_Interns(request, Internship_id):
    try:
        internship = Internship.objects.get(pk=Internship_id)
        interns = Intern.objects.filter(internships=internship)
        serializer = InternSerializer(interns, many=True)
        return Response({"interns": serializer.data})
    except Internship.DoesNotExist:
        return Response({"error": "Internship matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)




import sys
sys.path.append('C:/Users/youne/OneDrive/Desktop/ATS_Project/Scrapping_Service/Outlook')
from demo import handle_Scrapping

@api_view(['GET'])
def start_scraping(request,Internship_id):
    internship = get_object_or_404(Internship, pk=Internship_id)
    
    subject = internship.subject

    handle_Scrapping(subject, Internship_id)
    
    return Response({'subject': subject,'Internship_id': Internship_id})





@api_view(['GET'])
def code_outlook(request, Internship_id):
    json_file_path = r'C:\Users\youne\OneDrive\Desktop\testdjango\user_code.json'
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            user_code_key = f'user_code_{Internship_id}'
            user_code = data.get(user_code_key)
            if user_code:
                return Response({'user_code': user_code})
            else:
                return Response({'error': f'User code for Internship ID {Internship_id} not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

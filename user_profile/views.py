import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from user_profile import models


@api_view(['GET', 'POST', 'PATCH'])
def upload_profile(request):
    try:
        if request.method == 'GET':
            ''' To get user profile information 
            Input params : User Id (int)
            Response : user profile info in Json response
            '''
            user_id = request.GET.get('user_id')
            user_data = list(User.objects.filter(id=user_id).values('id', 'email', 'first_name', 'last_name'))
            profile_info = models.Profile.objects.filter(user_details__id=user_id)
            if profile_info:
                profile_info = profile_info.values()[0]

                with open(profile_info.get('profile_pic'), "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                profile_info["profile_pic"] = image_data

            return Response({"user_info": user_data, "profile_info": profile_info})

        if request.method == 'POST':
            ''' To save user profile information 
            Input params : Form data 
            Response : Profile created (201)
            '''
            data = request.data
            
            #import pdb;pdb.set_trace()
            file = request.FILES.get('image')

            try:
                # user_da = User.objects.get(id=data.get('user_id'))
                user_da = User.objects.get(id=1)
            except User.DoesNotExist:
                return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

            profile_data = {
                'user_details': user_da,
                'profile_pic': file,
                'gender': data.get('gender'),
                'image_type': data.get('image_type')
            }

            models.Profile.objects.create(**profile_data)

            return Response({"message": "Profile created !"}, status=status.HTTP_201_CREATED)

        if request.method == 'PATCH':
            ''' To update user profile information 
            Input params : Profile data (In Form)
            Response : success (200)
            '''
            data = request.data
            try:
                profile_da = models.Profile.objects.get(id=data.get('profile_id'))
            except models.Profile.DoesNotExist:
                return Response({"error": "Invalid Profile ID."}, status=status.HTTP_400_BAD_REQUEST)

            profile_da.profile_pic = data.get('image')
            profile_da.save()

            return Response({"message": "Profile Updated !"}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

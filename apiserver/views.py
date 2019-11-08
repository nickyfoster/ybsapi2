from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from apiserver.models import User
from apiserver.serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time


# TODO Add CORS support
#

@api_view()
def health_check(request, **kwargs):
    if request.version == 'v1':
        referer = request.META.get('HTTP_REFERER')
        if referer:
            print(referer)
        else:
            print("No referrer")
        return Response(data={'msg': 'Ok'}, status=status.HTTP_200_OK)

    elif request.version == 'v2':
        return Response(data={'msg': 'Not implemented yet'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def users_list(request, format=None, **kwargs):
    """
    List all users or create a new one
    :param request:
    :param format:
    :return:
    """
    if request.version == 'v1':
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                vk_id = serializer.validated_data['vk_id']
                if vk_id != '':
                    list_of_users = User.objects.filter(vk_id=vk_id)
                    if not list_of_users:
                        serializer.save()
                    else:
                        user = list_of_users[0]
                        serializer = UserSerializer(user)
                    return Response(serializer.data)
                else:
                    return Response(data={'msg': 'Empty Vk id'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.version == 'v2':
        return Response(data={'msg': 'Not implemented yet'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None, **kwargs):
    """
    Retrieve, updated or delete a user
    :param request:
    :param pk:
    :param format:
    :return:
    """
    if request.version == 'v1':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.version == 'v2':
        return Response(data={'msg': 'Not implemented yet'}, status=status.HTTP_404_NOT_FOUND)


@api_view()
def workload(request, **kwargs):
    if request.version == 'v1':
        print("Processing")
        ts1 = time.time()
        res = []
        for x in range(1000000, 1001050):
            value = 2 ** x
            res.append(value)
        ts2 = round((time.time() - ts1), 2)
        print(f"****** {ts2} seconds ****** ")
        return Response(data={'msg': f'Done in {ts2} seconds'}, status=status.HTTP_200_OK)
    elif request.version == 'v2':
        return Response(data={'msg': 'Not implemented yet'}, status=status.HTTP_404_NOT_FOUND)

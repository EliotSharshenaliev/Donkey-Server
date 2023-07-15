from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from socket_service.models import UserDeviceTasks
from worker_service.serializer import UserDeviceSerializer


class DeleteTaskByPid(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req, *args, **kwargs):
        print(req)
        return Response({
            "ok": True
        }, status=status.HTTP_200_OK)


from django.dispatch import Signal

signal = Signal()


class UpdateDeviceTasks(APIView):
    def get(self, requests, deviceId, *args, **kwargs):
        query_set = UserDeviceTasks.objects.get(deviceId=deviceId)
        serializer = UserDeviceSerializer(query_set)
        return Response({
            "type": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, requests, *args, **kwargs):
        query_set = UserDeviceTasks.objects.get(deviceId=requests.data.get("deviceId"))
        serializer = UserDeviceSerializer(query_set, data=requests.data)
        if serializer.is_valid():
            serializer.save()
            # signal.send(sender=UserDeviceTasks)
            return Response({
                "type": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return serializer.error_messages

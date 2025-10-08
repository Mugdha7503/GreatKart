from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": getattr(user, "email", None),
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
        })


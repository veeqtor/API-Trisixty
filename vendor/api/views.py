"""Module for the views"""
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from vendor.api.serializer import VendorSerializer

from utils.messages import MESSAGES
from utils.permissions import VerifiedBusinessAccountPermission, IsAuthenticated


class VendorView(viewsets.GenericViewSet,
                 mixins.CreateModelMixin):
    """A viewset for viewing and editing vendor instances."""

    serializer_class = VendorSerializer
    permission_classes = (IsAuthenticated,
                          VerifiedBusinessAccountPermission)

    def create(self, request, *args, **kwargs):
        """Create a new vendor"""

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.validated_data['created_by'] = request.user.full_name
            self.perform_create(serializer)

            msg = {
                'status': 'success',
                'message': MESSAGES['CREATED'].format('Vendor'),
            }
            return Response(msg, status=status.HTTP_201_CREATED)

        msg = {
            'status': 'error',
            'errors': serializer.errors,
        }

        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

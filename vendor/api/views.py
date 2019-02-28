"""Module for the views"""
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from vendor.api.serializer import VendorSerializer
from vendor.models import Vendor

from utils.messages import MESSAGES
from utils.permissions import (VerifiedBusinessAccountPermission,
                               IsAuthenticated)


class VendorView(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """A viewset for viewing and editing vendor instances."""

    queryset = Vendor.objects.all()
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

    def list(self, request, *args, **kwargs):
        """View all vendors"""

        queryset = self.get_queryset()

        try:
            page = self.paginate_queryset(queryset)

        except Exception as e:

            return Response({
                "status": 'success',
                "message": 'The page requested is not valid.',
                "data": []
            })

        if page is not None:

            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            results = paginated_response.data.pop('results')
            meta = paginated_response.data

            return Response({"status": 'success',
                             "message": MESSAGES['FETCHED'].format('Vendors'),
                             "meta": meta,
                             "data": results
                             })

    def get_queryset(self):
        """queryset to get all vendors for authenticated users and owners"""

        queryset = self.queryset
        user = self.request.user
        is_business_account = user.account_type == 'BUSINESS'

        if is_business_account:
            queryset = queryset.filter(owner=self.request.user)

        return queryset

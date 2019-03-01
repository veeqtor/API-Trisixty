"""Module for the views"""
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from vendor.api.serializer import VendorSerializer, VendorDetailsSerializer
from vendor.models import Vendor

from utils.messages import MESSAGES
from utils.permissions import (VerifiedBusinessAccountPermission,
                               IsAuthenticated)


class VendorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin):
    """A viewSet for viewing and editing vendor instances."""

    queryset = Vendor.objects.all().filter(deleted=False)
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

            response = {
                "status": 'success',
                "message": 'The page requested is not valid.',
                "data": []
            }

            return Response(response)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            results = paginated_response.data.pop('results')
            meta = paginated_response.data

            response = {
                "status": 'success',
                "message": MESSAGES['FETCHED'].format('Vendors'),
                "meta": meta,
                "data": results
            }

            return Response(response)

    def retrieve(self, request, *args, **kwargs):
        """View method for retrieving a single vendor"""

        instance = self.get_object()
        serializer = self.get_serializer_class()
        serialized_data = serializer(instance).data

        response = {
            "status": 'success',
            "message": MESSAGES['FETCHED'].format('Vendor'),
            "data": serialized_data
        }

        return Response(response)

    def partial_update(self, request, *args, **kwargs):
        """View to update vendors"""

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_by'] = request.user.full_name
            self.perform_update(serializer)

            response = {
                "status": 'success',
                "message": MESSAGES['UPDATED'].format('Vendor'),
                "data": serializer.data
            }
            return Response(response)

        msg = {
            'status': 'error',
            'errors': serializer.errors,
        }

        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Method to delete vendors"""

        instance = self.get_object()
        self.perform_destroy(instance)

        response = {
            "status": 'success',
            "message": MESSAGES['DELETED'].format('Vendor'),
        }
        return Response(response)

    @action(methods=['get'], detail=True, url_path='restore')
    def restore(self, request, pk=None):
        """Restoring a deleted vendor"""

        instance = Vendor.objects.filter(pk=pk).first()
        if instance:
            self.check_object_permissions(request, instance)
            instance.deleted = False
            instance.save()

            serializer = self.get_serializer_class()
            serialized_data = serializer(instance).data

            response = {
                "status": 'success',
                "message": MESSAGES['RESTORE'].format('Vendor',
                                                      serialized_data['name']),
                "data": serialized_data
            }
            return Response(response)

        error = {
            "status": "error",
            "message": MESSAGES['NOT_FOUND']
        }

        return Response(error, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True, url_path='delete')
    def hard_delete(self, request, pk=None):
        """Restoring a deleted vendor"""

        instance = Vendor.objects.filter(pk=pk).first()
        if instance:
            self.check_object_permissions(request, instance)
            self.perform_hard_delete(instance)

            response = {
                "status": 'success',
                "message": MESSAGES['P_DELETED'].format('Vendor'),
            }
            return Response(response)

        error = {
            "status": "error",
            "message": MESSAGES['NOT_FOUND']
        }

        return Response(error, status=status.HTTP_404_NOT_FOUND)

    def perform_hard_delete(self, instance):
        """Performs hard delete"""

        instance.hard_delete()

    def get_queryset(self):
        """queryset to get all vendors for authenticated users and owners"""

        queryset = self.queryset
        user = self.request.user
        is_business_account = bool(user.__dict__ and
                                   user.account_type == 'BUSINESS')
        if is_business_account:
            queryset = queryset.filter(owner=self.request.user)

        return queryset

    # Overriding the get_serializer_class method so as to use
    # a different serializer for the retrieve
    def get_serializer_class(self):
        """Custom serializer"""

        if self.action in ('retrieve', 'partial_update'):
            return VendorDetailsSerializer

        return super(self.__class__, self).get_serializer_class()

    # Overriding the get get_permissions method  so as to use
    # a different serializer for the retrieve
    def get_permissions(self):
        """Custom permissions for the retrieve view"""

        if self.action in ('retrieve',):
            self.permission_classes = []

        return super(self.__class__, self).get_permissions()

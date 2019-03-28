"""Module for the product views"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from src.apps.product.api.serializer import (ProductSerializer,
                                             ProductWithVendorSerializer,
                                             ProductWithOwnerSerializer)
from src.apps.product.models import Product
from utils.messages import MESSAGES
from utils.permissions import (IsAuthenticated,
                               VerifiedBusinessAccountPermission)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the products"""

    queryset = Product.objects.filter(deleted=False).all()
    serializer_class = ProductSerializer

    permission_classes = (IsAuthenticated, VerifiedBusinessAccountPermission)

    def list(self, request, *args, **kwargs):
        """View all products"""

        queryset = self.get_queryset()

        try:
            page = self.paginate_queryset(queryset)

        except Exception as e:
            response = {
                "status": 'error',
                "message": MESSAGES['INVALID_PAGE'],
                "data": []
            }

            return Response(response, status.HTTP_404_NOT_FOUND)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            results = paginated_response.data.pop('results')
            meta = paginated_response.data

            response = {
                "status": 'success',
                "message": MESSAGES['FETCHED'].format('Products'),
                "meta": meta,
                "data": results
            }

            return Response(response)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a product"""
        instance = self.get_object()
        serializer = self.get_serializer_class()
        serialized_data = serializer(instance).data

        response = {
            "status": 'success',
            "message": MESSAGES['FETCHED'].format('Product'),
            "data": serialized_data
        }

        return Response(response)

    def create(self, request, *args, **kwargs):
        """Create a product"""

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            is_owner = bool(serializer.validated_data.get('vendor')
                            .owner == request.user)

            if not is_owner:
                response = MESSAGES['NO_PERMISSION']
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            serializer.validated_data['created_by'] = request.user.full_name
            self.perform_create(serializer)

            response = {
                'status': 'success',
                'message': MESSAGES['CREATED'].format('Product'),
            }
            return Response(response, status=status.HTTP_201_CREATED)

        errors = {
            "status": "error",
            "errors": serializer.errors
        }

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Update a product"""

        instance = self.get_queryset().filter(pk=kwargs['pk']).first()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        if not instance:
            msg = {
                'status': 'error',
                'message': MESSAGES['NOT_FOUND']
            }
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        is_owner_or_superuser = bool(instance.vendor.owner == request.user
                                     or request.user.is_superuser)

        if not is_owner_or_superuser:
            response = MESSAGES['NO_PERMISSION']
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.validated_data['updated_by'] = request.user.full_name
            self.perform_update(serializer)

            response = {
                "status": 'success',
                "message": MESSAGES['UPDATED'].format('Product'),
                "data": serializer.data
            }
            return Response(response)

        msg = {
            'status': 'error',
            'errors': serializer.errors,
        }

        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Soft delete a product"""

        instance = self.get_object()

        if instance:
            self.perform_destroy(instance)

            response = {
                "status": 'success',
                "message": MESSAGES['DELETED'].format('Product'),
            }
            return Response(response)

        error = {
            "status": "error",
            "message": MESSAGES['NOT_FOUND']
        }

        return Response(error, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='new_arrivals')
    def new_arrivals(self, request, *args, **kwargs):
        """Endpoint to get a list of eight latest additions to the products"""

        queryset = self.get_queryset().order_by('-created_at')[:8]
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "status": 'success',
            "message": MESSAGES['FETCHED'].format('Products'),
            "data": serializer.data
        })

    @action(methods=['get'], detail=True, url_path='restore')
    def restore(self, request, *args, **kwargs):
        """Restore a deleted product"""

        instance = self.get_object()

        if instance and instance.deleted:
            instance.deleted = False
            instance.save()

            serializer = self.get_serializer_class()
            serialized_data = serializer(instance).data

            response = {
                "status": 'success',
                "message": MESSAGES['RESTORE'].format('Product',
                                                      serialized_data['title']),
                "data": serialized_data
            }
            return Response(response)

        error = {
            "status": "error",
            "message": MESSAGES['NOT_DELETED']
        }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True, url_path='delete')
    def hard_delete(self, request, *args, **kwargs):
        """Hard delete a product"""

        instance = self.get_object()
        if instance:
            self.perform_hard_delete(instance)

            response = {
                "status": 'success',
                "message": MESSAGES['P_DELETED'].format('Product'),
            }
            return Response(response)

        error = {
            "status": "error",
            "message": MESSAGES['NOT_FOUND']
        }

        return Response(error, status=status.HTTP_404_NOT_FOUND)

    def perform_hard_delete(self, instance):
        """Performs hard deleting"""

        instance.hard_delete()

    # Overriding the get get_permissions method  so as to use
    # a different serializer for the list and retrieve end point
    def get_permissions(self):
        """Custom permissions for the list view"""

        if self.action in ('list', 'retrieve', 'new_arrivals'):
            self.permission_classes = []

        return super(self.__class__, self).get_permissions()

    def get_object(self):
        """Gets the objects from the provided keys"""

        if self.action in ('retrieve',):
            return get_object_or_404(
                    self.get_queryset().filter(pk=self.kwargs['pk']))

        elif self.action in ('hard_delete', 'destroy') and \
                not self.request.user.is_superuser:
            return get_object_or_404(
                    self.get_queryset().filter(pk=self.kwargs['pk'],
                                               vendor__owner=self.request.user)
            )

        elif self.action in ('restore',) and self.request.user.is_superuser:
            return get_object_or_404(
                    Product.objects.filter(pk=self.kwargs['pk']).all())

    def get_serializer_class(self):
        """sets serializer class for side-loading vendors and owner."""

        if self.request:
            include = self.request.query_params.get('include')

            if include and 'vendor' in include:
                self.serializer_class = ProductWithVendorSerializer

            if include and 'owner' in include:
                self.serializer_class = ProductWithOwnerSerializer

        return self.serializer_class

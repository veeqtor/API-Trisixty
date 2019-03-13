"""Module for the product views"""

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from product.models import Product
from product.api.serializer import ProductSerializer

from utils.permissions import (IsAuthenticated,
                               VerifiedBusinessAccountPermission)
from utils.messages import MESSAGES


class ProductViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin):
    """ViewSet for the products"""

    queryset = Product.objects.filter(deleted=False).all()
    serializer_class = ProductSerializer

    permission_classes = (IsAuthenticated, VerifiedBusinessAccountPermission)

    def list(self, request, *args, **kwargs):
        """Method to view all products"""

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
        """Method to retrieve all product"""
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
        """Method to create a product"""

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
        """View to update products"""

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

    # Overriding the get get_permissions method  so as to use
    # a different serializer for the list and retrieve end point
    def get_permissions(self):
        """Custom permissions for the list view"""

        if self.action in ('list', 'retrieve'):
            self.permission_classes = []

        return super(self.__class__, self).get_permissions()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product
from .serializers import ProductSerializer


class CreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = JWTAuthentication,

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class ProductListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = JWTAuthentication,

    def get(self, request):
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class DetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = JWTAuthentication,

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, user=request.user)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Exception:
            return Response({"detail": "Mahsulot topilmadi"})



class UpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = JWTAuthentication,

    def put(self, request, pk):
        product = Product.objects.get(pk=pk, user=request.user)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = JWTAuthentication,

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, user=request.user)
            product.delete()
            return Response({"msg": "Mahsulot o‘chirildi"})
        except Exception:
            return Response({"detail": "Mahsulot topilmadi"})
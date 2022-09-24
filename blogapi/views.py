from django.shortcuts import render

from blogapi.models import Mobiles,Reviews,Carts,Orders
from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.serializers import MobileSerializer,MobileModelSerializer,UserSerializer,ReviewSerializer,CartSerializer,OrderSerializer
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action




class MobilesView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileSerializer(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=MobileSerializer(data=request.data)
        if serializer.is_valid():
            Mobiles.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)



class MobileDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            qs=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(qs)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"object doesn't exist"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            instance=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(data=request.data)
            if serializer.is_valid():
                instance.name=serializer.validated_data.get("name")
                instance.price = serializer.validated_data.get("price")
                instance.band = serializer.validated_data.get("band")
                instance.display = serializer.validated_data.get("display")
                instance.processor = serializer.validated_data.get("processor")
                instance.save()
                return Response(data=serializer.data)
            else:
                return Response(serializer.errors)
        except:
            return Response({"msg": "object doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            object.delete()
            return Response({"msg":"deleted"})
        except:
            return Response({"msg": "object doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


class MobileModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors)

class MobileDetailModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(qs)
        return Response(data=serializer.data)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Mobiles.objects.get(id=id)
        qs.delete()
        return Response({"msg":"deleted"})


class MobileViewSetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def create(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)


    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(object)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)

        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


class MobileModelViewSetView(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MobileModelSerializer
    queryset = Mobiles.objects.all()

    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)
    @action(methods=["get"],detail=True)
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        reviews=mobile.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)
    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        carts=Carts.objects.filter(user=user,product=mobile)
        if carts:
            object=carts[0]
            object.quantity+=1
            object.save()
            serializer=CartSerializer(object)
            return Response(data=serializer.data)
        else:

            serializer=CartSerializer(data=request.data,context={"user":user,"product":mobile})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(serializer.errors)
    # @action(methods=["get"],detail=False)
    # def my_cart(self,request,*args,**kwargs):
    #     qs=Carts.objects.filter(user=request.user)
    #     serializer=CartSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    @action(methods=["post"], detail=True)
    def order_place(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=OrderSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)





class UserRegistrationView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CartsView(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

class OrdersView(viewsets.ModelViewSet):
    serializer_class =OrderSerializer
    queryset = Orders.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)










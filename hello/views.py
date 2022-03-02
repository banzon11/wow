from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
import requests
from rest_framework import status
from django.conf import settings
from decouple import config
from django.db.models import Sum,Max
import json
import jwt
from rest_framework.authtoken.models import Token
from .serializer import *
import pandas as pd
from rest_framework.permissions import IsAuthenticated
TOKEN_URL=config('TOKEN_URL')
# Create your views here.
def index(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def generate(user, username, password):
    payload = {
        "agentId": user.id,
        "username": username,
        "password": password,
    }
    
    url = settings.TOKEN_URL
    print(url)
    url_response = requests.post(url, payload)
    print(url_response)
   
    response = json.loads(url_response.text)
    return response

def blackListToken(request):
    token = request.headers['Authorization'].split(' ')[1]
    t, created = BlackListedToken.objects.get_or_create(token=token)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def decode_token(request):
    token = request.headers['Authorization'].split(' ')[1]
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    return decoded_token

def isTokenValid(request):
    token = request.headers['Authorization'].split(' ')[1]
    t = BlackListedToken.objects.filter(token=token)
    if len(t) > 0:
        return False

    return True


def validate_decoded_token(request):
    decodedToken = decode_token(request)
    user_id = decodedToken['user_id']

    if not isTokenValid(request):
        return False, decodedToken

    try:
        user = User.objects.get(pk=user_id)
        if user:
            return True, decodedToken
    except:
        return False, decodedToken

# First part is for the authentication and logout of users
class LoginView(APIView):
    permission_classes = () 
    def post(self, request):
        
        email = request.data["email"]
    
        password = request.data["password"]
        query = User.objects.all()
   
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response({"status": "Failed", "message": "We don't recognize this user with that username.",
                            "error_message": str(e)})

        if user:    
            if not user.is_active:
                return Response({"status": "Failed", "message": "This user is not active."})
            if not user.check_password(password):
                return Response({"status": "Failed", "message": "Password is incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)
            print("waw")
            token,created = Token.objects.get_or_create(user=user)
            
            
          
   
        else:
            return Response({"status": "Failed", "message": "This user doesn't exists."})
      
        return Response({
                        "token":token.key,"user_id":user.id}, status=status.HTTP_202_ACCEPTED)
   
       
class LogoutView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

#For the countries VIew
class CountryView(APIView):
    
    def get(self,request):
        permission_classes = (IsAuthenticated) 
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        up=User.objects.get(pk=token.id)
        print(up)
        print("here")
        country = Countries.objects.all()
        print(country)
        serializer=CountrySerializer(country,many=True,context={"request": request})
        print(serializer)
        return Response(serializer.data)

#this is for editing the user
    
class EditUserView(APIView):
    def get(self,request,id=None):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        up=User.objects.get(pk=token.id)
        serializer=UserSerializer(up)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,id=None):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        
        current_agent.email=request.data["email"]
        current_agent.first_name=request.data["first_name"]
        current_agent.last_name=request.data["last_name"]
        current_agent.save()
        up=UserProfile.objects.get(user=current_agent)
        up.age=request.data["age"]
        country=Countries.objects.get(pk=int(request.data["country"]))
        up.countries=country
        city=Cities.objects.get(pk=int(request.data["city"]))
        up.cities=city
        up.company=request.data["company"]
        up.save()
        return Response(status=status.HTTP_200_OK)

# This part is for the User part the first View will be for the get whole and add new sales 
class SalesUserView(APIView):
    def get(self,request):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        sales=SalesProduct.objects.filter(user=current_agent)
        serializer=SalesSerializer(sales,many=True,context={"request": request})
        return Response(serializer.data)

    def post(self,request):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        prod=Product.objects.filter(name=request.data["product"])
        user=User.objects.get(pk=int(request.data["user_id"]))
        sales=SalesProduct.objects.create(
        
        
        product=prod[0],
        
        revenue=request.data["revenue"],
        
        sales_number=request.data["sales_number"],
        
        date=request.data["date"],
        
        user=user)
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class NewSalesUserView(APIView):
    def delete(self,request,id=None):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        sales=SalesProduct.objects.get(pk=id).delete()
   
        return Response(status=status.HTTP_204_NO_CONTENT)



    def patch(self,request,id=None):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        sales=SalesProduct.objects.get(pk=id)
        data=request.data.keys()
        print(data)
        if "product" in data:
            prod=Product.objects.filter(name=request.data["product"])
            sales.product=prod[0]
        if "revenue" in data:
            sales.revenue=request.data["revenue"]
        if "sales_number" in data:
            sales.sales_number=request.data["sales_number"]
        if "date" in data:
            sales.date=request.data["date"]
        if "user_id" in data:
            user=User.objects.get(pk=int(request.data["user_id"]))
            sales.user=user
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request,id=None):
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        sales=SalesProduct.objects.get(pk=id)
        
        prod=Product.objects.filter(name=request.data["product"])
        sales.product=prod[0]
        
        sales.revenue=request.data["revenue"]
        
        sales.sales_number=request.data["sales_number"]
        
        sales.date=request.data["date"]
        user=User.objects.get(pk=int(request.data["user_id"]))
        sales.user=user
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class SalesView(APIView):
    def get(self,request):
        
        permission_classes = (IsAuthenticated)
        g=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        token=Token.objects.get(key=g).user
        current_agent=User.objects.get(pk=token.id)
        sum=SalesProduct.objects.filter(user=current_agent).aggregate(Sum('sales_number'))
        
        revenue=SalesProduct.objects.filter(user=current_agent).aggregate(Sum('revenue'))
        sumall=SalesProduct.objects.all().aggregate(Sum('sales_number'))
        revenueall=SalesProduct.objects.aggregate(Sum('revenue'))
        highrevenue= SalesProduct.objects.filter(user=current_agent)
        try:
            highre = SalesProduct.objects.latest('revenue')
        except:
            return Response({"status": "failed", "message": "no sales product available"})
        print(highre)
        products=Product.objects.all()
        
        max=0
        max1=0
        for g in products:
            print(g)
            tempsum=SalesProduct.objects.filter(user=current_agent,product=g).aggregate(Sum('revenue'))
            print(tempsum)
            if tempsum['revenue__sum']>max:
                max=tempsum['revenue__sum']
                tally={"product_name":g.name,"price":max}
            tempmax=SalesProduct.objects.filter(user=current_agent,product=g).aggregate(Sum('sales_number'))
            if tempmax['sales_number__sum']>max1:
                max=tempmax['sales_number__sum']
                tally1={"product_name":g.name,"price":max}
        print(tally1)    
        return Response({"average_sales_for_current_user":revenue["revenue__sum"]/sum["sales_number__sum"],"average_sales_all_user":revenueall["revenue__sum"]/sumall["sales_number__sum"], "highest_revenue_sale_for_current_user":{"sale_id":highre.id,"revenue":highre.revenue},"product_highest_revenue_for_current_user":{"product_name":tally["product_name"],"price":tally["price"]},"product_highest_sales_number_for_current_user":{"product_name":tally1["product_name"],"price":tally1["price"]}})


class UploadCountryAndCityView(APIView):
    permission_classes = () 
    def post(self,request):
        try:
            file = request.FILES['file']
            print(file)
            pandas=pd.read_csv(file)
            print(pandas)
            for index, row in pandas.iterrows():
                country,created=Countries.objects.get_or_create(name=row['Country'])
                city=Cities.objects.create(name=row['City'],country=country)
            return Response(status=status.HTTP_200_OK)
        except:
            print("waw")

class UploadSalesView(APIView):
    permission_classes = () 
    def post(self,request,id=None):
        print(id)
        try:
            file = request.FILES['file']
            print(file)
            pandas=pd.read_csv(file)
            print(3)
            user=User.objects.get(pk=id)
            print(pandas)
            for index, row in pandas.iterrows():
                prod,created=Product.objects.get_or_create(name=row['product'])
                sp=SalesProduct.objects.create(sales_number=row['sales_number'],revenue=row['revenue'],product=prod,date=row['date'],user=user )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "failed", "message": "Something went wrong. Document failed to update. {}".format(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
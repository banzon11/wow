
from rest_framework import serializers
from hello.models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"

    
    def to_representation(self, instance):
        print("wow")
        response = super().to_representation(instance)
        print(instance.name)
        city=Cities.objects.filter(country_id=instance.id)
        response["cities"]=[{"id":ct.id,"name":ct.name} for ct in city]

        return response
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesProduct
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["product"]=instance.product.name
        return response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username","email","first_name","last_name"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        up=UserProfile.objects.get(user=instance)
        response["gender"]=up.gender
        response["age"]=up.age
        response["country"]=up.countries.name
        response["city"]=up.cities.name
        response["company"]=up.company
        return response
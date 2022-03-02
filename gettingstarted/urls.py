from django.urls import path, include

from django.contrib import admin
from rest_framework import permissions
from hello.views import *
import hello.views
from rest_framework_simplejwt.views import TokenObtainPairView
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('redoc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here

    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('api/v1/logout/',LogoutView.as_view(), name='user-logout'),
    path('api/v1/login/',LoginView.as_view(), name='user-login'),
    path('api/v1/gettoken/', TokenObtainPairView.as_view(), name='gettoken'),
    path('api/v1/countries/', CountryView.as_view(), name='country'),
    path('api/v1/sale_statistics/',SalesView.as_view(), name='salesall'),
    path('api/v1/users/<int:id>',EditUserView.as_view(), name='edituser'),
    path('api/v1/sales/',SalesUserView.as_view(), name='salesuseronly'),
    path('api/v1/sales/<int:id>',NewSalesUserView.as_view(), name='salesuser'),
    path('api/v1/import/place/<int:id>',UploadCountryAndCityView.as_view(), name='import-place'),
    path('api/v1/import/sales/<int:id>',UploadSalesView.as_view(), name='import-sales'),

]

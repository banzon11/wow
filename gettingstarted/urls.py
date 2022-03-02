from django.urls import path, include

from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
admin.autodiscover()
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

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("", hello.views.index, name="index"),
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
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

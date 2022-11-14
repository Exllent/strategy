from django.urls import path

from main.views import Home, CastleBuilding, CastleProduction

urlpatterns: list[path] = [
    path(route='', view=Home.as_view(), name='home'),
    path(route='castle/<int:castle_id>/', view=CastleBuilding.as_view(), name='castle'),
    path(route='production/<int:castle_id>/', view=CastleProduction.as_view(), name='production'),
]

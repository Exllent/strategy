from django.views import View

from main.models import Castle, ResourceBuildings, Buildings
from main.services import MixinHomePage, CastleMixin, CastleProductionMixin


class Home(MixinHomePage, View):
    """Класс отображающий главную страницу"""

    template_name = "main/index.html"
    model_castle = Castle


class CastleBuilding(CastleMixin, View):
    """Класс отображающий здания замка и их уровень"""

    template_name = "main/castle.html"
    model_castle = Castle


class CastleProduction(CastleProductionMixin, View):
    """Класс для улучшения ресурсо добывающих зданий замка"""

    template_name = "main/castle_production.html"
    model_castle = Castle
    model_buildings = Buildings
    model_resource_buildings = ResourceBuildings

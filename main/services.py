from django.db.models import F
from django.shortcuts import render, redirect

from main.constants import ConstantsResourceBuildings as res_const, ConstantsBuildings as b_const
from main.models import ResourceBuildings, Buildings


def create_resource_buildings(model_resource_buildings: ResourceBuildings, castle_id: int) -> None:
    """Строит ресурсные здания новому пользователю функция отрабатывает единоразово"""
    model_resource_buildings.objects.create(
        name=res_const.QUARRY.value, resource="stones", castle_id=castle_id
    )
    model_resource_buildings.objects.create(
        name=res_const.MINE.value, resource="iron", castle_id=castle_id
    )
    model_resource_buildings.objects.create(
        name=res_const.FARM.value, resource="food", castle_id=castle_id
    )
    model_resource_buildings.objects.create(
        name=res_const.SAWMILL.value, resource="wood", castle_id=castle_id
    )


def create_stock_buildings(model_buildings: Buildings, castle_id: int) -> None:
    model_buildings.objects.create(name=b_const.STOCK.value, castle_id=castle_id)


class CastleProductionMixin:
    """Класс для прокачки зданий по добычи ресурсов"""

    template_name = None
    model_castle = None
    model_buildings = None
    model_resource_buildings = None

    def get(self, request):
        castle = self.get_castle(request)
        resource_buildings = self.model_resource_buildings.objects.filter(
            castle_id=castle.pk
        )
        return render(
            request=request,
            template_name=self.template_name,
            context={"resource": resource_buildings},
        )

    def post(self, request):
        castle = self.get_castle(request)
        if request.POST.get("resource"):
            create_resource_buildings(self.model_resource_buildings, castle.pk)
            return redirect(
                request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
            )
        else:
            building = list(request.POST)[-1]
            self.model_resource_buildings.objects.filter(name=building).update(
                level=F("level") + 1
            )

            return redirect(
                request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
            )

    def get_castle(self, request):
        """Получает замок из id пользователя"""
        castle = self.model_castle.objects.get(id=getattr(request.user, "castle_id"))
        return castle


class MixinHomePage:
    """Класс для отображения главной страницы сайта"""

    template_name = None
    model_castle = None

    def get(self, request):
        castle = self.get_castle(request)
        context = {"castle": castle}
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def get_castle(self, request):
        """Получает замок из id пользователя"""
        castle = self.model_castle.objects.get(id=getattr(request.user, "castle_id"))
        return castle


class CastleMixin:
    """Класс отображающий здания замка и их уровень"""

    template_name = None
    model_castle = None

    def get(self, request, **kwargs):
        """Получаем замок и его характеристики"""
        castle = self.get_castle(kwargs["castle_id"])
        context = {"castle": castle}
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def get_castle(self, castle_id):
        """Получает замок пользователя из модели"""
        castle = self.model_castle.objects.get(pk=castle_id)
        return castle

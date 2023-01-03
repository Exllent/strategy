from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from main.constants import ConstantsResourceBuildings as res_const, ConstantsBuildings as b_const
from main.models import ResourceBuildings, Buildings, Castle
from main.tasks import celery_task_update_resources


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


def create_buildings(model_buildings: Buildings, castle_id: int) -> None:
    model_buildings.objects.create(name=b_const.STOCK.value, castle_id=castle_id)


class CastleProductionMixin:
    """Класс для прокачки зданий по добычи ресурсов"""

    template_name: str = None
    model_castle: Castle = None
    model_buildings: Buildings = None
    model_resource_buildings: ResourceBuildings = None

    def get(self, request: HttpRequest, castle_id: int) -> HttpResponse:
        resource_buildings = self.model_resource_buildings.objects.filter(
            castle_id=castle_id
        )
        return render(
            request=request,
            template_name=self.template_name,
            context={"resource": resource_buildings},
        )

    def post(self, request: HttpRequest, castle_id: int) -> HttpResponse:
        if request.POST.get("resource"):
            create_resource_buildings(self.model_resource_buildings, castle_id)
            create_buildings(self.model_buildings, castle_id)
            return redirect(
                request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
            )
        else:
            celery_task_update_resources.delay(castle_id)
            building = list(request.POST)[-1]
            res = self.model_resource_buildings.objects.get(name=building)
            res.level = F("level") + 1
            res.save()

            return redirect(
                request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
            )

    def get_castle(self, castle_id):
        """Получает замок пользователя из модели"""
        castle = self.model_castle.objects.get(pk=castle_id)
        return castle


class MixinHomePage:
    """Класс для отображения главной страницы сайта"""

    template_name = None
    model_castle = None

    def get(self, request: HttpRequest) -> HttpResponse:
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

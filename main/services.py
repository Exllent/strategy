from django.db.models import F
from django.shortcuts import render, redirect

from main.constants import ConstantsResourceBuildings as const


def create_resource_buildings(model_resource_buildings, pk):
    """Строит ресурсные здания новому пользователю функция отрабатывает единоразово"""
    model_resource_buildings.objects.create(
        name=const.Quarry, resource="stones", castle_id=pk
    )
    model_resource_buildings.objects.create(
        name=const.Mine, resource="iron", castle_id=pk
    )
    model_resource_buildings.objects.create(
        name=const.Farm, resource="food", castle_id=pk
    )
    model_resource_buildings.objects.create(
        name=const.Sawmill, resource="wood", castle_id=pk
    )


class CastleProductionMixin:
    """Класс для прокачки зданий по добычи ресурсов"""

    template_name = None
    model_castle = None
    model_resource_buildings = None

    def get(self, request, **kwargs):
        castle = self.get_castle(request)
        resource_buildings = self.model_resource_buildings.objects.filter(
            castle_id=castle.pk
        )
        return render(
            request=request,
            template_name=self.template_name,
            context={"resource": resource_buildings},
        )

    def post(self, request, **kwargs):
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
            # resource_buildings = self.model_resource_buildings.objects.get(name=building)
            # setattr(resource_buildings, 'level', F('level') + 1)
            # resource_buildings.save()
            # resource_buildings.refresh_from_db()

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

    # def post(self, request, **kwargs):
    #     """отправляет запрос на получение замка пользователя и улучшение"""
    #     castle = self.get_castle(kwargs['castle_id'])
    #     self.get_building(request, castle)
    #     return redirect(castle)

    def get_castle(self, castle_id):
        """Получает замок пользователя из модели"""
        castle = self.model_castle.objects.get(pk=castle_id)
        return castle

    # @staticmethod
    # def get_building(request, castle):
    #     """Получает здание замкa пользователя и улучшает здание на +1 уровень, возращает изменённый замок"""
    #     building = list(request.POST)[-1]
    #     setattr(castle, building, F(f"{building}") + 1)
    #     castle.save()
    #     castle.refresh_from_db()
    #     return castle

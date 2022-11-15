from django.db.models import F

from averege.celery import app
from main.models import ResourceBuildings, Castle, Buildings


@app.task()
def func(id):
    res = ResourceBuildings.objects.get(pk=id)
    minutes = res.production_per_hour // 60
    castle = Castle.objects.get(pk=res.castle_id)
    setattr(castle, res.resource, F(res.resource) + minutes)
    castle.save()
    castle.refresh_from_db()
    building = Buildings.objects.get(castle_id=castle.pk, name="склад")
    if getattr(castle, res.resource) >= building.characteristic:
        pass
    else:
        func.apply_async((id,), countdown=60)


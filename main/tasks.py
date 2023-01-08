from time import sleep
from celery import shared_task
from .models import ResourceBuildings, Buildings

resources_of_castle = {}


def resources_something(castle_id: int) -> dict:
    building = Buildings.get_capacity_resources_by_castle(castle_id=castle_id)
    capacity_stock = building.capacity
    castle = building.castle
    resources_of_castle[castle_id] = {}
    for resource in ["wood", "food", "stones", "iron"]:
        if (quantity := getattr(castle, resource)) < capacity_stock:
            resources_of_castle[castle_id][resource] = quantity
    return resources_of_castle[castle_id], capacity_stock


@shared_task
def celery_task_update_resources(castle_id: int, time: int = 60):
    if resources_of_castle.get(castle_id) is None:
        while resources_of_castle.get(castle_id) is not {}:
            resources, capacity_stock = resources_something(castle_id)
            resource_buildings = ResourceBuildings.get_resources_buildings(castle_id)
            castle = resource_buildings[0].castle
            for building in resource_buildings:
                production_per_minute = building.production_per_hour // time
                if (resource := building.resource) in resources:
                    resources[resource] += production_per_minute
                    if resources[resource] >= capacity_stock:
                        resources[resource] = capacity_stock
            castle.update_quantity_resources(**resources)
            sleep(time)

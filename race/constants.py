from django.db import models


class RaceChoices(models.TextChoices):
    ORCS = ("Орки_1", "Орки")
    ELVES = ("Эльфы_2", "Эльфы")
    GNOMES = ("Гномы_3", "Гномы")
    PEOPLE = ("Люди_4", "Люди")

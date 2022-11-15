# Generated by Django 4.1.1 on 2022-10-29 18:53

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("main", "0001_initial"),
        ("race", "0001_initial"),
        ("warrior", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Army",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Название армии"
                    ),
                ),
                (
                    "warrior",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="warrior.warrior",
                        verbose_name="Воин",
                    ),
                ),
            ],
            options={
                "verbose_name": "Армия",
                "verbose_name_plural": "Армии",
                "db_table": "army",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "login",
                    models.CharField(
                        error_messages={
                            "unique": "Пользователь с этим логином уже существует"
                        },
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator()
                        ],
                        verbose_name="Логин",
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Пользователь с этим nickname уже существует"
                        },
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="Имя игрока",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        error_messages={
                            "unique": "Пользователь с этой почтой уже существует"
                        },
                        max_length=254,
                        unique=True,
                        verbose_name="E-mail",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Статус персонала"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Последний вход"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=25, unique=True, verbose_name="Слаг"
                    ),
                ),
                (
                    "silver_money",
                    models.PositiveBigIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(
                                limit_value=1000000
                            )
                        ],
                        verbose_name="Серебро",
                    ),
                ),
                (
                    "gold_money",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(limit_value=50000)
                        ],
                        verbose_name="Золото",
                    ),
                ),
                (
                    "army",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.army",
                        verbose_name="Армия",
                    ),
                ),
                (
                    "castle",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.castle",
                        verbose_name="замок",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="race.race",
                        verbose_name="Раса",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "db_table": "custom_user",
                "ordering": ["login"],
            },
        ),
    ]

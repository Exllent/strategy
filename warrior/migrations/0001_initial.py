# Generated by Django 4.1.1 on 2023-01-07 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('race', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warrior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Имя')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Слаг')),
                ('health', models.PositiveSmallIntegerField(default=0, verbose_name='Здоровье')),
                ('damage', models.PositiveSmallIntegerField(default=0, verbose_name='Урон')),
                ('armor', models.PositiveSmallIntegerField(default=0, verbose_name='Броня')),
                ('speed', models.PositiveSmallIntegerField(default=0, verbose_name='Скорость')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='race.race', verbose_name='Раса')),
            ],
            options={
                'verbose_name': 'Характеристика-армии',
                'verbose_name_plural': 'Характеристики-армий',
                'db_table': 'warrior',
                'ordering': ['name'],
            },
        ),
    ]

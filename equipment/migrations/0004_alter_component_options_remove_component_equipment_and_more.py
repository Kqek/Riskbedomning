# Generated by Django 4.2.7 on 2023-11-08 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_alter_component_equipment_alter_equipment_component'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'verbose_name': 'Component', 'verbose_name_plural': 'Components'},
        ),
        migrations.RemoveField(
            model_name='component',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='component',
        ),
        migrations.AddField(
            model_name='component',
            name='equipments',
            field=models.ManyToManyField(blank=True, to='equipment.equipment', verbose_name='categories'),
        ),
        migrations.AlterModelTable(
            name='component',
            table='Components',
        ),
    ]

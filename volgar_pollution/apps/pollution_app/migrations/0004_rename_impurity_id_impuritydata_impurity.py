# Generated by Django 4.0.1 on 2022-01-26 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollution_app', '0003_impuritydata_rename_impurities_impurity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impuritydata',
            old_name='impurity_id',
            new_name='impurity',
        ),
    ]

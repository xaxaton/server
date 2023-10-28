# Generated by Django 3.2.4 on 2023-10-28 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_department_organization_postion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.department",
                verbose_name="отдел",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.organization",
                verbose_name="организация",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.postion",
                verbose_name="должность",
            ),
        ),
    ]

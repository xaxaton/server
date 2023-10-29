# Generated by Django 3.2.4 on 2023-10-29 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0002_alter_ticketanswer_ticket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketanswer",
            name="ticket",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answer",
                to="tickets.ticket",
                verbose_name="обращение",
            ),
        ),
    ]
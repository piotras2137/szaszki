# Generated by Django 3.1.5 on 2022-12-14 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chess', '0006_auto_20221214_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pgn', models.TextField()),
                ('result', models.TextField()),
                ('difficulty', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now=True)),
                ('invite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chess.invite')),
                ('player1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

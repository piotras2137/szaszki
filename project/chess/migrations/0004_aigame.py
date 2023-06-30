# Generated by Django 3.1.5 on 2022-12-14 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chess', '0003_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='AiGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fen', models.TextField()),
                ('result', models.TextField()),
                ('difficulty', models.CharField(max_length=32)),
                ('playercolor', models.TextField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
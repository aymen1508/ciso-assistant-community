# Generated by Django 5.0.4 on 2024-05-20 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_appliedcontrol_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirementnode',
            name='typical_evidence',
            field=models.TextField(blank=True, null=True, verbose_name='Typical evidence'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_answer_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='display_order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('Creative', '创新型企业'), ('Specialized', '专精特新'), ('LittleGiant', '专精特新小巨人'), ('Test', '测试问题')], default='Creative', max_length=50),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
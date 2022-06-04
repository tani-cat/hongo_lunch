# Generated by Django 3.2.8 on 2022-06-04 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lunch_gacha', '0002_auto_20220604_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True, verbose_name='形態名称')),
            ],
            options={
                'verbose_name': '店舗形態',
                'verbose_name_plural': '店舗形態',
            },
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': '店舗地区', 'verbose_name_plural': '店舗地区'},
        ),
        migrations.AlterModelOptions(
            name='lunchgenre',
            options={'verbose_name': '食事ジャンル', 'verbose_name_plural': '食事ジャンル'},
        ),
        migrations.AlterModelOptions(
            name='lunchplace',
            options={'verbose_name': '店舗', 'verbose_name_plural': '店舗'},
        ),
        migrations.AddField(
            model_name='lunchplace',
            name='store_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='lunch_gacha.storetype', verbose_name='店舗形態'),
        ),
    ]
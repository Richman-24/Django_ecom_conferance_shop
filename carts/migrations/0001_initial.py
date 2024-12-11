# Generated by Django 5.1.4 on 2024-12-11 12:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0002_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=1, default=2.5, max_digits=3, verbose_name='Количество товара')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ключ сессии')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='goods.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
                'db_table': 'cart',
                'ordering': ('user__username', 'created_at'),
            },
        ),
    ]

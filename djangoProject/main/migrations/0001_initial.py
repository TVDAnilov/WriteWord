# Generated by Django 4.1.2 on 2022-10-31 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EngWord', models.CharField(max_length=255, verbose_name='Английское слово')),
                ('RusWordTranslate', models.CharField(default='_', max_length=255, verbose_name='Перевод слова')),
                ('RUSWord_value1', models.CharField(default='_', max_length=255, verbose_name='Вариант перевода №1')),
                ('RUSWord_value2', models.CharField(default='_', max_length=255, verbose_name='Вариант перевода №2')),
                ('RUSWord_value3', models.CharField(default='_', max_length=255, verbose_name='Вариант перевода №3')),
                ('RUSWord_Description1', models.CharField(default='_', max_length=255, verbose_name='Описание и пример №1')),
                ('RUSWord_Description2', models.CharField(default='_', max_length=255, verbose_name='Описание и пример №2')),
                ('RUSWord_Description3', models.CharField(default='_', max_length=255, verbose_name='Описание и пример №3')),
                ('NameText', models.CharField(default='_', max_length=255, verbose_name='Название текста')),
                ('ImKnowThisWord', models.IntegerField(default='0', verbose_name='Знакомое слово')),
                ('CurrentLearn', models.IntegerField(default='0', verbose_name='В очереди на запоминание')),
                ('CounterLearn', models.IntegerField(default='0', verbose_name='Счетчик повторения')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('CountErrLastTry', models.IntegerField(default='0', verbose_name='Кол-во ошибок в прошлый раз')),
                ('CountErrLastTotal', models.IntegerField(default='0', verbose_name='Общее кол-во ошибок')),
                ('WordsNotLearn', models.IntegerField(default='0', verbose_name='Слово не запоминается')),
                ('CountMeets', models.IntegerField(default='0', verbose_name='Частота появления в текстах')),
                ('NumberLearn', models.IntegerField(default='0', verbose_name='Номер урока')),
                ('LearnCheck', models.IntegerField(default='0', verbose_name='Выучено ли слово во время урока')),
                ('DisplayNoneWord', models.IntegerField(default='0', verbose_name='Не показывать слово')),
                ('UserName_WorldOwner', models.CharField(default='_', max_length=255, verbose_name='Имя пользователя')),
                ('UserID_WorldOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Слова',
                'verbose_name_plural': 'Слова',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='InterruptCheckWordKnow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EngWord', models.CharField(max_length=255, verbose_name='Английское слово')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('CountMeets', models.IntegerField(verbose_name='Частота появления в тексте')),
                ('DisplayNoneWord', models.IntegerField(default='0', verbose_name='Не показывать слово')),
                ('UserID_WorldOwner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Не законченный отбор слов',
                'verbose_name_plural': 'Не законченный отбор слов',
                'ordering': ['id'],
            },
        ),
    ]

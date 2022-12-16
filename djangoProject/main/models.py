from django.db import models
from django.urls import reverse


class Words(models.Model):
    EngWord = models.CharField(max_length=255, verbose_name="Английское слово")
    RusWordTranslate = models.CharField(max_length=255, verbose_name="Перевод слова", default='_')
    RUSWord_value1 = models.CharField(max_length=255, verbose_name="Вариант перевода №1", default='_')
    RUSWord_value2 = models.CharField(max_length=255, verbose_name="Вариант перевода №2", default='_')
    RUSWord_value3 = models.CharField(max_length=255, verbose_name="Вариант перевода №3", default='_')
    RUSWord_Description1 = models.CharField(max_length=255, verbose_name="Описание и пример №1", default='_')
    RUSWord_Description2 = models.CharField(max_length=255, verbose_name="Описание и пример №2", default='_')
    RUSWord_Description3 = models.CharField(max_length=255, verbose_name="Описание и пример №3", default='_')
    NameText = models.CharField(max_length=255, verbose_name="Название текста",
                                default='_')  # имя текста, откуда взялось слово
    ImKnowThisWord = models.IntegerField(verbose_name="Знакомое слово", default='0')
    CurrentLearn = models.IntegerField(
        verbose_name="В очереди на запоминание",
        default='0')  # Индикатор того, учим мы слово или оно в сформированной очереди на запоминание
    CounterLearn = models.IntegerField(
        verbose_name="Счетчик повторения", default='0')  # счетчик, сколько раз уже было заучено слово
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    CountErrLastTry = models.IntegerField(verbose_name="Кол-во ошибок в прошлый раз", default='0')
    CountErrLastTotal = models.IntegerField(verbose_name="Общее кол-во ошибок", default='0')
    WordsNotLearn = models.IntegerField(
        verbose_name="Слово не запоминается", default='0')  # Добавлять пометку если постоянно в этом слове ошибка
    CountMeets = models.IntegerField(verbose_name="Частота появления в текстах", default='0')
    NumberLearn = models.IntegerField(verbose_name="Номер урока", default='0')  # на самом деле кол-во уроков.
    LearnCheck = models.IntegerField(verbose_name="Выучено ли слово во время урока",
                                     default='0')  # была ли ошибка в прошлом уроке
    DisplayNoneWord = models.IntegerField(verbose_name="Не показывать слово", default='0')
    UserName_WorldOwner = models.CharField(max_length=255, verbose_name="Имя пользователя", default='_')

    def __str__(self):
        return self.EngWord

    def get_absolute_url(self):
        return reverse('word', kwargs={'word': self.pk})

    class Meta:
        verbose_name = 'Слова'
        verbose_name_plural = 'Слова'
        ordering = ['id']


class InterruptCheckWordKnow(models.Model):
    EngWord = models.CharField(max_length=255, verbose_name="Английское слово")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    CountMeets = models.IntegerField(verbose_name="Частота появления в тексте")
    UserID_WorldOwner = models.CharField(max_length=255, verbose_name="Пользователь", default='_')
    DisplayNoneWord = models.IntegerField(verbose_name="Не показывать слово", default='0')
    NameText = models.CharField(max_length=255, verbose_name="Название текста", default='_')

    def __str__(self):
        return self.EngWord

    def get_absolute_url(self):
        return reverse('word', kwargs={'word': self.pk})

    class Meta:
        verbose_name = 'Не законченный отбор слов'
        verbose_name_plural = 'Не законченный отбор слов'
        ordering = ['id']


class WordGeneralKnow(models.Model):
    EngWord = models.CharField(max_length=255, verbose_name="Английское знакомое слово")

    def __str__(self):
        return self.EngWord

    def get_absolute_url(self):
        return reverse('word', kwargs={'word': self.pk})

    class Meta:
        verbose_name = 'Знакомые всем слова'
        verbose_name_plural = 'Знакомые всем слова'
        ordering = ['id']


class WordGeneralStatistics(models.Model):
    UserName = models.CharField(max_length=255, verbose_name="Имя пользователя", default='_')
    CountErrLastTry = models.IntegerField(verbose_name="Кол-во ошибок в прошлый раз", default='0')
    StartLearn = models.IntegerField(verbose_name="Уроков начато", default='0')
    LearnComplete = models.IntegerField(verbose_name="Уроков закончено", default='0')

    def __str__(self):
        return self.UserName

    def get_absolute_url(self):
        return reverse('word', kwargs={'word': self.pk})

    class Meta:
        verbose_name = 'Общая статистика'
        verbose_name_plural = 'Общая статистика'
        ordering = ['id']

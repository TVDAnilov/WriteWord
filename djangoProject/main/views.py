import re

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.db.models import F
import datetime
from django.utils import timezone

from datetime import datetime, timedelta

import json

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from main.forms import LoginUserForm, RegisterUserForm, AddWordsTextarea
# AddWordKnowwords
from main.lib import clear_text
from main.models import InterruptCheckWordKnow, Words, WordGeneralKnow, WordGeneralStatistics


def index(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        if not WordGeneralStatistics.objects.filter(UserName=str(request.user)).exists():
            statistics_model = WordGeneralStatistics(UserName=str(request.user), StartLearn=0, CountErrLastTry=0,
                                                     LearnComplete=0)
            statistics_model.save()

        statistics = {}
        req_list = Words.objects.filter(UserName_WorldOwner=str(request.user)).filter(ImKnowThisWord=0)

        learn_words_stat = Words.objects.filter(UserName_WorldOwner=str(request.user)).filter(NumberLearn__gt=0).filter(
            WordsNotLearn=0).count()  # Выучено слов
    word_written = 0  # Записано слов
    statistic_usr = WordGeneralStatistics.objects.filter(UserName=str(request.user))  # Уроков закончено
    learn_complete = 0  # Уроков закончено
    Words_add = 0  # Добавлено незнакомых слов
    Words_add_know = Words.objects.filter(UserName_WorldOwner=str(request.user)).filter(
        ImKnowThisWord=1).count()  # добавлено знакомых слов
    Errors_last_time = 0  # Ошибок в последний раз
    Errors_total = 0  # Ошибок совершено
    Errors_most = 0  # Самая частая ошибка
    Text_add_count = 0  # Текстов добавлено
    learn_start = 0  # Уроков начато
    name_text = []

    for key in statistic_usr:
        learn_complete = key.LearnComplete
        Errors_last_time = key.CountErrLastTry
        learn_start = key.StartLearn

    for key in req_list:
        word_written = word_written + key.CounterLearn
        Errors_total = Errors_total + key.CountErrLastTotal
        Errors_most_tmp = key.CountErrLastTotal
        Words_add = Words_add + 1

        if Errors_most < Errors_most_tmp:
            Errors_most = Errors_most_tmp

        name_text.append(key.NameText)
    if Errors_most != 0:
        Errors_most = Words.objects.filter(UserName_WorldOwner=str(request.user)).filter(
            CountErrLastTotal=Errors_most).filter(ImKnowThisWord=0).first()
        if Errors_most is not None:
            Errors_most = Errors_most.EngWord
        else:
            Errors_most = 0

    name_text = list(set(name_text))
    Text_add_count = len(name_text)

    statistics['learn_words_stat'] = learn_words_stat
    statistics['word_written'] = word_written
    statistics['Errors_total'] = Errors_total
    statistics['learn_complete'] = learn_complete
    statistics['Errors_last_time'] = Errors_last_time
    if Errors_most == 0:
        statistics['Errors_most'] = "Ошибок нет"
    else:
        statistics['Errors_most'] = Errors_most
    statistics['learn_start'] = learn_start
    statistics['Text_add_count'] = Text_add_count
    statistics['Words_add'] = Words_add
    statistics['Words_add_know'] = Words_add_know

    return render(request, 'main/index.html', {'statistics': statistics})


def learn_words(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/Learn_words.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('logon')

    def get_user_context(self, **kwargs):
        context = kwargs
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/logon.html'

    def get_user_context(self, **kwargs):
        context = kwargs
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        logout(request)
        return redirect('logon')


def add_word_textarea(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        if request.method == 'POST':
            form = AddWordsTextarea(request.POST)
            if form.is_valid():
                words = clear_text(form.cleaned_data['Text'])
                words_know = WordGeneralKnow.objects.all()
                words_InterruptCheckWordKnow = InterruptCheckWordKnow.objects.filter(
                    UserID_WorldOwner=str(request.user))
                duplicate = Words.objects.filter(UserName_WorldOwner=str(request.user))
                for word in words:
                    dubl_bool = 0
                    for word_k in words_know:
                        if str(word_k).strip() == str(word.get('word')).strip():
                            dubl_bool = 1
                            # print("слово ", str(word.get('word')).strip(), "уже в списке Know")
                    if dubl_bool > 0:
                        continue

                    for dubl in duplicate:
                        if str(dubl).strip() == str(word.get('word')).strip():
                            dubl_bool = 1
                            # print("слово ", str(word.get('word')).strip(), "уже добавлено ранее")

                    if dubl_bool > 0:
                        continue

                    for word_irq in words_InterruptCheckWordKnow:
                        if str(word_irq).strip() == str(word.get('word')).strip():
                            dubl_bool = 1
                            # print("слово уже в очереди на добавление")

                    if dubl_bool > 0:
                        continue

                    if dubl_bool == 0:
                        word_bd = InterruptCheckWordKnow(EngWord=word.get('word'), CountMeets=word.get('CountMeets'),
                                                         UserID_WorldOwner=request.user,
                                                         NameText=form.cleaned_data['NameText'])
                        word_bd.save()
                words_obj = InterruptCheckWordKnow.objects.filter(UserID_WorldOwner=str(request.user)).count()
                if words_obj > 0:
                    return redirect('AddWords_Know')
                else:
                    return redirect('home')
        else:
            form = AddWordsTextarea()
            check_interrupt_add_words = InterruptCheckWordKnow.objects.filter(
                UserID_WorldOwner=str(request.user)).count()

    return render(request, 'main/AddWords.html', {'form': form, 'check_interrupt_add_words': check_interrupt_add_words})


def add_words_know(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        if request.method == 'POST':
            form_word_know = request.POST

            words = InterruptCheckWordKnow.objects.filter(UserID_WorldOwner=str(request.user))
            res = []
            for word in words:
                for know_word in form_word_know:
                    word = str(word).strip()
                    know_word = str(know_word).strip()
                    if word == know_word:
                        res.append(word)
                        break
            for word_know in res:
                words = InterruptCheckWordKnow.objects.filter(EngWord=word_know).filter(
                    UserID_WorldOwner=str(request.user)).first()
                word = Words(EngWord=words.EngWord, NameText=words.NameText, ImKnowThisWord=1,
                             CountMeets=words.CountMeets,
                             UserName_WorldOwner=words.UserID_WorldOwner, DisplayNoneWord=words.DisplayNoneWord)
                word.save()
                words.delete()
            if 'pass' in request.POST:
                return redirect('home')
            words_obj = InterruptCheckWordKnow.objects.filter(UserID_WorldOwner=str(request.user)).count()
            if words_obj > 0:
                return redirect('Translate')
            else:
                return redirect('home')
        else:
            words = InterruptCheckWordKnow.objects.filter(UserID_WorldOwner=str(request.user)).order_by('EngWord')
            if words.count() == 0:
                return redirect('home')
            else:
                return render(request, 'main/AddWordsKnow.html', {'words': words})


def translate(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        if request.method == 'POST':
            form = request.POST
            rus_words_tmp = re.split('\r |\n |\r\n', form['rusWord'])
            rus_words = []
            for i in rus_words_tmp:
                rus_words.append(i.strip())
            eng_words = re.split(r"\W", form['engWord'])
            eng_words = list(filter(len, eng_words))
            rus_words = list(filter(len, rus_words))
            if len(rus_words) == len(eng_words):
                for i, engW in enumerate(eng_words):
                    if engW != "":
                        if InterruptCheckWordKnow.objects.filter(EngWord=engW).filter(
                                UserID_WorldOwner=str(request.user)).exists():
                            word_translate = InterruptCheckWordKnow.objects.filter(EngWord=engW).filter(
                                UserID_WorldOwner=str(request.user)).first()
                            word = Words(
                                EngWord=word_translate.EngWord,
                                RUSWord_value1=rus_words[i],
                                NameText=word_translate.NameText,
                                ImKnowThisWord=0,
                                CountMeets=word_translate.CountMeets,
                                UserName_WorldOwner=word_translate.UserID_WorldOwner
                            )
                            word.save()
                            word_translate.delete()
            return redirect('home')
        else:
            words_obj = InterruptCheckWordKnow.objects.filter(UserID_WorldOwner=str(request.user))
            words = []
            for i, word in enumerate(words_obj, start=0):
                words.append(word.EngWord.strip() + "\n")
            return render(request, 'main/translate.html', {'words': words})


def know(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        if request.method == 'POST':
            form = request.POST
            words = re.split(r"\W", form['engWord'])
            words = list(filter(len, words))
            for word in words:
                know_word = WordGeneralKnow(EngWord=word)
                know_word.save()
            return render(request, 'main/know.html')
        else:
            return render(request, 'main/know.html')


def getNewWord(user):
    countWord = 8
    words = []
    words_1 = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        NumberLearn=0).order_by('-CountMeets')[:countWord]

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))

    return words


def LearnNewWords(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/LearnNewWords.html')


def LearnNewWords_get_json_err_words(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = getNewWord(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def Words_push_json_err_words(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        if request.method == 'POST':
            user = request.user
            json_data = request.POST
            data = {}
            statisticErr = 0
            for key in json_data:
                data = key
            data = json.loads(data)
            if data.get("no_err", "not_key") == "not_key":
                pass
                # print("Нет ключа no_err")
            else:
                for key in data:
                    if Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user)).exists():
                        # print("В БД есть:", key)
                        if data[key][0] == "0":
                            Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user)).update(
                                CurrentLearn=0,
                                LearnCheck="1",
                                CountErrLastTry=
                                data[key][0],
                                NumberLearn=F(
                                    "NumberLearn") + 1,
                                CounterLearn=F(
                                    "CounterLearn") +
                                             data[
                                                 key][
                                                 1],
                                time_update=datetime.now())
                        else:
                            Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user)).update(
                                CurrentLearn=0,
                                CountErrLastTry=
                                data[key][0],
                                LearnCheck="0",
                                NumberLearn=F(
                                    "NumberLearn") + 1,
                                CounterLearn=F(
                                    "CounterLearn") +
                                             data[
                                                 key][
                                                 1],
                                CountErrLastTotal=F(
                                    "CountErrLastTotal") +
                                                  data[
                                                      key][
                                                      0],
                                time_update=datetime.now())
                            statisticErr += int(data[key][0])

                    w = Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user))
                    for i in w:
                        if i.CountErrLastTotal > 0:

                            if float(i.NumberLearn) / float(i.CountErrLastTotal) > 1:  # слово учится или нет.
                                Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user)).update(
                                    WordsNotLearn=0, time_update=datetime.now())  # слово запоминается
                            else:
                                Words.objects.filter(EngWord=key).filter(UserName_WorldOwner=str(user)).update(
                                    WordsNotLearn=1,
                                    time_update=datetime.now())  # никак, нужно еще раз повторять в дальнейшем

                WordGeneralStatistics.objects.filter(UserName=str(user)).update(CountErrLastTry=statisticErr,
                                                                                LearnComplete=F('LearnComplete') + 1)

        return JsonResponse({'words': 'OK'})


def Words_push_json_new_tranclate(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        if request.method == 'POST':
            user = str(request.user)
            json_data = request.POST
            data = {}
            for key in json_data:
                data = key
            data = json.loads(data)
            for key in data:
                new_translate_str = str(data[key]).strip()[0:35]  # 35 символов макс
                if Words.objects.filter(UserName_WorldOwner=user).filter(EngWord=key).exists():
                    Words.objects.filter(UserName_WorldOwner=user).filter(EngWord=key).update(
                        RUSWord_value1=new_translate_str, time_update=datetime.now())
    return JsonResponse({'words': 'OK'})


def RepetitionPreviousWords(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/RepetitionPreviousWords.html')


def getRepetitionWord(user):
    countWord = 8
    words = []
    words_1 = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        NumberLearn__gte=1).order_by('-time_update')[:countWord]
    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def RepetitionPreviousWords_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = getRepetitionWord(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def work_on_err(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/work_on_err.html')


def get_word_on_err(user):
    countWord = 8
    words_1 = []
    words = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        CountErrLastTotal__gt=0).order_by(
        '-CountErrLastTotal')[:countWord]

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def Work_on_Err_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = get_word_on_err(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def get_Popular_words_with_errors(user):
    countWord = 8
    words_1 = []
    words = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        CountErrLastTotal__gt=0).filter(CountErrLastTry__gt=0).order_by('-CountMeets')[:countWord]

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def Popular_words_with_errors_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = get_Popular_words_with_errors(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def Popular_words_with_errors(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/Popular_words_with_errors.html')


def Words_not_remembered_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = get_Words_not_remembered(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def Words_not_remembered(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/Words_not_remembered.html')


def get_Words_not_remembered(user):
    countWord = 8
    words_1 = []
    words = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        WordsNotLearn=1).order_by('-CountMeets')[:countWord]

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def get_learned_words_with_random(user):
    countWord = 20
    words_1 = []
    words = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
        NumberLearn__gt=0).order_by('?')[:countWord]

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def learned_words_with_random(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/learned_words_with_random.html')


def learned_words_with_random_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = get_learned_words_with_random(request.user)
        WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def Words_from_text(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        all_note = Words.objects.filter(UserName_WorldOwner=str(request.user))
        name_text = []
        for text in all_note:
            name_text.append(text.NameText)

        name_text = list(set(name_text))

        if len(name_text) == 0:
            return redirect('home')
        else:
            return render(request, 'main/Words_from_text.html', {'texts': name_text})


def word_from_the_text(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/word_from_the_text_learn.html')


def get_word_from_the_text_learn(user, name_text):
    words_1 = []
    words = []
    if Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(NameText=name_text).exists():
        words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
            NameText=name_text).order_by('-CountMeets')[:50]

        for word in words_1:
            words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def word_from_the_text_learn_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        # Проверить, есть ли такое поле
        name_text = request.GET.get('name_text', "no_text")
        if name_text == "no_text":
            return JsonResponse('{}')
        words = []
        if len(name_text) != 0:
            words = get_word_from_the_text_learn(request.user, name_text)
            WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def Repeat_by_date(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        all_date = Words.objects.filter(UserName_WorldOwner=str(request.user))
        date_list = []
        for date in all_date:
            if date.time_update == date.time_create:
                continue
            date_list.append(str(date.time_update.date()))

        date_list = list(set(date_list))
        if len(date_list) == 0:
            return redirect('home')
        else:
            return render(request, 'main/Repeat_by_date.html', {'date_list': date_list})


def Repeat_by_the_date(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/Repeat_by_the_date.html')


def get_Repeat_by_the_date(user, date):
    words_1 = []
    words = []
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    date_time_obj_one_day = date_time_obj + timedelta(days=1)

    if Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
            time_update__gt=date_time_obj).filter(time_update__lt=date_time_obj_one_day).exists():
        words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(ImKnowThisWord=0).filter(
            time_update__gt=date_time_obj).filter(time_update__lt=date_time_obj_one_day).order_by('-CountMeets')[:50]
        for word in words_1:
            words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def Repeat_by_the_date_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        date = request.GET.get('date', "no_date")
        if date == "no_date":
            return JsonResponse('{}')
        words = []
        if len(date) != 0:
            words = get_Repeat_by_the_date(request.user, date)
            WordGeneralStatistics.objects.filter(UserName=str(request.user)).update(StartLearn=F("StartLearn") + 1)
        return JsonResponse({'words': words})


def words_learned(request):
    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        return render(request, 'main/words_learned_statistic.html')


def get_words_learned(user):
    words = []
    words_1 = []

    words_1 = Words.objects.filter(UserName_WorldOwner=str(user)).filter(NumberLearn__gt=0).filter(WordsNotLearn=0)

    for word in words_1:
        words.append(dict(engword=word.EngWord, rusword=word.RUSWord_value1, CountMeets=word.CountMeets))
    return words


def words_learned_get_json(request):
    if not request.user.is_authenticated:
        return JsonResponse('{}')
    else:
        words = get_words_learned(request.user)
        return JsonResponse({'words': words})

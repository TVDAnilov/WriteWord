from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('AddWords', add_word_textarea, name='AddWords'),
    path('Learn_words', views.learn_words, name='Learn_words'),
    path('regiseter', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('logon', LoginUser.as_view(), name='logon'),
    path('AddWordsKnow', add_words_know, name='AddWords_Know'),
    path('Translate', translate, name='Translate'),
    path('Know', know, name='Know'),
    path('word_from_the_text', word_from_the_text, name='word_from_the_text'),
    path('Words_push_json_new_tranclate', Words_push_json_new_tranclate, name='Words_push_json_new_tranclate'),
    path('word_from_the_text_learn_get_json', word_from_the_text_learn_get_json, name='word_from_the_text_learn_get_json'),
    path('LearnNewWords', LearnNewWords, name='LearnNewWords'),
    path('Repeat_by_date', Repeat_by_date, name='Repeat_by_date'),
    path('Repeat_by_the_date', Repeat_by_the_date, name='Repeat_by_the_date'),
    path('Repeat_by_the_date_get_json', Repeat_by_the_date_get_json, name='Repeat_by_the_date_get_json'),
    path('Words_from_text', Words_from_text, name='Words_from_text'),
    path('Words_not_remembered', Words_not_remembered, name='Words_not_remembered'),
    path('learned_words_with_random', learned_words_with_random, name='learned_words_with_random'),
    path('learned_words_with_random_get_json', learned_words_with_random_get_json, name='learned_words_with_random_get_json'),
    path('Words_not_remembered_get_json', Words_not_remembered_get_json, name='Words_not_remembered_get_json'),
    path('Popular_words_with_errors', Popular_words_with_errors, name='Popular_words_with_errors'),
    path('Popular_words_with_errors_get_json', Popular_words_with_errors_get_json, name='Popular_words_with_errors_get_json'),
    path('Work_on_Err_get_json', Work_on_Err_get_json, name='Work_on_Err_get_json'),
    path('work_on_err', work_on_err, name='work_on_err'),
    path('LearnNewWords_get_json_err_words', LearnNewWords_get_json_err_words, name='LearnNewWords_get_json_err_words'),
    path('RepetitionPreviousWords', RepetitionPreviousWords, name='RepetitionPreviousWords'),
    path('RepetitionPreviousWords_get_json', RepetitionPreviousWords_get_json, name='RepetitionPreviousWords_get_json'),
    path('Words_push_json_err_words', Words_push_json_err_words,
         name='Words_push_json_err_words'),

]

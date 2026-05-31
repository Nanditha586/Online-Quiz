from django.urls import path
from . import views

urlpatterns = [

    path(
        'quiz-list/',
        views.quiz_list,
        name='quiz_list'
    ),

    path(
        'start-quiz/<int:quiz_id>/',
        views.start_quiz,
        name='start_quiz'
    ),

    path(
        'submit-quiz/<int:quiz_id>/',
        views.submit_quiz,
        name='submit_quiz'
    ),

    path(
        'leaderboard/',
        views.leaderboard,
        name='leaderboard'
    ),

    path(
        'dashboard/',
        views.user_dashboard,
        name='user_dashboard'
    ),

    path(
        'save-answer/',
        views.save_answer,
        name='save_answer'
    ),

    path(
        'analytics/',
        views.analytics_dashboard,
        name='analytics_dashboard'
    ),

    path(
        'export-csv/',
        views.export_results_csv,
        name='export_results_csv'
    ),

    path(
        'upload-questions/',
        views.upload_questions,
        name='upload_questions'
    ),
    path(
    'my-quizzes/',
    views.my_quizzes,
    name='my_quizzes'
),

path(
    'quiz-questions/<int:quiz_id>/',
    views.quiz_questions,
    name='quiz_questions'
),
   path(
        'edit-question/<int:question_id>/',
        views.edit_question,
        name='edit_question'
    ),

    path(
        'delete-question/<int:question_id>/',
        views.delete_question,
        name='delete_question'
    ),
]
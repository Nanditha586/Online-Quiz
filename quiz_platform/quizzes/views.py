from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Result, StudentProfile, UserRole
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserAnswer
from django.db.models import Avg
from django.http import HttpResponse
import csv
import io
from .models import UserRole
from django.contrib.auth.models import User
import pandas as pd
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

@login_required
def quiz_list(request):

    role = UserRole.objects.filter(
        user=request.user
    ).first()

    if role and role.role == 'staff':

        quizzes = Quiz.objects.all()

    else:

        profile = StudentProfile.objects.get(
            user=request.user
        )

        quizzes = Quiz.objects.filter(
            year=profile.year,
            branch=profile.branch
        )

    attempted_quiz_ids = Result.objects.filter(
        user=request.user
    ).values_list(
        'quiz_id',
        flat=True
    )

    paginator = Paginator(quizzes,2)

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'quiz_list.html',
        {
            'quizzes': page_obj,
            'page_obj': page_obj,
            'attempted_quiz_ids':attempted_quiz_ids,
            'user_role': role
        }
    )

@login_required
def start_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    # ❌ If already attempted → block access
    already_attempted = Result.objects.filter(
        user=request.user,
        quiz=quiz
    ).exists()

    if already_attempted:
        return render(
            request,
            'result.html',
            {
                'quiz': quiz,
                'score': None,
                'message': "You have already attempted this quiz."
            }
        )

    questions = Question.objects.filter(quiz=quiz)

    return render(
        request,
        'start_quiz.html',
        {
            'quiz': quiz,
            'questions': questions
        }
    )
@login_required
def submit_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    questions = Question.objects.filter(quiz=quiz)

    score = 0
    correct_answers = 0
    wrong_answers = 0
    attempted_questions = 0

    user_answers = UserAnswer.objects.filter(
        user=request.user,
        quiz=quiz
    )

    # convert to dictionary for FAST lookup
    answer_map = {
        ua.question_id: ua.selected_answer
        for ua in user_answers
    }

    for question in questions:

        selected_answer = answer_map.get(question.id)

        # ❌ not attempted
        if not selected_answer:
            continue

        attempted_questions += 1

        # ✅ correct
        if selected_answer == question.correct_answer:
            score += question.marks
            correct_answers += 1

        # ❌ wrong
        else:
            score -= question.negative_marks
            wrong_answers += 1

    # prevent negative score
    if score < 0:
        score = 0

    # save result
    Result.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total_questions=questions.count(),
        correct_answers=correct_answers,
        wrong_answers=wrong_answers
    )

    # clear answers AFTER submission
    UserAnswer.objects.filter(
        user=request.user,
        quiz=quiz
    ).delete()
    user_role = UserRole.objects.filter(
        user=request.user
        ).first()
    return render(
        request,
        'result.html',
        {
            'quiz': quiz,
            'score': score,
            'total_questions': questions.count(),
            'attempted_questions': attempted_questions,
            'correct_answers': correct_answers,
            'wrong_answers': wrong_answers,
            'user_role': user_role
        }
    )



@login_required
def leaderboard(request):

    leaderboard_data = Result.objects.exclude(
        user__userrole__role='staff'
    ).order_by('-score')

    user_role = UserRole.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        'leaderboard.html',
        {
            'leaderboard_data': leaderboard_data,
            'user_role': user_role
        }
    )
@login_required
def user_dashboard(request):

    results = Result.objects.filter(
        user=request.user
    ).order_by('-submitted_at')

    total_quizzes = results.count()

    highest_score = 0

    if results.exists():

        highest_score = results.aggregate(
            Max('score')
        )['score__max']

    return render(
        request,
        'user_dashboard.html',
        {
            'results': results,
            'total_quizzes': total_quizzes,
            'highest_score': highest_score
        }
    )
def save_answer(request):
    if request.method == "POST":

        question_id = request.POST.get("question_id")
        selected = request.POST.get("selected_answer")
        quiz_id = request.POST.get("quiz_id")

        question = Question.objects.get(id=question_id)
        quiz = Quiz.objects.get(id=quiz_id)

        UserAnswer.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            question=question,
            defaults={"selected_answer": selected}
        )

        return JsonResponse({"status": "saved"})

def staff_only(view_func):

    def wrapper(request, *args, **kwargs):

        role = UserRole.objects.filter(
            user=request.user
        ).first()

        if not role:
            return HttpResponseForbidden(
            "No role assigned."
        )

        if role.role != 'staff':
            return HttpResponseForbidden(
                "Only Staff Can Access This Page"
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper



@login_required
@staff_only
def analytics_dashboard(request):

    # Student users only
    total_users = UserRole.objects.filter(
        role='student'
    ).count()

    # Student results only
    student_results = Result.objects.filter(
        user__userrole__role='student'
    )

    total_quizzes = Quiz.objects.count()

    total_attempts = student_results.count()

    average_score = student_results.aggregate(
        Avg('score')
    )['score__avg'] or 0

    top_results = student_results.select_related(
        'user',
        'quiz'
    ).order_by(
        '-score'
    )[:10]

    quizzes = Quiz.objects.all()

    quiz_labels = []
    quiz_scores = []

    for quiz in quizzes:

        avg_score = Result.objects.filter(
            quiz=quiz,
            user__userrole__role='student'
        ).aggregate(
            Avg('score')
        )['score__avg'] or 0

        quiz_labels.append(
            quiz.title
        )

        quiz_scores.append(
            float(avg_score)
        )

    context = {

        'total_quizzes': total_quizzes,

        'total_users': total_users,

        'total_attempts': total_attempts,

        'average_score': round(
            average_score,
            2
        ),

        'top_results': top_results,

        'quiz_labels': quiz_labels,

        'quiz_scores': quiz_scores

    }

    return render(
        request,
        'analytics_dashboard.html',
        context
    )

@login_required
def export_results_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="quiz_results.csv"'

    writer = csv.writer(response)

    writer.writerow([

        'Username',
        'Quiz',
        'Score',
        'Correct Answers',
        'Wrong Answers',
        'Submitted At'

    ])

    results = Result.objects.all()

    for result in results:

        writer.writerow([

            result.user.username,
            result.quiz.title,
            result.score,
            result.correct_answers,
            result.wrong_answers,
            result.submitted_at

        ])

    return response



@staff_only
@login_required
def upload_questions(request):

    if request.method == 'POST':

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):

            return HttpResponse(
                'File must be CSV'
            )

        quiz_title = request.POST.get(
            'quiz_title'
        )
        description=request.POST.get('description')
        duration=request.POST.get('duration') 
        year = request.POST.get(
            'year'
        )

        branch = request.POST.get(
            'branch'
        )
       


        quiz, created = Quiz.objects.get_or_create(

            title=quiz_title,

            year=year,

            branch=branch,

            defaults={

                'description': description,
                'duration': duration,
                'created_by': request.user
            }
        )

        data = pd.read_csv(csv_file)

        for _, row in data.iterrows():

            Question.objects.create(

                quiz=quiz,

                question=row['question'],

                option1=row['option1'],

                option2=row['option2'],

                option3=row['option3'],

                option4=row['option4'],

                correct_answer=row[
                    'correct_answer'
                ],

                marks=row['marks'],

                negative_marks=row[
                    'negative_marks'
                ]
            )

        return HttpResponse(
            'Questions Uploaded Successfully'
        )

    return render(
        request,
        'upload_questions.html'
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Quiz


@login_required
def my_quizzes(request):

    quizzes = Quiz.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_quizzes.html',
        {
            'quizzes': quizzes
        }
    )
from django.shortcuts import get_object_or_404
from .models import Quiz, Question

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
@staff_only
@login_required
def quiz_questions(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        created_by=request.user
    )

    questions_list = Question.objects.filter(
        quiz=quiz
    ).order_by('id')

    paginator = Paginator(
        questions_list,
        10
    )  # 10 questions per page

    page_number = request.GET.get('page')

    questions = paginator.get_page(
        page_number
    )

    return render(
        request,
        'quiz_questions.html',
        {
            'quiz': quiz,
            'questions': questions
        }
    )
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question

@login_required
@staff_only
def edit_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if request.method == 'POST':

        question.question = request.POST.get('question')
        question.option1 = request.POST.get('option1')
        question.option2 = request.POST.get('option2')
        question.option3 = request.POST.get('option3')
        question.option4 = request.POST.get('option4')
        question.correct_answer = request.POST.get('correct_answer')
        question.marks = request.POST.get('marks')
        question.negative_marks = request.POST.get('negative_marks')

        # IMPORTANT
        question.save()

        return redirect(
            'quiz_questions',
            quiz_id=question.quiz.id
        )

    return render(
        request,
        'edit_question.html',
        {
            'question': question
        }
    )
@login_required
def delete_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id,
        quiz__created_by=request.user
    )

    quiz_id = question.quiz.id

    question.delete()

    return redirect(
        'quiz_questions',
        quiz_id=quiz_id
    )
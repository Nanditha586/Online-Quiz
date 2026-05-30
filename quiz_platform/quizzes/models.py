from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    duration = models.IntegerField(
        help_text="Duration in minutes"
    )

    year = models.CharField(
        max_length=10,
        default='1'
    )

    branch = models.CharField(
        max_length=50,
        default='CSE'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    option1 = models.CharField(max_length=200)

    option2 = models.CharField(max_length=200)

    option3 = models.CharField(max_length=200)

    option4 = models.CharField(max_length=200)

    correct_answer = models.CharField(max_length=200)

    marks = models.IntegerField(default=1)

    negative_marks = models.FloatField(default=0)

    def __str__(self):
        return self.question
class Result(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )

    score = models.FloatField()

    total_questions = models.IntegerField()

    correct_answers = models.IntegerField()

    wrong_answers = models.IntegerField()

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
class UserAnswer(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_answer = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    answered_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    

    def __str__(self):
        return self.user.username


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username
class UserRole(models.Model):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
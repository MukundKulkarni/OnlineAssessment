from django.db import models
from django.db import AbstractUser
from django.utils.html import escape, mark_safe

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

class Exam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    exams = models.ManyToManyField(Exam, through='TakenExam')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, exam):
        answered_questions = self.exam_answers \
            .filter(answer__question__exam=exam) \
            .values_list('answer__question__pk', flat=True)
        questions = exam.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_exams')
    quiz = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='taken_exams')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

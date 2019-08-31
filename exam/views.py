from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy


from .models import User, Student, Exam
from .forms import StudentSignUpForm, StudentInterestsForm, TeacherSignUpForm
from .decorators import student_required, teacher_required

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    #if request.user.is_authenticated:
        #if request.user.is_teacher:
            #return redirect('teachers:quiz_change_list')
        #else:
            #return redirect('students:quiz_list')
    return render(request, 'exam/home.html')

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'exam/students/interests_form.html'
    #success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)

@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Exam
    ordering = ('name', )
    context_object_name = 'exams'
    template_name = 'exam/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_exams = student.exams.values_list('pk', flat=True)
        queryset = Exam.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_exams) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:quiz_change_list')

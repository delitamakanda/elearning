from django import forms
from django.contrib import messages
from django.core.mail import mail_admins
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms.models import modelform_factory
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from students.decorators import teacher_required
from students.forms import BaseAnswerInlineFormSet
from students.forms import QuestionForm
from students.forms import TeacherSignupForm
from students.models import Answer
from students.models import Question
from students.models import Quiz
from students.models import User

from courses.badges import possibly_award_badge

class TeacherRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = TeacherSignupForm
    success_url = reverse_lazy('students:teacher_quiz_change_list')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        result = super(TeacherRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        user.profile.get_award_points(3)
        possibly_award_badge("teacher_signup", user=user)
        mail_admins("{} is sign up ".format(user.username), "check your admin on myelearning")
        login(self.request, user)
        return result

    def form_invalid(self, form):
        result = super(TeacherRegistrationView, self).form_invalid(form)
        return result


@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherQuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'students/teacher/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes.select_related('tags').annotate(questions_count=Count('questions', distinct=True)).annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    # fields = ('name', 'tags',)
    form_class = modelform_factory(Quiz, exclude=['owner'], widgets={"name": forms.TextInput(attrs={'class':'form-control'}) })
    template_name = 'students/teacher/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'Quiz created with sucess! Next add some questions.')
        return redirect('students:teacher_update_quiz', quiz.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    # fields = ('name', 'tags', )
    form_class = modelform_factory(Quiz, exclude=['owner'], widgets={"name": forms.TextInput(attrs={'class':'form-control'}) })
    context_object_name = 'quiz'
    template_name = 'students/teacher/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('students:teacher_update_quiz', kwargs={'pk': self.object.pk})

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'students/teacher/quiz_delete_confirm.html'
    success_url = reverse_lazy('students:teacher_quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'students/teacher/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@login_required
@teacher_required
def question_add(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('students:teacher_change_question', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'students/teacher/question_add_form.html', {'quiz': quiz, 'form': form})

@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)
    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        formset = BaseAnswerInlineFormSet,
        fields = ('text', 'is_correct'),
        min_num = 2,
        validate_min = True,
        max_num = 10,
        validate_max = True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('students:teacher_update_quiz', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'students/teacher/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'students/teacher/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('students:teacher_update_quiz', kwargs={'pk': question.quiz_id})

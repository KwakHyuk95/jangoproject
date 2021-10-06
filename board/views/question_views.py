from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Answer, Comment
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='common:login')
def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # request.user : 현재 로그인한 계정의
                                           #                User모델 객체.
            question.create_date = timezone.now()
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    return render(request, 'board/question_form.html', {'form': form})

def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'board/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 질문을 한 사람과 글을 작성한 사람이 같은지를 확인.
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from django.utils import timezone

from .models import BatchExam, PersonalExamResult
from .forms import BatchExamForm, PersonalExamResultForm


class ExamListView(LoginRequiredMixin, ListView):
    model = BatchExam
    template_name = 'exams/list.html'
    context_object_name = 'batch_exams'

    def get_queryset(self):
        user = self.request.user
        if user.batch:
            return BatchExam.objects.filter(batch=user.batch).order_by('exam_date')
        return BatchExam.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()

        batch_exams = context['batch_exams']

        # Build exam dates JSON for calendar
        exam_dates = []
        for exam in batch_exams:
            exam_dates.append({
                'id': exam.id,
                'date': exam.exam_date.isoformat(),
                'subject': exam.subject,
                'name': exam.exam_name,
                'type': exam.exam_type,
            })
        context['exam_dates_json'] = json.dumps(exam_dates)

        # Get user's personal results for linking
        # personal_results: {batch_exam_id: result_object}
        # personal_scores: {batch_exam_id: score_string} — used directly in template
        results = {
            r.batch_exam_id: r
            for r in PersonalExamResult.objects.filter(student=user)
        }
        context['personal_results'] = results
        # String-keyed for Django template dict lookup (template uses exam.pk which is int,
        # but Django template engine coerces to string for dict lookup)
        context['personal_scores'] = {str(k): v.score for k, v in results.items()}

        # Mark past vs upcoming and compute days_until
        next_exam = None
        for exam in batch_exams:
            exam.is_past = exam.exam_date < today
            exam.days_until = (exam.exam_date - today).days
            if not exam.is_past and next_exam is None:
                next_exam = exam

        context['today'] = today
        context['next_exam'] = next_exam

        return context


class BatchExamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """CR-only: add a batch exam."""
    model = BatchExam
    form_class = BatchExamForm
    template_name = 'exams/form.html'
    success_url = reverse_lazy('exam_list')

    def test_func(self):
        return self.request.user.is_cr

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.batch = self.request.user.batch
        return super().form_valid(form)


class PersonalResultCreateView(LoginRequiredMixin, View):
    """AJAX: Student adds their result for a batch exam."""

    def post(self, request, pk):
        # Ensure the exam belongs to the user's batch (prevents cross-batch data entry)
        user_batch = request.user.batch
        if not user_batch:
            return JsonResponse({'error': 'You are not assigned to a batch'}, status=403)

        batch_exam = get_object_or_404(BatchExam, pk=pk, batch=user_batch)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Guard against JSON null values crashing .strip()
        raw_score = data.get('score') or ''
        raw_notes = data.get('notes') or ''
        score = str(raw_score).strip()
        notes = str(raw_notes).strip()

        result, created = PersonalExamResult.objects.update_or_create(
            student=request.user,
            batch_exam=batch_exam,
            defaults={'score': score, 'notes': notes},
        )

        return JsonResponse({
            'score': result.score,
            'notes': result.notes,
            'created': created,
        })



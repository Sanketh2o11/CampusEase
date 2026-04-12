import json
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.views import View

from core.mixins import CRRequiredMixin
from django.utils import timezone
from django.db.models import F

from .models import Material, MaterialThankYou
from .forms import MaterialForm
from exams.models import BatchExam


class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = 'materials/list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return Material.objects.all().select_related('uploader').order_by('subject', '-thank_you_count', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get materials the user has already thanked
        thanked_ids = set(
            MaterialThankYou.objects.filter(student=user).values_list('material_id', flat=True)
        )
        context['thanked_ids'] = thanked_ids

        # Exam mode banner: check if any batch exam within 2 days
        if user.batch:
            today = timezone.now().date()
            upcoming_exams = BatchExam.objects.filter(
                batch=user.batch,
                exam_date__gte=today,
                exam_date__lte=today + timedelta(days=2),
            ).order_by('exam_date')

            if upcoming_exams.exists():
                exam = upcoming_exams.first()
                days_until = (exam.exam_date - today).days
                context['exam_alert'] = {
                    'subject': exam.subject,
                    'exam_name': exam.exam_name,
                    'days_until': days_until,
                }
                # Top 3 most thanked materials for this subject
                context['exam_top_materials'] = Material.objects.filter(
                    subject__iexact=exam.subject
                ).order_by('-thank_you_count')[:3]

        return context


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/form.html'
    success_url = reverse_lazy('material_list')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class MaterialDeleteView(LoginRequiredMixin, CRRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('material_list')


class MaterialPinToggleView(LoginRequiredMixin, CRRequiredMixin, View):
    def post(self, request, pk):
        material = get_object_or_404(Material, pk=pk)
        material.is_pinned = not material.is_pinned
        material.save()
        return redirect('material_list')


@login_required
@require_POST
def material_thankyou(request, pk):
    """AJAX endpoint: POST /materials/<id>/thankyou/ — thank a material uploader."""
    material = get_object_or_404(Material, pk=pk)

    _, created = MaterialThankYou.objects.get_or_create(
        material=material,
        student=request.user,
    )

    if created:
        # Use F() expression to avoid race condition on concurrent increments
        Material.objects.filter(pk=material.pk).update(
            thank_you_count=F('thank_you_count') + 1
        )
        material.refresh_from_db(fields=['thank_you_count'])

    return JsonResponse({
        'count': material.thank_you_count,
        'already_thanked': not created,
    })

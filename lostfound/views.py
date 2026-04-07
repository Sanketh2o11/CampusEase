import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, View
from django.contrib import messages

from .models import LostFoundItem
from .forms import LostFoundItemForm


class LostFoundListView(LoginRequiredMixin, ListView):
    model = LostFoundItem
    template_name = 'lostfound/list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return LostFoundItem.objects.all().select_related('reporter', 'claimed_by').order_by('-created_at')


class LostFoundCreateView(LoginRequiredMixin, CreateView):
    model = LostFoundItem
    form_class = LostFoundItemForm
    template_name = 'lostfound/list.html'
    success_url = reverse_lazy('lostfound_list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class LostFoundIndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = LostFoundListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LostFoundItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.reporter = request.user
            item.save()
            messages.success(request, f'"{item.title}" has been reported.')
            return redirect('lostfound_list')
        # Re-render list with form errors in context
        items = LostFoundItem.objects.all().select_related('reporter', 'claimed_by').order_by('-created_at')
        return render(request, 'lostfound/list.html', {
            'items': items,
            'form': form,
            'form_errors': True,
        })


class LostFoundResolveView(LoginRequiredMixin, View):
    """CR or reporter can mark as resolved."""
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(LostFoundItem, pk=pk)
        if not (request.user.is_cr or request.user == item.reporter):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        item.is_resolved = True
        item.save()
        messages.success(request, f'"{item.title}" marked as resolved.')
        return redirect('lostfound_list')


class LostFoundFoundView(LoginRequiredMixin, View):
    """When someone clicks 'I Found This' on a lost item — changes status to found."""
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(LostFoundItem, pk=pk)
        if item.status != 'lost':
            return JsonResponse({'error': 'Item is not lost'}, status=400)

        item.status = 'found'
        item.save()

        return JsonResponse({
            'status': 'found',
            'reporter_name': item.reporter.full_name or item.reporter.email,
            'contact_info': item.contact_info,
        })


class LostFoundClaimView(LoginRequiredMixin, View):
    """When someone clicks 'This is mine — Claim it' on a found item."""
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(LostFoundItem, pk=pk)
        if item.status != 'found':
            return JsonResponse({'error': 'Item is not in found status'}, status=400)
        if item.claimed_by is not None:
            return JsonResponse({'error': 'Item has already been claimed'}, status=400)

        item.claimed_by = request.user
        item.save()

        return JsonResponse({
            'claimed_by_name': request.user.full_name or request.user.email,
            'reporter_name': item.reporter.full_name or item.reporter.email,
            'contact_info': item.contact_info,
        })


class LostFoundDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cr

    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(LostFoundItem, pk=pk)
        title = item.title
        item.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('lostfound_list')

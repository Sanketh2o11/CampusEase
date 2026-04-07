import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View

from .models import Notice, NoticePoll, PollVote, NoticeRead
from .forms import NoticeForm


class CRRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cr


class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/list.html'
    context_object_name = 'notices'

    def get_queryset(self):
        return Notice.objects.all().select_related('author').prefetch_related('poll', 'poll__votes', 'reads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Pinned notices (max 3)
        context['pinned_notices'] = Notice.objects.filter(is_pinned=True).order_by('-created_at')[:3]

        # Mark all visible notices as read for this student
        notices = context['notices']
        if notices:
            read_records = [
                NoticeRead(notice=notice, student=user)
                for notice in notices
            ]
            NoticeRead.objects.bulk_create(read_records, ignore_conflicts=True)

        # Annotate each notice with read count and user's vote
        for notice in notices:
            notice.read_count = notice.reads.count()
            if hasattr(notice, 'poll'):
                poll = notice.poll
                poll.yes_count = poll.votes.filter(choice='yes').count()
                poll.no_count = poll.votes.filter(choice='no').count()
                poll.maybe_count = poll.votes.filter(choice='maybe').count()
                try:
                    poll.user_vote = poll.votes.get(student=user).choice
                except PollVote.DoesNotExist:
                    poll.user_vote = None

        return context


class NoticeCreateView(LoginRequiredMixin, CRRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/form.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Create poll if event type and poll data provided
        if form.cleaned_data.get('notice_type') == 'event':
            poll_question = self.request.POST.get('poll_question', '').strip()
            if poll_question:
                NoticePoll.objects.create(
                    notice=self.object,
                    question=poll_question,
                    option_yes=self.request.POST.get('poll_option_yes', "Yes, I'm in") or "Yes, I'm in",
                    option_no=self.request.POST.get('poll_option_no', "No, I'll skip") or "No, I'll skip",
                    option_maybe=self.request.POST.get('poll_option_maybe', "Maybe") or "Maybe",
                )

        return response


class NoticeUpdateView(LoginRequiredMixin, CRRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/form.html'
    success_url = reverse_lazy('notice_list')


class NoticeDeleteView(LoginRequiredMixin, CRRequiredMixin, DeleteView):
    model = Notice
    success_url = reverse_lazy('notice_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class NoticePinToggleView(LoginRequiredMixin, CRRequiredMixin, View):
    def post(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        notice.is_pinned = not notice.is_pinned
        notice.save()
        return redirect('notice_list')


@login_required
@require_POST
def poll_vote(request, pk):
    """AJAX endpoint: POST /notices/<id>/vote/ — vote on a poll."""
    try:
        data = json.loads(request.body)
        choice = data.get('choice')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if choice not in ('yes', 'no', 'maybe'):
        return JsonResponse({'error': 'Invalid choice'}, status=400)

    notice = get_object_or_404(Notice, pk=pk)
    if not hasattr(notice, 'poll'):
        return JsonResponse({'error': 'No poll on this notice'}, status=404)

    poll = notice.poll

    # Update or create vote
    PollVote.objects.update_or_create(
        poll=poll,
        student=request.user,
        defaults={'choice': choice},
    )

    # Return updated counts
    return JsonResponse({
        'yes_count': poll.votes.filter(choice='yes').count(),
        'no_count': poll.votes.filter(choice='no').count(),
        'maybe_count': poll.votes.filter(choice='maybe').count(),
        'user_vote': choice,
    })

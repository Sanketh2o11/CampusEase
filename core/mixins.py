from django.contrib.auth.mixins import UserPassesTestMixin


class CRRequiredMixin(UserPassesTestMixin):
    """Restrict a CBV to authenticated CR users only."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cr

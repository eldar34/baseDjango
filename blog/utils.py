from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class AuthorPermissionMixin:

    def has_permission(self):
        currentUser = self.request.user
        superuser = User.objects.filter(username=currentUser, is_superuser=1).exists()
        self.get_object().author == currentUser
        if superuser or currentUser == self.get_object().author:
            return True 
        else:
            return False
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.success(self.request, 'Permission denied')
            return redirect('/post/{}/'.format(self.get_object().pk))
        return super().dispatch(request, *args, **kwargs)
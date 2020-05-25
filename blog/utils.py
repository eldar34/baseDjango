from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import BasePermission 
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth import login
from django.utils.encoding import force_text 
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse

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
        return bool(self.request.user.is_superuser or self.request.user == self.get_object().author)
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.success(self.request, 'Permission denied')
            return redirect('/post/{}/'.format(self.get_object().pk))
        return super().dispatch(request, *args, **kwargs)

class AuthorApiPermissionMixin(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user
    
    # def has_permission(self, request, view):
    #     return bool(self.request.user.is_superuser or self.request.user == self.get_object().author)

class ApiEmailConfirm:
    """ Activate user """

    def chekUser(self, request, uidb64=None, token=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(pk=uid)
            print(uid)
        except User.DoesNotExist:
            user = None
        if user and default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.is_active = True
            user.save()
            login(request, user)
            print("Activaton done")
        else:
            print("Activation failed")

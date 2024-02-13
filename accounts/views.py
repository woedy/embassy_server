from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import FormView, CreateView
from django.views.generic.edit import FormMixin

from accounts.forms import LoginForm, RegisterForm, ReactivateEmailForm
from accounts.models import EmailActivation
from mysite.mixins import NextUrlMixin, RequestFormAttachMixin
from visa.models import VisaApplication

User = get_user_model()

class LoginView(SuccessMessageMixin, NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/visa/visa_init_view/'
    template_name = 'accounts/login.html'
    default_next = '/visa/visa_init_view/'
    success_message = "Login Successful"

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


def login_view(request):

    context = {}

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        qs = User.objects.filter(email=email)



        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("accounts:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                                                resend confirmation email</a>.
                                                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    messages.info(request, msg1)
                    return redirect("accounts:login")
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    messages.info(request, msg2)
                if not is_confirmable and not email_confirm_exists:
                    messages.info(request, "This user is inactive.")
        user = authenticate(email=email, password=password)
        visa_application = VisaApplication.objects.filter(user=user).first()
        if user is not None:
            if visa_application is None:
                login(request, user)
                messages.success(request, f"You are now logged in as {email}.")
                return redirect("visa:visa_init_view")
            if visa_application is not None:
                step_complete = visa_application.step_complete

                print(step_complete)


                if step_complete == "Step One":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with step two")
                    return redirect("visa:visa_application_form_2")
                elif step_complete == "Step Two":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with step three")
                    return redirect("visa:visa_application_form_3")
                elif step_complete == "Step Three":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with step three b")
                    return redirect("visa:visa_application_form_3b")
                elif step_complete == "Step Three_b":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with step four")
                    return redirect("visa:visa_application_form_4")
                elif step_complete == "Step Four":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with review")
                    return redirect("visa:visa_application_review")
                elif step_complete == "Review":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}. Proceed with payment")
                    return redirect("visa:visa_application_form_5")
                elif step_complete == "Submitted":
                    login(request, user)
                    messages.success(request, f"You are now logged in as {email}.")
                    return redirect("visa:visa_init_view")
        else:
            messages.error(request, "Invalid credential")

    return render(request, 'accounts/login.html', context)








def login_view2(request):

    context = {}

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']


        print(email)
        print(password)

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are now logged in as {email}.")
            return redirect("visa:visa_init_view")
        else:
            messages.error(request, "Invalid credential")

    return render(request, 'accounts/login.html', context)


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'
    success_message = "Account created successfully. A verification link is sent to your email."



def logout_view(request):
    logout(request)
    return redirect('/')



class AccountEmailActivateView(FormMixin, View):
    success_url = '/accounts/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("accounts:login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("accounts:login")
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)






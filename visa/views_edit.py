from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.views import View
from xhtml2pdf import pisa

from visa.models import VisaApplication, PersonalInfo, TravelDetail, TravelHistory, PassportDetail, ContactInfo, \
    MailingAddress, HotelBusinessWorkSchoolAddress, DestinedCountryAddress, EmployerAddress, SponsorOfTrip, \
    ProxyApplicant, Payment, AdditionalDocument

User = get_user_model()

def visa_application_form_1_edit(request):
    context = {}

    user = User.objects.get(id=request.user.id)

    visa_application = VisaApplication.objects.get(user=user)

    if request.method == "POST":


        #VisaApplication


        visa_application.visa_type=request.POST['visa_type']
        visa_application.passport_type = request.POST['passport_type']
        visa_application.country_residence = request.POST['country_residence']
        visa_application.visa_entry = request.POST['visa_entry']
        visa_application.nationality = request.POST['nationality']
        visa_application.nationality_at_birth = request.POST['nationality_at_birth']
        visa_application.other_nationality = request.POST['other_nationality']
        visa_application.embassy_processing_office = request.POST['embassy_processing_office']
        visa_application.service_type = request.POST['service_type']
        visa_application.save()

        # PersonalInfo

        personal_info = PersonalInfo.objects.get(user=user)
        personal_info.other_names = request.POST.get("other_names")
        personal_info.title = request.POST['title']
        personal_info.median_names = request.POST['median_names']
        personal_info.gender = request.POST['gender']
        personal_info.marital_status = request.POST['marital_status']
        personal_info.profession = request.POST['profession']
        personal_info.dob = request.POST['dob']
        personal_info.place_of_birth = request.POST['place_of_birth']
        personal_info.phone_number = request.POST['phone_number']
        personal_info.mode_of_communication = request.POST['mode_of_communication']


        personal_info.save()

        # TravelDetail
        travel_detail = TravelDetail.objects.get(visa=visa_application)
        travel_detail.purpose_of_travel=request.POST['purpose_of_travel']
        travel_detail.stay_duration = request.POST['stay_duration']
        travel_detail.departure_date = request.POST['departure_date']
        travel_detail.return_ticket = bool(request.POST.get('return_ticket', False))
        travel_detail.last_visit_to_country_date = request.POST['last_visit_to_country_date']
        travel_detail.financial_dispose = request.POST['financial_dispose']

        travel_detail.save()

        print(request.POST.get('ever_visited_destination'))


        # TravelHistory
        travel_history = TravelHistory.objects.get(visa=visa_application)
        travel_history.ever_visited_destination = bool(request.POST.get('ever_visited_destination', False))
        travel_history.ever_been_denied_entry = bool(request.POST.get('ever_been_denied_entry', False))
        travel_history.ever_been_denied_visa = bool(request.POST.get('ever_been_denied_visa', False))
        travel_history.ever_been_deported = bool(request.POST.get('ever_been_deported', False))
        travel_history.criminal_record_in_destined_or_other = bool(request.POST.get('criminal_record_in_destined_or_other', False))
        travel_history.mental_disorder = bool(request.POST.get('mental_disorder', False))
        travel_history.communicable_disease = bool(request.POST.get('communicable_disease', False))


        travel_history.save()

        visa_application.step_complete = "Step One"
        visa_application.save()



        return redirect("visa:visa_application_review")


    personal_info = PersonalInfo.objects.get(user=user)
    visa_application = VisaApplication.objects.get(user=user)




    context['visa_application'] = visa_application
    context['personal_info'] = personal_info



    return render(request, 'edit_visa/visa_application_form_1_edit.html', context)

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

def embassy_admin_view(request):
    context = {}

    user = User.objects.get(id=request.user.id)
    visa_applications = VisaApplication.objects.all().order_by('timestamp')

    context['all_applications'] = visa_applications

    return render(request, 'embassy_admin_view.html', context)


def admin_view_visa_application(request, id):
    context = {}

    if request.method == "POST":
        print(request.POST['status'])
        print(id)

        visa_application = VisaApplication.objects.get(id=id)
        visa_application.status = request.POST['status']
        visa_application.save()
        messages.success(request, f"Visa Application Status changed to {request.POST['status']}.")

        if visa_application.status == "Completed":
            send_complete_confirmation(visa_application.user.email, visa_application.user)

        if visa_application.status == "Review":
            send_review_confirmation(visa_application.user.email, visa_application.user)


        return redirect("visa:embassy_admin_view")



    visa_application = get_object_or_404(VisaApplication, id=id)

    user_id = visa_application.user.id
    user = User.objects.get(id=user_id)
    personal_info = PersonalInfo.objects.get(user=user)
    travel_detail = TravelDetail.objects.get(visa=visa_application)
    travel_history = TravelHistory.objects.get(visa=visa_application)
    passport_detail = PassportDetail.objects.get(visa=visa_application)
    contact_info = ContactInfo.objects.get(visa=visa_application)
    mailing_address = MailingAddress.objects.get(visa=visa_application)
    hotel_address = HotelBusinessWorkSchoolAddress.objects.get(visa=visa_application)
    destined_country_address = DestinedCountryAddress.objects.get(visa=visa_application)
    employer_address = EmployerAddress.objects.get(visa=visa_application)
    sponsor_of_trip = SponsorOfTrip.objects.get(visa=visa_application)
    proxy_applicant = ProxyApplicant.objects.get(visa=visa_application)
    payment = Payment.objects.get(visa=visa_application)
    additional_document = AdditionalDocument.objects.get(visa=visa_application)

    context['visa_application'] = visa_application
    context['personal_info'] = personal_info
    context['travel_detail'] = travel_detail
    context['travel_history'] = travel_history
    context['passport_detail'] = passport_detail
    context['contact_info'] = contact_info
    context['mailing_address'] = mailing_address
    context['hotel_address'] = hotel_address
    context['destined_country_address'] = destined_country_address
    context['employer_address'] = employer_address
    context['sponsor_of_trip'] = sponsor_of_trip
    context['proxy_applicant'] = proxy_applicant
    context['payment'] = payment
    context['additional_document'] = additional_document


    return render(request, 'admin_view_visa_application.html', context)


def visa_view(request):
    context = {}

    return render(request, 'visa_view.html', context)


def visa_init_view(request):
    context = {}

    user = User.objects.get(id=request.user.id)
    visa_application = VisaApplication.objects.filter(user=user).first()

    if visa_application is not None:
        context['visa_application'] = visa_application
    elif visa_application is None:
        context['visa_application'] = None

    context['user'] = user


    return render(request, 'visa_init_view.html', context)



def update_profile_view(request):
    context = {}

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":

        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.save()
        messages.success(request, f"Profile updated successfully.")
        return redirect("visa:visa_init_view")

    context['user'] = user

    return render(request, 'update_profile_view.html', context)



def visa_application_view(request):
    context = {}


    return render(request, 'visa_application_view.html', context)


def visa_application_successful_view(request):


    context = {}

    return render(request, 'visa_application_successful_view.html', context)


def visa_application_form(request):
    context = {}

    if request.method == "POST":
        print(request.POST['visa_type'])
        print(request.POST['passport_type'])
        print(request.POST['service_type'])

        #VisaApplication

        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.create(
            user=user,
            visa_type=request.POST['visa_type'],
            passport_type=request.POST['passport_type'],
            country_residence=request.POST['country_residence'],
            visa_entry=request.POST['visa_entry'],
            nationality=request.POST['nationality'],
            nationality_at_birth=request.POST['nationality_at_birth'],
            other_nationality=request.POST['other_nationality'],
            embassy_processing_office=request.POST['embassy_processing_office'],
            service_type=request.POST['service_type'],

        )
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
        travel_detail = TravelDetail.objects.create(
            visa=visa_application,
            purpose_of_travel=request.POST['purpose_of_travel'],
            stay_duration=request.POST['stay_duration'],
            departure_date=request.POST['departure_date'],
            return_ticket=bool(request.POST.get('return_ticket', False)),
            last_visit_to_country_date=request.POST['last_visit_to_country_date'],
            financial_dispose=request.POST['financial_dispose'],
        )

        travel_detail.save()

        print(request.POST.get('ever_visited_destination'))


        # TravelHistory
        travel_history = TravelHistory.objects.create(
            visa=visa_application,
            ever_visited_destination=bool(request.POST.get('ever_visited_destination', False)),
            ever_been_denied_entry=bool(request.POST.get('ever_been_denied_entry', False)),
            ever_been_denied_visa=bool(request.POST.get('ever_been_denied_visa', False)),
            ever_been_deported=bool(request.POST.get('ever_been_deported', False)),
            criminal_record_in_destined_or_other=bool(request.POST.get('criminal_record_in_destined_or_other', False)),
            mental_disorder=bool(request.POST.get('mental_disorder', False)),
            communicable_disease=bool(request.POST.get('communicable_disease', False)),
        )

        travel_history.save()

        ##  STEP 2
        ##
        #####################################

        # PassportDetail
        passport_detail = PassportDetail.objects.create(
            visa=visa_application,
            passport_no=request.POST['financial_dispose'],
            place_of_issue=request.POST['place_of_issue'],
            date_of_issue=request.POST['date_of_issue'],
            expiry_date=request.POST['expiry_date'],
        )

        passport_detail.save()

        # ContactInfo
        contact_info = ContactInfo.objects.create(
            visa=visa_application,
            application_name=request.POST['application_name'],
            residential_addr_cur_country=request.POST['residential_addr_cur_country'],
            street_address=request.POST['street_address'],
            postal_address=request.POST['postal_address'],
            city_town=request.POST['city_town'],
            country=request.POST['country'],
            state_region=request.POST['state_region'],
            zip_code=request.POST['zip_code'],
            telephone=request.POST['telephone'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
        )

        contact_info.save()

        # MailingAddress
        mailing_address = MailingAddress.objects.create(
            visa=visa_application,
            same_as_residential=bool(request.POST.get('same_as_residential', False)),
            recipient_name=request.POST['recipient_name'],
            postal_address=request.POST['postal_address_m'],
            address_2=request.POST['address_2_m'],
            city_town=request.POST['city_town_m'],
            country=request.POST['country_m'],
            state_region=request.POST['state_region_m'],
            zip_code=request.POST['zip_code_m'],
            email=request.POST['email_m'],
        )

        mailing_address.save()

        # HotelBusinessWorkSchoolAddress
        hotel_address = HotelBusinessWorkSchoolAddress.objects.create(
            visa=visa_application,
            retiree_complete=bool(request.POST.get('retiree_complete', False)),
            name=request.POST['name_h'],
            postal_address=request.POST['postal_address_h'],
            address_2=request.POST['address_2_h'],
            city_town=request.POST['city_town_h'],
            country=request.POST['country_h'],
            state_region=request.POST['state_region_h'],
            zip_code=request.POST['zip_code_h'],
            email=request.POST['email_h'],

        )
        hotel_address.save()

        # DestinedCountryAddress
        destined_country = DestinedCountryAddress.objects.create(
            visa=visa_application,
            host_name=request.POST['host_name_d'],
            street_name=request.POST['street_name_d'],
            city=request.POST['city_d'],
            physical_address=request.POST['physical_address_d'],
            telephone=request.POST['telephone_d'],
            email=request.POST['email_d'],

            )
        destined_country.save()

        # EmployerAddress
        employer_address = EmployerAddress.objects.create(
            visa=visa_application,
            name_of_reference=request.POST['name_of_reference_e'],
            address_1=request.POST['address_1_e'],
            address_2=request.POST['address_2_e'],
            city_town=request.POST['city_town_e'],
            country=request.POST['country_e'],
            state_region=request.POST['state_region_e'],
            digital_address=request.POST['digital_address_e'],
            telephone=request.POST['telephone_e'],
            tin_no=request.POST['tin_no_e'],

        )
        employer_address.save()

        ##  STEP 3
        ##
        #####################################

        # SponsorOfTrip
        sponsor_of_trip = SponsorOfTrip.objects.create(
            visa=visa_application,
            sponsor_as_applicant=bool(request.POST.get('sponsor_as_applicant', False)),
            organization=request.POST['organization'],
            last_name=request.POST['last_name_s'],
            first_name=request.POST['first_name_s'],
            other_names=request.POST['other_names_s'],
            phone=request.POST['phone_s'],
            address=request.POST['address_s'],
            country=request.POST['country_s'],
            email=request.POST['email_s'],

        )

        sponsor_of_trip.save()

        # ProxyApplicant
        proxy_applicant = ProxyApplicant.objects.create(
            visa=visa_application,
            full_name=request.POST['full_name_p'],
            address=request.POST['address_p'],
            telephone=request.POST['telephone_p'],
            phone=request.POST['phone_p'],
            not_applicable=bool(request.POST.get('not_applicable_p', False)),

        )

        proxy_applicant.save()

        # Payment
        payment = Payment.objects.create(
            visa=visa_application,
            payment_method=request.POST['payment_method'],
            amount=request.POST['amount'],
        )
        payment.save()

        return render(request, 'visa_application_successful_view.html', context)




    return render(request, 'visa_application_form.html', context)

def visa_application_form_1(request):
    context = {}

    if request.method == "POST":


        #VisaApplication

        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.create(
            user=user,
            visa_type=request.POST['visa_type'],
            passport_type=request.POST['passport_type'],
            country_residence=request.POST['country_residence'],
            visa_entry=request.POST['visa_entry'],
            nationality=request.POST['nationality'],
            nationality_at_birth=request.POST['nationality_at_birth'],
            other_nationality=request.POST['other_nationality'],
            embassy_processing_office=request.POST['embassy_processing_office'],
            service_type=request.POST['service_type'],

        )
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
        travel_detail = TravelDetail.objects.create(
            visa=visa_application,
            purpose_of_travel=request.POST['purpose_of_travel'],
            stay_duration=request.POST['stay_duration'],
            departure_date=request.POST['departure_date'],
            return_ticket=bool(request.POST.get('return_ticket', False)),
            last_visit_to_country_date=request.POST['last_visit_to_country_date'],
            financial_dispose=request.POST['financial_dispose'],
        )

        travel_detail.save()

        print(request.POST.get('ever_visited_destination'))


        # TravelHistory
        travel_history = TravelHistory.objects.create(
            visa=visa_application,
            ever_visited_destination=bool(request.POST.get('ever_visited_destination', False)),
            ever_been_denied_entry=bool(request.POST.get('ever_been_denied_entry', False)),
            ever_been_denied_visa=bool(request.POST.get('ever_been_denied_visa', False)),
            ever_been_deported=bool(request.POST.get('ever_been_deported', False)),
            criminal_record_in_destined_or_other=bool(request.POST.get('criminal_record_in_destined_or_other', False)),
            mental_disorder=bool(request.POST.get('mental_disorder', False)),
            communicable_disease=bool(request.POST.get('communicable_disease', False)),
        )

        travel_history.save()

        visa_application.step_complete = "Step One"
        visa_application.save()

        return redirect("visa:visa_application_form_2")



    return render(request, 'visa_application_form_1.html', context)


def visa_application_form_2(request):
    context = {}

    if request.method == "POST":


        #VisaApplication

        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)

        ##  STEP 2
        ##
        #####################################

        # PassportDetail
        passport_detail = PassportDetail.objects.create(
            visa=visa_application,
            passport_no=request.POST['passport_no'],
            place_of_issue=request.POST['place_of_issue'],
            date_of_issue=request.POST['date_of_issue'],
            expiry_date=request.POST['expiry_date'],
        )

        passport_detail.save()

        # ContactInfo
        contact_info = ContactInfo.objects.create(
            visa=visa_application,
            application_name=request.POST['application_name'],
            residential_addr_cur_country=request.POST['residential_addr_cur_country'],
            street_address=request.POST['street_address'],
            postal_address=request.POST['postal_address'],
            city_town=request.POST['city_town'],
            country=request.POST['country'],
            state_region=request.POST['state_region'],
            zip_code=request.POST['zip_code'],
            telephone=request.POST['telephone'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
        )

        contact_info.save()

        # MailingAddress
        mailing_address = MailingAddress.objects.create(
            visa=visa_application,
            same_as_residential=bool(request.POST.get('same_as_residential', False)),
            recipient_name=request.POST['recipient_name'],
            postal_address=request.POST['postal_address_m'],
            address_2=request.POST['address_2_m'],
            city_town=request.POST['city_town_m'],
            country=request.POST['country_m'],
            state_region=request.POST['state_region_m'],
            zip_code=request.POST['zip_code_m'],
            email=request.POST['email_m'],
        )

        mailing_address.save()

        # HotelBusinessWorkSchoolAddress
        hotel_address = HotelBusinessWorkSchoolAddress.objects.create(
            visa=visa_application,
            retiree_complete=bool(request.POST.get('retiree_complete', False)),
            name=request.POST['name_h'],
            postal_address=request.POST['postal_address_h'],
            address_2=request.POST['address_2_h'],
            city_town=request.POST['city_town_h'],
            country=request.POST['country_h'],
            state_region=request.POST['state_region_h'],
            zip_code=request.POST['zip_code_h'],
            email=request.POST['email_h'],

        )
        hotel_address.save()

        # DestinedCountryAddress
        destined_country = DestinedCountryAddress.objects.create(
            visa=visa_application,
            host_name=request.POST['host_name_d'],
            street_name=request.POST['street_name_d'],
            city=request.POST['city_d'],
            physical_address=request.POST['physical_address_d'],
            telephone=request.POST['telephone_d'],
            email=request.POST['email_d'],

            )
        destined_country.save()

        # EmployerAddress
        employer_address = EmployerAddress.objects.create(
            visa=visa_application,
            name_of_reference=request.POST['name_of_reference_e'],
            address_1=request.POST['address_1_e'],
            address_2=request.POST['address_2_e'],
            city_town=request.POST['city_town_e'],
            country=request.POST['country_e'],
            state_region=request.POST['state_region_e'],
            digital_address=request.POST['digital_address_e'],
            telephone=request.POST['telephone_e'],
            tin_no=request.POST['tin_no_e'],

        )
        employer_address.save()

        visa_application.step_complete = "Step Two"
        visa_application.save()


        return redirect("visa:visa_application_form_3")




    return render(request, 'visa_application_form_2.html', context)


def visa_application_form_3(request):
    context = {}

    if request.method == "POST":

        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)


        ##  STEP 3
        ##
        #####################################

        # SponsorOfTrip
        sponsor_of_trip = SponsorOfTrip.objects.create(
            visa=visa_application,
            sponsor_as_applicant=bool(request.POST.get('sponsor_as_applicant', False)),
            organization=request.POST['organization'],
            last_name=request.POST['last_name_s'],
            first_name=request.POST['first_name_s'],
            other_names=request.POST['other_names_s'],
            phone=request.POST['phone_s'],
            address=request.POST['address_s'],
            country=request.POST['country_s'],
            email=request.POST['email_s'],

        )

        sponsor_of_trip.save()

        # ProxyApplicant
        proxy_applicant = ProxyApplicant.objects.create(
            visa=visa_application,
            full_name=request.POST['full_name_p'],
            address=request.POST['address_p'],
            telephone=request.POST['telephone_p'],
            phone=request.POST['phone_p'],
            language=request.POST['language'],
            not_applicable=bool(request.POST.get('not_applicable_p', False)),

        )

        proxy_applicant.save()

        visa_application.step_complete = "Step Three"
        visa_application.save()

        return redirect("visa:visa_application_form_3b")



    return render(request, 'visa_application_form_3.html', context)

def visa_application_form_3b(request):
    context = {}


    if request.method == "POST":

        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)


        ##  STEP 3b
        ##
        #####################################

        # AdditionalDocument
        additional_document = AdditionalDocument.objects.create(
            visa=visa_application,
            passport_picture=request.FILES['passport_picture'],
            payment_evidence=request.FILES['payment_evidence'],
            transfer_certificate=request.FILES['transfer_certificate'],
            financial_proof=request.FILES['financial_proof'],
            bio_data=request.FILES['bio_data'],
            covid_cert=request.FILES['covid_cert']
        )

        additional_document.save()

        visa_application.step_complete = "Step Three_b"
        visa_application.save()

        return redirect("visa:visa_application_form_4")



    return render(request, 'visa_application_form_3b.html', context)


def visa_application_form_4(request):
    context = {}

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)

        visa_application.step_complete = "Step Four"
        visa_application.save()

        return redirect("visa:visa_application_review")

    return render(request, 'visa_application_form_4.html', context)


def visa_application_review(request):
    context = {}

    user = User.objects.get(id=request.user.id)

    visa_application = VisaApplication.objects.get(user=user)
    personal_info = PersonalInfo.objects.get(user=user)
    travel_detail = TravelDetail.objects.get(visa=visa_application)
    travel_history = TravelHistory.objects.get(visa=visa_application)
    passport_detail = PassportDetail.objects.get(visa=visa_application)
    contact_info = ContactInfo.objects.get(visa=visa_application)
    mailing_address = MailingAddress.objects.get(visa=visa_application)
    hotel_address = HotelBusinessWorkSchoolAddress.objects.get(visa=visa_application)
    destined_country_address = DestinedCountryAddress.objects.get(visa=visa_application)
    employer_address = EmployerAddress.objects.get(visa=visa_application)
    sponsor_of_trip = SponsorOfTrip.objects.get(visa=visa_application)
    proxy_applicant = ProxyApplicant.objects.get(visa=visa_application)
    additional_document = AdditionalDocument.objects.get(visa=visa_application)


    context['user'] = user
    context['visa_application'] = visa_application
    context['personal_info'] = personal_info
    context['travel_detail'] = travel_detail
    context['travel_history'] = travel_history
    context['passport_detail'] = passport_detail
    context['contact_info'] = contact_info
    context['mailing_address'] = mailing_address
    context['hotel_address'] = hotel_address
    context['destined_country_address'] = destined_country_address
    context['employer_address'] = employer_address
    context['sponsor_of_trip'] = sponsor_of_trip
    context['proxy_applicant'] = proxy_applicant
    context['additional_document'] = additional_document


    if request.method == "POST":
        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)

        visa_application.step_complete = "Review"
        visa_application.save()

        return redirect("visa:visa_application_form_5")



    return render(request, 'visa_application_review.html', context)



def visa_application_form_5(request):
    context = {}

    if request.method == "POST":


        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)

        ##  STEP 5
        ##
        #####################################
        # Payment
        payment = Payment.objects.create(
            visa=visa_application,
            payment_method=request.POST['payment_method'],
            amount=request.POST['amount'],
        )
        payment.save()

        visa_application.step_complete = "Submitted"
        visa_application.save()

        send_submission_confirmation(user.email, user)

        return redirect("visa:visa_application_successful_view")




    return render(request, 'visa_application_form_5.html', context)




def view_visa_application(request):
    context = {}

    user = User.objects.get(id=request.user.id)

    visa_application = VisaApplication.objects.get(user=user)
    personal_info = PersonalInfo.objects.get(user=user)
    travel_detail = TravelDetail.objects.get(visa=visa_application)
    travel_history = TravelHistory.objects.get(visa=visa_application)
    passport_detail = PassportDetail.objects.get(visa=visa_application)
    contact_info = ContactInfo.objects.get(visa=visa_application)
    mailing_address = MailingAddress.objects.get(visa=visa_application)
    hotel_address = HotelBusinessWorkSchoolAddress.objects.get(visa=visa_application)
    destined_country_address = DestinedCountryAddress.objects.get(visa=visa_application)
    employer_address = EmployerAddress.objects.get(visa=visa_application)
    sponsor_of_trip = SponsorOfTrip.objects.get(visa=visa_application)
    proxy_applicant = ProxyApplicant.objects.get(visa=visa_application)
    payment = Payment.objects.get(visa=visa_application)
    additional_document = AdditionalDocument.objects.get(visa=visa_application)


    context['user'] = user
    context['visa_application'] = visa_application
    context['personal_info'] = personal_info
    context['travel_detail'] = travel_detail
    context['travel_history'] = travel_history
    context['passport_detail'] = passport_detail
    context['contact_info'] = contact_info
    context['mailing_address'] = mailing_address
    context['hotel_address'] = hotel_address
    context['destined_country_address'] = destined_country_address
    context['employer_address'] = employer_address
    context['sponsor_of_trip'] = sponsor_of_trip
    context['proxy_applicant'] = proxy_applicant
    context['payment'] = payment
    context['additional_document'] = additional_document




    return render(request, 'view_visa_application.html', context)



# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):

        context = {}
        user = User.objects.get(id=request.user.id)

        visa_application = VisaApplication.objects.get(user=user)
        personal_info = PersonalInfo.objects.get(user=user)
        travel_detail = TravelDetail.objects.get(visa=visa_application)
        travel_history = TravelHistory.objects.get(visa=visa_application)
        passport_detail = PassportDetail.objects.get(visa=visa_application)
        contact_info = ContactInfo.objects.get(visa=visa_application)
        mailing_address = MailingAddress.objects.get(visa=visa_application)
        hotel_address = HotelBusinessWorkSchoolAddress.objects.get(visa=visa_application)
        destined_country_address = DestinedCountryAddress.objects.get(visa=visa_application)
        employer_address = EmployerAddress.objects.get(visa=visa_application)
        sponsor_of_trip = SponsorOfTrip.objects.get(visa=visa_application)
        proxy_applicant = ProxyApplicant.objects.get(visa=visa_application)
        payment = Payment.objects.get(visa=visa_application)

        context['user'] = user
        context['visa_application'] = visa_application
        context['personal_info'] = personal_info
        context['travel_detail'] = travel_detail
        context['travel_history'] = travel_history
        context['passport_detail'] = passport_detail
        context['contact_info'] = contact_info
        context['mailing_address'] = mailing_address
        context['hotel_address'] = hotel_address
        context['destined_country_address'] = destined_country_address
        context['employer_address'] = employer_address
        context['sponsor_of_trip'] = sponsor_of_trip
        context['proxy_applicant'] = proxy_applicant
        context['payment'] = payment

        open('templates/temp.html', "w").write(render_to_string('visa_application_pdf.html', context))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


def send_submission_confirmation(email, user):
    host_scheme = getattr(settings, 'HOST_SCHEME', "http://")
    base_url = getattr(settings, 'BASE_URL', 'http://www.togoembassy.com')
    path = "{host}{base}".format(base=base_url, host=host_scheme)
    context = {
        'path': path,
        'user': user
    }

    txt_ = get_template("visa/submission_email.txt/").render(context)
    html_ = get_template("visa/submission_email.html/").render(context)
    subject = 'Togo Visa Application Submission'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )
    return sent_mail


def send_complete_confirmation(email, user):
    host_scheme = getattr(settings, 'HOST_SCHEME', "http://")
    base_url = getattr(settings, 'BASE_URL', 'http://www.togoembassy.com')
    path = "{host}{base}".format(base=base_url, host=host_scheme)
    context = {
        'path': path,
        'user': user
    }

    txt_ = get_template("visa/complete_email.txt/").render(context)
    html_ = get_template("visa/complete_email.html/").render(context)
    subject = 'Togo Visa Application Complete'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )
    return sent_mail

def send_review_confirmation(email, user):
    host_scheme = getattr(settings, 'HOST_SCHEME', "http://")
    base_url = getattr(settings, 'BASE_URL', 'http://www.togoembassy.com')
    path = "{host}{base}".format(base=base_url, host=host_scheme)
    context = {
        'path': path,
        'user': user
    }

    txt_ = get_template("visa/review_email.txt/").render(context)
    html_ = get_template("visa/review_email.html/").render(context)
    subject = 'Togo Visa Application Review'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )
    return sent_mail

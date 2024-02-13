import os
import random

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

VISA_TYPE_CHOICE = (

    ('Business', 'Business'),
    ('Diplomat', 'Diplomat'),
    ('Student', 'Student'),
)

PASSPORT_TYPE_CHOICE = (

    ('Ordinary', 'Ordinary'),
    ('Official', 'Official'),
    ('Diplomatic', 'Diplomatic'),
)

VISA_ENTRY_CHOICE = (

    ('Single Entry', 'Single Entry'),
    ('Multiple Entry', 'Multiple Entry'),
)

SERVICE_TYPE_CHOICE = (

    ('Standard Services', 'Standard Services'),
    ('Express Services', 'Express Services'),
)


STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('Review', 'Review'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)



STEP_CHOICE = (

    ('Step One', 'Step One'),
    ('Step Two', 'Step Two'),
    ('Step Three', 'Step Three'),
    ('Step Three_b', 'Step Three_b'),
    ('Step Four', 'Step Four'),
    ('Review', 'Review'),
    ('Step Five', 'Step Five'),

    ('Submitted', 'Submitted'),
)



#########################################################
##
##  STEP 1
##
#####################################

class VisaApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visa_app_user')
    visa_type = models.CharField(max_length=255, choices=VISA_TYPE_CHOICE, null=True, blank=True)
    passport_type = models.CharField(max_length=255, choices=PASSPORT_TYPE_CHOICE, null=True, blank=True)
    country_residence = models.CharField(max_length=200, null=True, blank=True)
    visa_entry = models.CharField(max_length=255, choices=VISA_ENTRY_CHOICE, null=True, blank=True)
    nationality = models.CharField(max_length=200, null=True, blank=True)
    nationality_at_birth = models.CharField(max_length=200, null=True, blank=True)
    other_nationality = models.CharField(max_length=200, null=True, blank=True)
    embassy_processing_office = models.CharField(max_length=200, null=True, blank=True)
    service_type = models.CharField(max_length=255, choices=SERVICE_TYPE_CHOICE, null=True, blank=True)

    status = models.CharField(default="Pending", max_length=255, null=True, blank=True, choices=STATUS_CHOICE)
    step_complete = models.CharField(default="Step One", max_length=255, null=True, blank=True, choices=STEP_CHOICE)
    timestamp = models.DateTimeField(auto_now_add=True)


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_default_profile_image():
    return "defaults/default_profile_image.png"



GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)


MODE_OF_COM_CHOICES = (
    ('Email', 'Email'),
    ('SMS', 'SMS'),

)

MARITAL_STATUS_CHOICES = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),

)


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    other_names = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_image_path, null=True, blank=True, default=get_default_profile_image)


    title = models.CharField(max_length=255, null=True, blank=True)
    median_names = models.CharField(max_length=255, null=True, blank=True)

    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    mode_of_communication = models.CharField(max_length=100, choices=MODE_OF_COM_CHOICES, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



PURPOSE_OF_TRAVEL_CHOICES = (
    ('Temporary', 'Temporary'),
    ('Study', 'Study'),
    ('Tourism', 'Tourism'),
    ('Diplomatic Affair', 'Diplomatic Affair'),

)

class TravelDetail(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_travel_detail')
    purpose_of_travel = models.CharField(max_length=100, choices=PURPOSE_OF_TRAVEL_CHOICES, blank=True, null=True)
    stay_duration = models.CharField(max_length=200, null=True, blank=True)
    departure_date = models.DateTimeField(null=True, blank=True)
    return_ticket = models.BooleanField(default=False)
    last_visit_to_country_date = models.DateTimeField(null=True, blank=True)
    financial_dispose = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class TravelHistory(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_travel_history')
    ever_visited_destination = models.BooleanField(default=False)
    ever_been_denied_entry = models.BooleanField(default=False)
    ever_been_denied_visa = models.BooleanField(default=False)
    ever_been_deported = models.BooleanField(default=False)
    criminal_record_in_destined_or_other = models.BooleanField(default=False)
    mental_disorder = models.BooleanField(default=False)
    communicable_disease = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)



#########################################################
##
##  STEP 2
##
#####################################

class PassportDetail(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_passport_detail')
    passport_no = models.CharField(max_length=200, null=True, blank=True)
    place_of_issue = models.CharField(max_length=200, null=True, blank=True)
    date_of_issue = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ContactInfo(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_contact_info')
    application_name = models.CharField(max_length=400, null=True, blank=True)
    residential_addr_cur_country = models.CharField(max_length=400, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    postal_address = models.CharField(max_length=200, null=True, blank=True)
    city_town = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state_region = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class MailingAddress(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_mailing')
    same_as_residential = models.BooleanField(default=False)
    recipient_name = models.CharField(max_length=200, null=True, blank=True)
    postal_address = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    city_town = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state_region = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class HotelBusinessWorkSchoolAddress(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_hotel')
    retiree_complete = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    postal_address = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    city_town = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state_region = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class DestinedCountryAddress(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_destined_country')
    host_name = models.CharField(max_length=200, null=True, blank=True)
    street_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    physical_address = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class EmployerAddress(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_employer_addr')
    name_of_reference = models.CharField(max_length=200, null=True, blank=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    city_town = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state_region = models.CharField(max_length=200, null=True, blank=True)
    digital_address = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    tin_no = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


#########################################################
##
##  STEP 3
##
#####################################


class SponsorOfTrip(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_sponsor')
    sponsor_as_applicant = models.BooleanField(default=False)
    organization = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    other_names = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ProxyApplicant(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_proxy')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=200, null=True, blank=True)
    not_applicable = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)


def upload_passport_pic_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "passport/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_payment_evidence_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "payment_evidence/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_transfer_certificate_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "transfer_certificate/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_financial_proof_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "financial_proof/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_bio_data_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "bio_data/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_covid_cert_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "covid_cert/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



class AdditionalDocument(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_doc')
    passport_picture = models.ImageField(upload_to=upload_passport_pic_path, null=True, blank=True)
    payment_evidence = models.ImageField(upload_to=upload_payment_evidence_path, null=True, blank=True)
    transfer_certificate = models.ImageField(upload_to=upload_transfer_certificate_path, null=True, blank=True)
    financial_proof = models.ImageField(upload_to=upload_financial_proof_path, null=True, blank=True)
    bio_data = models.ImageField(upload_to=upload_bio_data_path, null=True, blank=True)
    covid_cert = models.ImageField(upload_to=upload_covid_cert_path, null=True, blank=True)




class Payment(models.Model):
    visa = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='visa_payment_method')
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)



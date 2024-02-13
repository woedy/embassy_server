from django.db import models
from django.urls import path

from visa.views import visa_view, visa_application_form, visa_application_view, visa_application_successful_view, \
    visa_init_view, update_profile_view, view_visa_application, visa_application_form_1, visa_application_form_2, \
    visa_application_form_3, visa_application_form_5, visa_application_review, visa_application_form_4, \
    embassy_admin_view, GeneratePdf, admin_view_visa_application, visa_application_form_3b
from visa.views_edit import visa_application_form_1_edit
from visa.views_edit_prev import visa_application_form_1_edit_prev, visa_application_form_2_edit_prev, \
    visa_application_form_3_edit_prev, visa_application_form_3b_edit_prev

app_name = 'visa'

urlpatterns = [
    path('embassy_admin_view/', embassy_admin_view, name='embassy_admin_view'),
    path('admin_view_visa_application/<id>', admin_view_visa_application, name='admin_view_visa_application'),
    path('visa_view/', visa_view, name='visa_view'),
    path('visa_init_view/', visa_init_view, name='visa_init_view'),
    path('update_profile_view/', update_profile_view, name='update_profile_view'),
    path('visa_application_form/', visa_application_form, name='visa_application_form'),

    path('visa_application_form_1/', visa_application_form_1, name='visa_application_form_1'),

    path('visa_application_form_2/', visa_application_form_2, name='visa_application_form_2'),
    path('visa_application_form_3/', visa_application_form_3, name='visa_application_form_3'),
    path('visa_application_form_3b/', visa_application_form_3b, name='visa_application_form_3b'),
    path('visa_application_form_4/', visa_application_form_4, name='visa_application_form_4'),
    path('visa_application_review/', visa_application_review, name='visa_application_review'),
    path('visa_application_form_5/', visa_application_form_5, name='visa_application_form_5'),
    path('visa_application_view/', visa_application_view, name='visa_application_view'),

    path('view_visa_application/', view_visa_application, name='view_visa_application'),
    path('visa_application_successful_view/', visa_application_successful_view, name='visa_application_successful_view'),

    path('pdf/', GeneratePdf.as_view(), name='pdf'),



    #EDIT APPLICATION REVIEW
    path('visa_application_form_1_edit/', visa_application_form_1_edit, name='visa_application_form_1_edit'),


    #EDIT APPLICATION PREV
    path('visa_application_form_1_edit_prev/', visa_application_form_1_edit_prev, name='visa_application_form_1_edit_prev'),
    path('visa_application_form_2_edit_prev/', visa_application_form_2_edit_prev, name='visa_application_form_2_edit_prev'),
    path('visa_application_form_3_edit_prev/', visa_application_form_3_edit_prev, name='visa_application_form_3_edit_prev'),
    path('visa_application_form_3b_edit_prev/', visa_application_form_3b_edit_prev, name='visa_application_form_3b_edit_prev'),

]
from django.contrib import admin

# Register your models here.
from visa.models import VisaApplication, PersonalInfo, TravelDetail, TravelHistory, PassportDetail, ContactInfo, \
    MailingAddress, HotelBusinessWorkSchoolAddress, DestinedCountryAddress, EmployerAddress, SponsorOfTrip, \
    ProxyApplicant, Payment, AdditionalDocument

admin.site.register(VisaApplication)
admin.site.register(PersonalInfo)
admin.site.register(TravelDetail)
admin.site.register(TravelHistory)
admin.site.register(PassportDetail)
admin.site.register(ContactInfo)
admin.site.register(MailingAddress)
admin.site.register(HotelBusinessWorkSchoolAddress)
admin.site.register(DestinedCountryAddress)
admin.site.register(EmployerAddress)
admin.site.register(SponsorOfTrip)
admin.site.register(ProxyApplicant)
admin.site.register(Payment)
admin.site.register(AdditionalDocument)
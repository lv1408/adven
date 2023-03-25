from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from flight.models import *
import secrets
from datetime import datetime, timedelta
from xhtml2pdf import pisa

from flight.constant import *

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def createticket(user,customers,customerscount,adven,advenInDate,avenOutDate,serviceClass,trip_type,countrycode,email,mobile):
    adventures = adven_Ticket_Model.objects.create()
    adventures.user = user
    adventures.ref_no = secrets.token_hex(3).upper()
    for customer in customers:
        adventures.passengers.add(customer)
    adventures.adven = adven
    adventures.adven_ddate = datetime(int(advenInDate.split('-')[2]),int(advenInDate.split('-')[1]),int(advenInDate.split('-')[0]))
    ###################
    adventures.adve_adate = datetime(int(avenOutDate.split('-')[2]),int(avenOutDate.split('-')[1]),int(avenOutDate.split('-')[0]))
    ffre = 0.0
    if serviceClass.lower() == 'regular':
        if trip_type == '1':
            adventures.adven_fare = adven.regular_fare*int(customerscount)
            ffre = adven.regular_fare*int(customerscount)
        elif trip_type == '2':
            adventures.adven_fare = (adven.regular_fare * int(customerscount))*CAD
            ffre = (adven.regular_fare * int(customerscount))*CAD
    elif serviceClass.lower() == 'premium':
        if trip_type == '1':
            adventures.flight_fare = adven.premium_fare*int(customerscount)
            ffre = adven.premium_fare*int(customerscount)
        elif trip_type == '2':
            adventures.adven_fare = (adven.premium_fare * int(customerscount))*CAD
            ffre = (adven.premium_fare * int(customerscount))*CAD
    adventures.other_charges = FEE
                    ##########Coupon
    adventures.total_fare = ffre+FEE+0.0                    ##########Total(Including coupon)
    if trip_type == '1':
        adventures.currency = 'USD'
    elif trip_type == '2':
        adventures.currency = 'CAD'
    adventures.service_class = serviceClass.lower()
    adventures.status = 'PENDING'
    adventures.mobile = ('+'+countrycode+' '+mobile)
    adventures.email = email
    adventures.save()
    return adventures
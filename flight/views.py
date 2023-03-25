from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import math
from .models import *
from capstone.utils import render_to_pdf, createticket

# Fee and Surcharge variable
from .constant import FEE, USD, AUD, CAD, GBT, EUR
from flight.utils import createWeekDays, addPlaces, addDomesticFlights, addInternationalFlights

try:
    if len(Week.objects.all()) == 0:
        createWeekDays()

    if len(Place.objects.all()) == 0:
        addPlaces()

    if len(Flight.objects.all()) == 0:
        print("Do you want to add flights in the Database? (y/n)")
        if input().lower() in ['y', 'yes']:
            addDomesticFlights()
            addInternationalFlights()
except:
    pass


# Create your views here.

def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month + 3) <= 12 else datetime.now().date().year + 1}-{(datetime.now().date().month + 3) if (datetime.now().date().month + 3) <= 12 else (datetime.now().date().month + 3 - 12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        return_date = request.POST.get('ReturnDate')

        if (trip_type == '1'):
            return render(request, 'flight/index.html', {
                'min_date': min_date,
                'max_date': max_date,
                'origin': origin,
                'destination': destination,
                'depart_date': depart_date,
                'seat': seat.lower(),
                'trip_type': trip_type,
                'return_date': return_date
            })
        elif (trip_type == '2'):
            return render(request, 'flight/index.html', {
                'min_date': min_date,
                'max_date': max_date,
                'origin': origin,
                'destination': destination,
                'depart_date': depart_date,
                'seat': seat.lower(),
                'trip_type': trip_type,
                'return_date': return_date
            })
    else:
        return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date
        })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "flight/login.html")


def register_view(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "flight/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "flight/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flight/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def query(request, q):
    places = Place.objects.all()
    filters = []
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.airport.lower()) or (q in place.code.lower()) or (
                q in place.country.lower()):
            filters.append(place)
    return JsonResponse([{'code': place.code, 'city': place.city, 'country': place.country} for place in filters],
                        safe=False)


@csrf_exempt
def booking(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    returndate = request.GET.get('ReturnDate')
    return_date = datetime.strptime(returndate, "%Y-%m-%d")
    service = request.GET.get('SeatClass')

    adven_day = Week.objects.get(number=depart_date.weekday())
    destination = adven_place.objects.get(code=d_place.upper())
    origin = adven_place.objects.get(code=o_place.upper())
    print("----------------------->", origin)
    if service == 'regular':
        books = adven_booking.objects.filter(check_in_day=adven_day, origin=origin, destination=destination).exclude(
            regular_fare=0).order_by('regular_fare')
        print("----------------------->", books)
        try:
            max_price = books.last().regular_fare
            min_price = books.first().regular_fare
        except:
            max_price = 0
            min_price = 0

    elif service == 'premium':
        books = adven_booking.objects.filter(check_in_day=adven_day, origin=origin, destination=destination).exclude(
            premium_fare=0).order_by('premium_fare')
        print("--------SERVICE--------------->", books)
        price = adven_booking.objects.first().premium_fare
        try:
            max_price = books.last().premium_fare
            min_price = books.first().premium_fare
        except:
            max_price = 0
            min_price = 0

    # print(calendar.day_name[depart_date.weekday()])
    if trip_type == '1':
        # usd_price = price
        print("----------1------------->", books)
        return render(request, "flight/search.html", {
            'allbooks': books,
            'origin': origin,
            'destination': destination,
            'service': service.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price / 100) * 100,
            'min_price': math.floor(min_price / 100) * 100,
            # 'price': usd_price
        })
    else:
        for book in books:
            book.regular_fare = book.regular_fare * CAD
            book.premium_fare = book.premium_fare * CAD
        print("----------2------------->", books)
        return render(request, "flight/search.html", {
            'allbooks': books,
            'origin': origin,
            'destination': destination,
            'service': service.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': (math.ceil(max_price / 100) * 100) * 1.35,
            'min_price': (math.floor(min_price / 100) * 100) * 1.35,
            #'price': cad_price
        })

def review(request):
    adven_id = request.GET.get('bookId')
    adven_date = request.GET.get('bookDate')
    adven_check_out_date = request.GET.get('returnDate')
    service = request.GET.get('serviceClass')
    duration = request.GET.get('duration')
    trip_type = request.GET.get('trip_type')

    if request.user.is_authenticated:
        adven = adven_booking.objects.get(id=adven_id)
        advenInDate = datetime(int(adven_date.split('-')[2]),int(adven_date.split('-')[1]),int(adven_date.split('-')[0]),adven.check_in_timing.hour,adven.check_in_timing.minute)
        advenOutDate = datetime(int(adven_check_out_date.split('-')[2]),int(adven_check_out_date.split('-')[1]),int(adven_check_out_date.split('-')[0]),adven.check_out_time.hour,adven.check_out_time.minute)
        print("------advenOutDate------",advenOutDate)
        trip_types = trip_type
        regular_fare = adven.regular_fare
        premium_fare = adven.premium_fare
        if trip_types == '1':
            print("-----Reached-----")
            return render(request, "flight/book.html", {
                'adven': adven,
                "advenInDate": advenInDate,
                "advenOutDate": advenOutDate,
                "service": service,
                "fee": FEE * USD,
                "usd_premium_fare": premium_fare * USD,
                "usd_regular_fare": regular_fare * USD,
                "final_usd_premium_fare": (FEE * USD) + (premium_fare * USD),
                "final_usd_regular_fare": (FEE * USD) + (regular_fare * USD),
                "trip_types": trip_types
            })
        elif trip_types == '2':
            return render(request, "flight/book.html", {
                'adven': adven,
                "advenInDate": advenInDate,
                "advenOutDate": advenOutDate,
                "service": service,
                "fee": FEE * CAD,
                "cad_premium_fare": premium_fare * CAD,
                "cad_regular_fare": regular_fare * CAD,
                "final_cad_premium_fare": (FEE * CAD) + (premium_fare * CAD),
                "final_cad_regular_fare": (FEE * CAD) + (regular_fare * CAD),
                "trip_types": trip_types
            })
    else:
        return HttpResponseRedirect(reverse("login"))



def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            adven_id = request.POST.get('advenid')
            advenInDate = request.POST.get('advenInDate')
            avenOutDate = request.POST.get('avenOutDate')
            serviceClass = request.POST.get('serviceClass')
            trip_type = request.POST.get('trip-type')
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            print("-------mobile-------",mobile)
            email = request.POST['email']
            advenid = adven_booking.objects.get(id=adven_id)

            customercount = request.POST['passengersCount']
            passengers=[]
            for i in range(1,int(customercount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))

            try:
                booking_ticket = createticket(request.user,passengers,customercount,advenid,advenInDate,avenOutDate,serviceClass,trip_type,countrycode,email,mobile)

                if(serviceClass == 'Regular'):
                    if (trip_type == '1'):
                        conversion = advenid.regular_fare * USD
                        fare = (conversion*int(customercount))
                    elif (trip_type == '2'):
                        conversion = advenid.regular_fare * CAD
                        fare = (conversion * int(customercount))
                elif (serviceClass == 'Premium'):
                    if (trip_type == '1'):
                        conversion = advenid.premium_fare * USD
                        fare = (conversion * int(customercount))
                    elif (trip_type == '2'):
                        conversion = advenid.premium_fare * CAD
                        fare = (conversion * int(customercount))
            except Exception as e:
                return HttpResponse(e)
             ##
            return render(request, "flight/payment.html", {
                'fare': fare+FEE,
                'ticket': booking_ticket.id
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            print("---------------------->ticket_id",ticket_id)
            fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']

            try:
                ticket = adven_Ticket_Model.objects.get(id=ticket_id)
                ticket.status = 'CONFIRMED'
                print("----ticket.status----",ticket.status)
                ticket.booking_date = datetime.now()
                print("------ticket.booking_date------",ticket.booking_date)
                ticket.save()
                return render(request, 'flight/payment_process.html', {
                    'ticket1': ticket
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    ticket = adven_Ticket_Model.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.adven.origin.code,
        'to': ticket.adven.destination.code,
        'flight_date': ticket.adven_ddate,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    # ticket1 = adven_Ticket_Model.objects.get(ref_no=ref)
    ticket1 = adven_Ticket_Model.objects.get(ref_no=ref)
    print("----ref-----",ticket1)
    data = {
        'ticket1': ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def bookings(request):
    if request.user.is_authenticated:
        tickets = adven_Ticket_Model.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                ticket = adven_Ticket_Model.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            ticket = adven_Ticket_Model.objects.get(ref_no=ref)
            if ticket.user == request.user:
                return render(request, "flight/payment.html", {
                    'fare': ticket.total_fare,
                    'ticket': ticket.id
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def contact(request):
    return render(request, 'flight/contact.html')


def privacy_policy(request):
    return render(request, 'flight/privacy-policy.html')


def terms_and_conditions(request):
    return render(request, 'flight/terms.html')


def about_us(request):
    return render(request, 'flight/about.html')


def mountain_adven(request):
    return render(request, 'flight/mountain.html')

def water_adven(request):
    return render(request, 'flight/water.html')

def road_adven(request):
    return render(request, 'flight/road.html')

def air_adven(request):
    return render(request, 'flight/air.html')

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt
from django.db.models import Q

def index(request):

    return render(request, 'travel_app/index.html')

def reg(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
                print tag, error
            return redirect('/')

        elif len(errors) == 0:
            password=request.POST['pw']
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print "This is the hashed pw: ", hash1
            b = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)
            b.save()
            request.session['user_id'] = b.id
            request.session['first_name'] = b.first_name
            print request.session['user_id']
            return redirect('/trips/')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {'user': User.objects.filter(id=request.session['user_id']),
        'trips': (Trip.objects.filter(Q(trip_creator_id=request.session['user_id']) | Q(users=request.session['user_id'])).distinct().order_by('start_date')),
        #other_trips is set to the data stored in the Trip table where the logged in user is not the creator or a participant. Ordered by start_date
        'other_trips': (Trip.objects.exclude(Q(trip_creator_id=request.session['user_id']) | Q(users=request.session['user_id'])).distinct().order_by('start_date')),
    }
        return render(request, 'travel_app/travel_dashboard.html', context)


def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
                print tag, error
            return redirect('/')
        else:
            c = User.objects.filter(email=request.POST['email'])
            request.session['user_id'] = c[0].id
            request.session['first_name'] = c[0].first_name
            print request.session['user_id'], "hi"
            print c[0].first_name
            return redirect('/trips/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_trip(request):
    print request.method
    context = {
        #trips is set to the data stored in the Trip table where the logged in user is either the creator or a participant. Ordered by start_date
        'trips': (Trip.objects.filter(Q(trip_creator_id=request.session['user_id']) | Q(users=request.session['user_id'])).distinct().order_by('start_date')),
        #other_trips is set to the data stored in the Trip table where the logged in user is not the creator or a participant. Ordered by start_date
        'other_trips': (Trip.objects.exclude(Q(trip_creator_id=request.session['user_id']) | Q(users=request.session['user_id'])).distinct().order_by('start_date')),
    }
    return render(request, 'travel_app/add_trip.html', context)

def add_to_trips_list(request):
    print request.session['user_id']
    # context = {'user': User.objects.filter(id=request.session['user_id'])}
    errors = Trip.objects.trip_validator(request.POST)
    # if request.method == 'POST':
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            print tag, error
        return redirect('/add_trip/')
    else:
        newTrip = Trip.objects.create(destination=request.POST['destination'], itinerary_goal=request.POST['itinerary_goal'], start_date=datetime.strptime(request.POST['start_date'],'%m/%d/%Y').strftime('%Y-%m-%d'), end_date=datetime.strptime(request.POST['end_date'],'%m/%d/%Y').strftime('%Y-%m-%d'), trip_creator_id=request.session['user_id'])
        this_trip=Trip.objects.get(id=newTrip.id)
        this_trip_goer=User.objects.get(id=request.session['user_id'])
        this_trip_goer.trips.add(this_trip)
        print "This is the trip info: ", newTrip.id
        return redirect('/trips/')

def view_trip(request, trip_id):
    users = User.objects.filter(trips=Trip.objects.get(id=trip_id))
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'users_going_on_trip': users,
    }
    return render(request, 'travel_app/destination_details.html', context)

def delete_trip(request, trip_id):
    b = Trip.objects.get(id=trip_id)
    if b.trip_creator_id == request.session['user_id']:
        b.delete()
    else:
        b = Trip.objects.get(id=trip_id)
        this_trip_goer=User.objects.get(id=request.session['user_id'])
        this_trip_goer.trips.remove(b)

    return redirect('/trips/')

def add_this_trip(request, other_trips_id):
    this_trip=Trip.objects.get(id=other_trips_id)
    this_trip_goer=User.objects.get(id=request.session['user_id'])
    this_trip_goer.trips.add(this_trip)
    return redirect('/trips/')
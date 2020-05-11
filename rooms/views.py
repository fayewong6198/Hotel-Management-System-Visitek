from django.shortcuts import render, get_object_or_404
from .models import Room
from .models import Payment
from datetime import datetime, date
# Create your views here.


def search(request):
    check_in_date = datetime.today().date()
    check_out_date = datetime.today().date()

    # for filter
    parameters = {field_name: value for field_name, value in request.GET.items()
                  if value and field_name in Room._meta.get_fields()}

    try:
        if 'check_in_date' in request.GET:
            check_in_date = datetime.strptime(
                request.GET["check_in_date"], "%Y-%m-%d").date()

        if 'check_out_date' in request.GET:
            check_out_date = datetime.strptime(
                request.GET["check_out_date"], "%Y-%m-%d").date()
    except ValueError:
        check_in_date = datetime.today().date()
        check_out_date = datetime.today().date()

    rooms = Room.objects.all().filter(**parameters)
    result = []
    for room in rooms:
        if (check_valid_date(check_in_date, check_out_date, room)):
            result.append(room)

    print(result)

    context = {
        'rooms_length': len(result),
        'rooms': result,
        'check_in_date': check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': check_out_date.strftime("%Y-%m-%d")
    }
    print(result)

    return render(request, 'rooms/rooms-list.html', context)


def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    check_in_date = datetime.today().date()
    check_out_date = datetime.today().date()

    try:
        if 'check_in_date' in request.GET:
            check_in_date = datetime.strptime(
                request.GET["check_in_date"], "%Y-%m-%d").date()

        if 'check_out_date' in request.GET:
            check_out_date = datetime.strptime(
                request.GET["check_out_date"], "%Y-%m-%d").date()
    except ValueError:
        check_in_date = datetime.today().date()
        check_out_date = datetime.today().date()

    context = {
        'room': room,
        'check_in_date': check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': check_out_date.strftime("%Y-%m-%d")
    }
    print(room)
    return render(request, 'rooms/room.html', context)


def check_valid_date(check_in_date, check_out_date, room):
    payments = Payment.objects.filter(room=room)
    payments = payments.filter(
        status="WAITING") | payments.filter(status="CHECKED_IN")

    for payment in payments:
        if (check_in_date >= payment.expected_check_in_date and check_in_date <= payment.expected_check_in_date):
            return False

        if (check_out_date >= payment.expected_check_in_date and check_out_date <= payment.expected_check_out_date):
            return False

        if(check_out_date >= payment.expected_check_in_date and check_in_date <= payment.expected_check_in_date):
            return False
    return True

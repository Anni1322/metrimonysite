from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Matches, Messages
from accounts.models import Locations

@login_required
def matches(request):
    matches = Matches.objects.filter(user_id_1=request.user) | Matches.objects.filter(user_id_2=request.user)
    return render(request, 'matrimony/matches.html', {'matches': matches})

@login_required
def messages(request, user_id):
    messages = Messages.objects.filter(sender=request.user, receiver_id=user_id) | Messages.objects.filter(sender_id=user_id, receiver=request.user)
    return render(request, 'matrimony/chat.html', {'messages': messages})

# @login_required
# def nearest_people(request):
#     # Simple distance query using GIS
#     user_location = Locations.objects.get(user=request.user).location
#     nearby = Locations.objects.filter(location__distance_lte=(user_location, 50000))  # 50km
#     return render(request, 'matrimony/nearest.html', {'nearby': nearby})

# @login_required
# def nearest_people(request):
#     user_location = Locations.objects.get(user=request.user)
#     nearby = Locations.objects.filter(
#         city=user_location.city,
#         latitude__range=(user_location.latitude - 0.5, user_location.latitude + 0.5),
#         longitude__range=(user_location.longitude - 0.5, user_location.longitude + 0.5)
#     ).exclude(user=request.user)
#     return render(request, 'matrimony/nearest.html', {'nearby': nearby})


@login_required
def nearest_people(request):
    user_location = Locations.objects.get(user=request.user)
    nearby = Locations.objects.filter(
        city=user_location.city,
        latitude__range=(user_location.latitude - 0.5, user_location.latitude + 0.5),
        longitude__range=(user_location.longitude - 0.5, user_location.longitude + 0.5)
    ).exclude(user=request.user)
    return render(request, 'matrimony/nearest.html', {'nearby': nearby})
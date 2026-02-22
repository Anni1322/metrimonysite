from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Weddings, Vendors, Reviews

@login_required
def wedding_planner(request):
    weddings = Weddings.objects.filter(user=request.user)
    return render(request, 'weddings/wedding_planner.html', {'weddings': weddings})

@login_required
def unbooked_weddings(request):
    # "Not Booked" query
    unbooked = Weddings.objects.exclude(status='booked')
    return render(request, 'weddings/unbooked.html', {'unbooked': unbooked})

@login_required
def vendor_search(request):
    vendors = Vendors.objects.all()
    return render(request, 'weddings/vendors.html', {'vendors': vendors})
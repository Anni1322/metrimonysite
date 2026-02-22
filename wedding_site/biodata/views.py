from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages  # Added for user feedback
from .models import *
from .forms import *
import urllib.parse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# --- Register View ---

def register_view(request):
    if request.method == 'POST':
        # Use the custom form here!
        form = CustomUserRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "पंजीकरण सफल रहा!")
            return redirect('pages_dashboard')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration.html', {'form': form})



# --- Login View ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pages_member_profile_detail')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# --- Logout View ---
def logout_view(request):
    logout(request)
    messages.info(request, "आप सफलतापूर्वक लॉग आउट हो गए हैं।")
    return redirect('home')



# --- READ: Home & List View ---

def home(request):
    # Fetch recent profiles for the home page
    recent_profiles = CommunityBiodata.objects.filter(is_active=True).order_by('-created_at')[:4]
    return render(request, 'index.html', {'recent_profiles': recent_profiles})

def biodata_list(request):
    profiles = CommunityBiodata.objects.filter(is_active=True).order_by('-id')  
    
    search_query = request.GET.get('search', '')
    gotra_filter = request.GET.get('gotra', '')

    if search_query:
        profiles = profiles.filter(
            Q(full_name__icontains=search_query) | 
            Q(serial_number__icontains=search_query) |
            Q(district__icontains=search_query)
        )
    
    if gotra_filter:
        profiles = profiles.filter(gotra__icontains=gotra_filter)

    paginator = Paginator(profiles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profiles': page_obj,
        'search_query': search_query,
        'gotra_filter': gotra_filter
    }
    return render(request, 'biodata_list.html', context)

# --- CREATE: Add New Biodata ---

def biodata_create(request):
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save()
            messages.success(request, f"Biodata for {new_profile.full_name} created successfully!")
            return redirect('biodata_detail', pk=new_profile.pk) 
    else:
        form = CommunityBiodataForm()
    
    return render(request, 'biodata_form.html', {'form': form, 'title': 'Create New Biodata'})

# --- UPDATE: Edit Existing Biodata ---

def biodata_update(request, pk):
    profile = get_object_or_404(CommunityBiodata, pk=pk)
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, "Biodata updated successfully.")
            return redirect('biodata_detail', pk=profile.pk)
    else:
        form = CommunityBiodataForm(instance=profile)
    
    return render(request, 'biodata_form.html', {'form': form, 'profile': profile, 'title': 'Update Biodata'})

# --- DELETE: Remove Biodata ---

def biodata_delete(request, pk):
    profile = get_object_or_404(CommunityBiodata, pk=pk)
    if request.method == 'POST':
        profile.delete()
        messages.warning(request, "Biodata deleted permanently.")
        return redirect('biodata_list')
    return render(request, 'biodata_confirm_delete.html', {'profile': profile})

# --- READ: Detail View & Sharing ---

def biodata_detail(request, pk):
    profile = get_object_or_404(CommunityBiodata, pk=pk)
    target_user = profile.user
    
    # Updated text to include new fields
    share_text = f"""*गोंडवाना वैवाहिक ग्रुप (नि:शुल्क बायोडाटा)*
*सरल क्रमांक: {profile.serial_number}*
▶️ नाम: {profile.full_name}
▶️ लिंग: {profile.get_gender_display()}
▶️ जन्मतिथि: {profile.date_of_birth} ({profile.birth_time or 'N/A'})
▶️ वैवाहिक स्थिति: {profile.get_marital_status_display()}
▶️ जाति/गोत्र: {profile.caste} / {profile.gotra}
▶️ देव संख्या: {profile.deity_number}
▶️ शिक्षा: {profile.education}
▶️ व्यवसाय: {profile.occupation}
▶️ पता: {profile.city}, {profile.district}
*(संपर्क हेतु एडमीन से संपर्क करें)*"""
    
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

    return render(request, 'biodata_detail.html', {
        'profile': profile,
        'whatsapp_url': whatsapp_url,
        'target_user': target_user,
    })


# def biodata_detail(request, pk):
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
    
#     # The 'target_user' is now pulled from the model relationship
#     target_user = profile.user 
    
#     share_text = f"""*गोंडवाना वैवाहिक ग्रुप (नि:शुल्क बायोडाटा)*
# *सरल क्रमांक: {profile.serial_number}*
# ▶️ नाम: {profile.full_name}
# ▶️ लिंग: {profile.get_gender_display()}
# ▶️ जन्मतिथि: {profile.date_of_birth}
# ▶️ जाति/गोत्र: {profile.caste} / {profile.gotra}
# ▶️ व्यवसाय: {profile.occupation}
# ▶️ स्थान: {profile.city}, {profile.district}
# *(संपर्क हेतु एडमीन से संपर्क करें)*"""
    
#     whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

#     return render(request, 'biodata_detail.html', {
#         'profile': profile,
#         'whatsapp_url': whatsapp_url,
#         'target_user': target_user, # This is used in the template for the Chat button
#     })

# user profile

@login_required
def user_profile_settings(request):
    # Try to get the biodata linked to the logged-in user
    # Note: This requires a ForeignKey(User) in your CommunityBiodata model
    # For now, we'll fetch the most recent one or a specific one for the demo
    profile = CommunityBiodata.objects.filter(full_name=request.user.get_full_name()).first()
    
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "आपका प्रोफाइल सफलतापूर्वक अपडेट कर दिया गया है।")
            return redirect('pages_account_settings')
    else:
        form = CommunityBiodataForm(instance=profile)

    return render(request, 'accountSetting.html', {
        'form': form,
        'profile': profile
    })


# --- MANAGE: Admin Dashboard Logic ---
# @login_required
def dashboard(request):
    # Fetch all profiles (including inactive ones) for management
    profiles_list = CommunityBiodata.objects.all().order_by('-id')
    
    # Search logic for the dashboard table
    query = request.GET.get('q')
    if query:
        profiles_list = profiles_list.filter(
            Q(full_name__icontains=query) | Q(serial_number__icontains=query)
        )

    # Statistics
    stats = {
        'total': CommunityBiodata.objects.count(),
        'active': CommunityBiodata.objects.filter(is_active=True).count(),
        'inactive': CommunityBiodata.objects.filter(is_active=False).count(),
    }

    return render(request, 'userDashboard.html', {
        'profiles': profiles_list,
        'stats': stats
    })



# --- Matching Logic ---

def biodata_matching(request, pk):
    profile = get_object_or_404(CommunityBiodata, pk=pk)
    
    # Exclude same gotra (community rule) and different gender
    opposite_gender = 'F' if profile.gender == 'M' else 'M'
    
    suggestions = CommunityBiodata.objects.filter(
        gender=opposite_gender,
        is_active=True
    ).exclude(gotra=profile.gotra).order_by('?')[:6]

    return render(request, 'biodata_matching.html', {
        'base_profile': profile,
        'suggestions': suggestions
    })
    

def success_stories(request):
    stories = SuccessStory.objects.filter(is_verified=True).order_by('-wedding_date')
    return render(request, 'successstory.html', {'stories': stories})



@login_required
def member_profile_detail(request):
    # Fetch the profile linked to the logged-in user
    # Adjust the filter based on how you link Users to Biodata
    profile = CommunityBiodata.objects.filter(email=request.user.email).first()
    
    if not profile:
        messages.warning(request, "कृपया पहले अपना बायोडाटा जोड़ें।")
        return redirect('biodata_create')

    # Pass the 'profile' to the template
    return render(request, 'memberProfileDetail.html', {'profile': profile})

  
  
# --- Static / Simple Page Views ---

def search_page(request):
    return render(request, 'SearchResult.html')

def account_settings(request):
    # This is the one causing the error!
    return render(request, 'accountSetting.html')

def chats(request):
    return render(request, 'chats.html')

 
def premium_plan(request):
    return render(request, 'premiumPlan.html')

def register(request):
    return render(request, 'registration.html')    
    
    
    
    
# 1. Search Results: Logic to filter profiles based on user input
def search_page(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = CommunityBiodata.objects.filter(
            Q(full_name__icontains=query) | 
            Q(gotra__icontains=query) | 
            Q(district__icontains=query),
            is_active=True
        )
    return render(request, 'SearchResult.html', {'results': results, 'query': query})

# 2. Premium Plans: Static data for your membership tiers
def premium_plan(request):
    plans = [
        {'name': 'Basic', 'price': 'Free', 'features': ['View 5 Profiles', 'Basic Search']},
        {'name': 'Gold', 'price': '₹499', 'features': ['Unlimited Profiles', 'Contact Details', 'Verified Badge']},
    ]
    return render(request, 'premiumPlan.html', {'plans': plans})

# 3. Chats: Requires login to protect community privacy


@login_required
def chats(request):
    # Fetch all users the current user has interacted with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    contact_ids = set(list(sent_to) + list(received_from))
    contacts = get_user_model().objects.filter(id__in=contact_ids)

    # Logic for a specific conversation
    receiver_id = request.GET.get('user_id')
    active_chat_messages = []
    receiver_user = None

    if receiver_id:
        receiver_user = get_object_or_404(get_user_model(), id=receiver_id)
        active_chat_messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver_user)) |
            (Q(sender=receiver_user) & Q(receiver=request.user))
        )
        # Mark as read
        active_chat_messages.filter(receiver=request.user).update(is_read=True)

    # Handle sending a message
    if request.method == 'POST' and receiver_user:
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver_user, content=content)
            return redirect(f"/biodata/chats/?user_id={receiver_id}")

    return render(request, 'chats.html', {
        'contacts': contacts,
        'messages': active_chat_messages,
        'receiver_user': receiver_user
    })











# from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Q
# from django.core.paginator import Paginator
# from django.views.generic import TemplateView # Kept if you still want to use it, but functions are below
# from .models import CommunityBiodata
# from .forms import CommunityBiodataForm
# import urllib.parse

 

# from django.http import JsonResponse
# from django.shortcuts import render
# import urllib



# # --- Functional Views (Logic) ---

# def home(request):
#     return render(request, 'index.html')

# def biodata_list(request):
#     profiles = CommunityBiodata.objects.all().order_by('-id')  
    
#     search_query = request.GET.get('search', '')
#     gotra_filter = request.GET.get('gotra', '')

#     if search_query:
#         profiles = profiles.filter(
#             Q(full_name__icontains=search_query) | 
#             Q(serial_number__icontains=search_query)
#         )
    
#     if gotra_filter:
#         profiles = profiles.filter(gotra__icontains=gotra_filter)

#     paginator = Paginator(profiles, 12)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'profiles': page_obj,
#         'search_query': search_query,
#         'gotra_filter': gotra_filter
#     }
#     return render(request, 'biodata_list.html', context)

# def biodata_detail(request, pk):
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
    
#     share_text = f"""*गोंडवाना वैवाहिक ग्रुप (नि:शुल्क बायोडाटा)*
# *सरल क्रमांक {profile.serial_number}*
# ▶️ नाम :- {profile.full_name}
# ▶️ जाति :- {profile.caste}
# ▶️ गोत्र :- {profile.gotra}
# ▶️ देव संख्या :- {profile.deity_number}
# ▶️ पिता का नाम :- {profile.father_name}
# ▶️ माता का नाम :- {profile.mother_name}
# ▶️ रंग :- {profile.complexion}
# ▶️ कद :- {profile.height}
# ▶️ जन्मतिथि :- {profile.date_of_birth}
# ▶️ मामा का गोत्र :- {profile.maternal_uncle_gotra}
# ▶️ शिक्षा :- {profile.education}
# ▶️ व्यवसाय :- {profile.occupation}
# ▶️ पारिवारिक स्थिति :- {profile.family_status}
# ▶️ पता :- {profile.address}
# *(संपर्क के लिए एडमिन से बात करें)*"""
    
#     whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

#     return render(request, 'biodata_detail.html', {
#         'profile': profile,
#         'whatsapp_url': whatsapp_url
#     })

# def biodata_create(request):
#     if request.method == 'POST':
#         form = CommunityBiodataForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('biodata_list') 
#     else:
#         form = CommunityBiodataForm()
    
#     return render(request, 'biodata_form.html', {'form': form})

 
# def biodata_matching(request, pk):
#     # Get the base profile to find matches for
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
    
#     suggestions = CommunityBiodata.objects.exclude(
#         Q(gotra=profile.gotra) | Q(pk=profile.pk)
#     ).order_by('?')[:6]  # Randomly pick 6 compatible profiles

#     return render(request, 'biodata_matching.html', {
#         'base_profile': profile,
#         'suggestions': suggestions
#     })
    
     

# # --- Simple Page Views (Static Renders) ---
# def search_page(request):
#     return render(request, 'SearchResult.html')

# def account_settings(request):
#     return render(request, 'accountSetting.html')

# def biodata_card(request):
#     return render(request, 'biodata_card.html')

# def chats(request):
#     return render(request, 'chats.html')

# def member_profile_detail(request):
#     return render(request, 'memberProfileDetail.html')

# def premium_plan(request):
#     return render(request, 'premiumPlan.html')

# def register(request):
#     return render(request, 'registration.html')

# def dashboard(request):
#     return render(request, 'userDashboard.html')

















# from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Q
# from django.core.paginator import Paginator
# from .models import CommunityBiodata
# from .forms import CommunityBiodataForm
# import urllib.parse
# def home(request):
#     return render(request, 'index.html')

# def biodata_list(request):
#     profiles = CommunityBiodata.objects.all()
    
#     search_query = request.GET.get('search', '')
#     gotra_filter = request.GET.get('gotra', '')

#     if search_query:
#         profiles = profiles.filter(
#             Q(full_name__icontains=search_query) | 
#             Q(serial_number__icontains=search_query)
#         )
    
#     if gotra_filter:
#         profiles = profiles.filter(gotra__icontains=gotra_filter)

#     paginator = Paginator(profiles, 12)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'profiles': page_obj,
#         'search_query': search_query,
#         'gotra_filter': gotra_filter
#     }
#     return render(request, 'biodata_list.html', context)

# # 2. Detail View
# def biodata_detail(request, pk):
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
    
#     share_text = f"""*गोंडवाना वैवाहिक ग्रुप (नि:शुल्क बायोडाटा)*
# *सरल क्रमांक {profile.serial_number}*
# ▶️ नाम :- {profile.full_name}
# ▶️ जाति :- {profile.caste}
# ▶️ गोत्र :- {profile.gotra}
# ▶️ देव संख्या :- {profile.deity_number}
# ▶️ पिता का नाम :- {profile.father_name}
# ▶️ माता का नाम :- {profile.mother_name}
# ▶️ रंग :- {profile.complexion}
# ▶️ कद :- {profile.height}
# ▶️ जन्मतिथि :- {profile.date_of_birth}
# ▶️ मामा का गोत्र :- {profile.maternal_uncle_gotra}
# ▶️ शिक्षा :- {profile.education}
# ▶️ व्यवसाय :- {profile.occupation}
# ▶️ पारिवारिक स्थिति :- {profile.family_status}
# ▶️ पता :- {profile.address}
# *(संपर्क के लिए एडमिन से बात करें)*"""
    
#     whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

#     return render(request, 'biodata_detail.html', {
#         'profile': profile,
#         'whatsapp_url': whatsapp_url
#     })

# # 3. Create View (UPDATED)
# def biodata_create(request):
#     if request.method == 'POST':
#         # MUST INCLUDE request.FILES here
#         form = CommunityBiodataForm(request.POST, request.FILES) 
#         if form.is_valid():
#             form.save()
#             return redirect('biodata_list')
#     else:
#         form = CommunityBiodataForm()
    
#     return render(request, 'biodata_form.html', {'form': form})


 

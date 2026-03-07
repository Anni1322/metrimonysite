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
from django.http import HttpResponseForbidden

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
    return redirect('pages_index')



# --- READ: Home & List View ---

def home(request):
    # Fetch recent profiles for the home page
    recent_profiles = CommunityBiodata.objects.filter(is_active=True).order_by('-created_at')[:4]
    return render(request, 'index.html', {'recent_profiles': recent_profiles})

# @login_required
# def biodata_list(request):
#     profiles = CommunityBiodata.objects.filter(is_active=True).order_by('-id')  
    
#     search_query = request.GET.get('search', '')
#     gotra_filter = request.GET.get('gotra', '')

#     if search_query:
#         profiles = profiles.filter(
#             Q(full_name__icontains=search_query) | 
#             Q(serial_number__icontains=search_query) |
#             Q(district__icontains=search_query)
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
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CommunityBiodata

def biodata_list(request):
    # Capture all search and filter parameters
    search_query = request.GET.get('search', '')
    gotra_query = request.GET.get('gotra', '')
    district_query = request.GET.get('district', '')
    caste_query = request.GET.get('caste', '')

    # Base Queryset
    profiles_list = CommunityBiodata.objects.filter(is_active=True)

    # Filtering Logic
    if search_query:
        profiles_list = profiles_list.filter(
            Q(full_name__icontains=search_query) | 
            Q(serial_number__icontains=search_query)
        )
    if gotra_query:
        profiles_list = profiles_list.filter(gotra__icontains=gotra_query)
    if district_query:
        profiles_list = profiles_list.filter(district=district_query)
    if caste_query:
        profiles_list = profiles_list.filter(caste=caste_query)

    # Pagination
    paginator = Paginator(profiles_list, 12)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)

    # Passing choices to template for the dropdowns
    context = {
        'profiles': profiles,
        'search_query': search_query,
        'gotra_filter': gotra_query,
        'district_filter': district_query,
        'caste_filter': caste_query,
        'DISTRICT_CHOICES': CommunityBiodata.DISTRICT_CHOICES,
        'CASTE_CHOICES': CommunityBiodata.CASTE_CHOICES,
    }
    
    return render(request, 'biodata_list.html', context)



# --- CREATE: Add New Biodata ---
# @login_required
def biodata_create(request):
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES)
        if form.is_valid():
            biodata = form.save(commit=False)
            biodata.user = request.user   # Important
            biodata.save()
            return redirect('pages_member_profile_detail')
    else:
        form = CommunityBiodataForm()
    return render(request, 'biodata_form.html', {'form': form})



# --- UPDATE: Edit Existing Biodata ---
def biodata_update(request, pk):
    obj = get_object_or_404(CommunityBiodata, pk=pk)
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('biodata_detail', pk=obj.pk)
    else:
        form = CommunityBiodataForm(instance=obj)
    return render(request, 'biodata_form.html', {'form': form})


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
    
    # Calculate Age for the share text
    age = ""
    if profile.date_of_birth:
        age = f"({datetime.date.today().year - profile.date_of_birth.year} वर्ष)"

    # Updated text to include ALL relevant community and physical fields
    share_text = f"""*जनजाति वैवाहिक समूह (नि:शुल्क बायोडाटा)*
*सरल क्रमांक: {profile.serial_number}*
---------------------------------------
▶️ नाम: {profile.full_name} {age}
▶️ लिंग: {profile.get_gender_display()}
▶️ जन्मतिथि: {profile.date_of_birth}
▶️ जन्म समय: {profile.birth_time.strftime('%I:%M %p') if profile.birth_time else 'N/A'}
▶️ कद: {profile.get_height_display() or 'N/A'}
▶️ रक्त समूह: {profile.blood_group or 'N/A'}
▶️ वैवाहिक स्थिति: {profile.get_marital_status_display()}
▶️ जाति/गोत्र: {profile.get_caste_display()} / {profile.get_gotra_display()}
▶️ देव संख्या: {profile.deity_number}
▶️ मामा गोत्र: {profile.maternal_uncle_gotra}
▶️ शिक्षा: {profile.get_education_display() or profile.education}
▶️ व्यवसाय: {profile.get_occupation_display()}
▶️ वार्षिक आय: {profile.get_annual_income_display() if hasattr(profile, 'get_annual_income_display') else 'N/A'}
▶️ स्थान: {profile.city}, {profile.get_district_display()} ({profile.state})
---------------------------------------
*(संपर्क हेतु एडमीन से संपर्क करें)*"""
    
    # URL Encoding for WhatsApp
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

    return render(request, 'biodata_detail.html', {
        'profile': profile,
        'whatsapp_url': whatsapp_url,
        'target_user': target_user,
    })

# user profile

@login_required
def user_profile_settings(request):
    profile = CommunityBiodata.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = CommunityBiodataForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            biodata = form.save(commit=False)
            biodata.user = request.user
            biodata.save()

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
# def dashboard(request):
#     # Fetch all profiles (including inactive ones) for management
#     profiles_list = CommunityBiodata.objects.all().order_by('-id')
    
#     # Search logic for the dashboard table
#     query = request.GET.get('q')
#     if query:
#         profiles_list = profiles_list.filter(
#             Q(full_name__icontains=query) | Q(serial_number__icontains=query)
#         )

#     # Statistics
#     stats = {
#         'total': CommunityBiodata.objects.count(),
#         'active': CommunityBiodata.objects.filter(is_active=True).count(),
#         'inactive': CommunityBiodata.objects.filter(is_active=False).count(),
#     }

#     return render(request, 'userDashboard.html', {
#         'profiles': profiles_list,
#         'stats': stats
#     })




@login_required
def dashboard(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("आपको इस पेज को देखने की अनुमति नहीं है।")

    profiles_list = CommunityBiodata.objects.all().order_by('-id')

    query = request.GET.get('q')
    if query:
        profiles_list = profiles_list.filter(
            Q(full_name__icontains=query) |
            Q(serial_number__icontains=query)
        )

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

# def biodata_matching(request, pk):
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
    
#     # Exclude same gotra (community rule) and different gender
#     opposite_gender = 'F' if profile.gender == 'M' else 'M'
    
#     suggestions = CommunityBiodata.objects.filter(
#         gender=opposite_gender,
#         is_active=True
#     ).exclude(gotra=profile.gotra).order_by('?')[:6]

#     return render(request, 'biodata_matching.html', {
#         'base_profile': profile,
#         'suggestions': suggestions
#     })
 
 
 
# from django.db.models import Q, Case, When, Value, IntegerField
# from django.shortcuts import render, get_object_or_404
# from .models import CommunityBiodata
# import datetime

# def biodata_matching(request, pk):
#     # 1. Get the base profile
#     profile = get_object_or_404(CommunityBiodata, pk=pk)
#     # 2. Basic Requirements
#     opposite_gender = 'F' if profile.gender == 'M' else 'M'
    
#     # 3. Age Logic (Optional but recommended)
#     # Suggestions usually look for +/- 5 to 7 years of age
#     current_year = datetime.date.today().year
#     profile_age = current_year - profile.date_of_birth.year
    
#     # 4. Start Filtering
#     suggestions = CommunityBiodata.objects.filter(
#         is_active=True,
#         gender=opposite_gender,
#         caste=profile.caste  # Hard requirement: Same Caste
#     ).exclude(
#         gotra=profile.gotra  # Community Rule: Different Gotra
#     ).exclude(
#         pk=profile.pk        # Don't suggest self
#     )

#     # 5. Advanced Weightage Logic (Scoring)
#     # We use Case/When to "score" profiles so the best matches appear first
#     suggestions = suggestions.annotate(
#         match_score=Case(
#             # Priority 1: Same District (Score 10)
#             When(district=profile.district, then=Value(10)),
#             # Priority 2: Similar Education Level (Score 5)
#             When(education=profile.education, then=Value(5)),
#             # Priority 3: Same State (Score 3)
#             When(state=profile.state, then=Value(3)),
#             default=Value(0),
#             output_field=IntegerField(),
#         )
#     )

#     # 6. Refine by Age (Strict filtering is risky, so we just prioritize)
#     if profile.gender == 'M':
#         # Men usually look for same age or younger
#         suggestions = suggestions.filter(
#             date_of_birth__year__gte=profile.date_of_birth.year - 2, # Max 2 years older
#             date_of_birth__year__lte=profile.date_of_birth.year + 10 # Up to 10 years younger
#         )
#     else:
#         # Women usually look for same age or older
#         suggestions = suggestions.filter(
#             date_of_birth__year__lte=profile.date_of_birth.year + 2, # Max 2 years younger
#             date_of_birth__year__gte=profile.date_of_birth.year - 10 # Up to 10 years older
#         )

#     # 7. Order by Score (Highest first) then Randomize to keep it fresh
#     suggestions = suggestions.order_by('-match_score', '?')[:8]

#     return render(request, 'biodata_matching.html', {
#         'base_profile': profile,
#         'suggestions': suggestions,
#         'match_count': suggestions.count()
#     }) 
    
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CommunityBiodata

@login_required
def biodata_matching(request, pk):
    # 1. Get the current user's profile
    profile = get_object_or_404(CommunityBiodata, pk=pk)
    user_profile = CommunityBiodata.objects.filter(user=request.user).first()
    
    if not user_profile:
        # If the user hasn't created a biodata yet, show an empty state or redirect
        return render(request, 'biodata_matching.html', {'no_profile': True})

    # 2. Matching Logic
    opposite_gender = 'F' if user_profile.gender == 'M' else 'M'
    
    matches = CommunityBiodata.objects.filter(
        caste=user_profile.caste,      # Same Caste
        gender=opposite_gender,         # Opposite Gender
        is_active=True
    ).exclude(
        gotra=user_profile.gotra       # Different Gotra (Rule)
    ).order_by('-created_at')

    return render(request, 'biodata_matching.html', {
        'user_profile': user_profile,
        'matches': matches,
        'match_count': matches.count()
    })    
    
    

def success_stories(request):
    stories = SuccessStory.objects.filter(is_verified=True).order_by('-wedding_date')
    return render(request, 'successstory.html', {'stories': stories})



@login_required
def member_profile_detail(request):
    profile = CommunityBiodata.objects.filter(user=request.user).first()
    if not profile:
        messages.warning(request, "कृपया पहले अपना बायोडाटा जोड़ें।")
        return redirect('biodata_create')
    return render(request, 'memberProfileDetail.html', {
        'profile': profile
    })

  
  
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
    
#     share_text = f"""*जनजाति वैवाहिक समूह (नि:शुल्क बायोडाटा)*
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
    
#     share_text = f"""*जनजाति वैवाहिक समूह (नि:शुल्क बायोडाटा)*
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


 

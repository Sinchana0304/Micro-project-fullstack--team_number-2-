from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, DisasterForm
from .models import User, Disaster
from .models import User, Disaster, Donation, Message, Feedback
from .forms import UserRegistrationForm, DisasterForm, DonationForm
from .forms import MessageForm, FeedbackForm
from django.db.models import Avg

# ----------------------------
# Role Selection and Registration
# ----------------------------

def choose_role(request):
    return render(request, 'core/choose_role.html')

def register(request):
    role = request.POST.get('role') or request.GET.get('role')
    if role not in ['organiser', 'donor']:
        return redirect('choose_role')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            password = form.cleaned_data.get('password1')

            if role == 'organiser' and not password.startswith('admin'):
                form.add_error('password1', "Organiser password must start with 'admin'")
            else:
                user.set_password(password)
                user.save()
                login(request, user)

                if user.role == 'organiser':
                    return redirect('organiser_dashboard')
                elif user.role == 'donor':
                    return redirect('donor_dashboard')
                else:
                    return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {
        'form': form,
        'role': role,
        'role_display': dict(User.ROLE_CHOICES).get(role, role).title()
    })

# ----------------------------
# Role-Based Dashboard Routing
# ----------------------------

@login_required
def dashboard(request):
    if request.user.role == 'organiser':
        return redirect('organiser_dashboard')
    elif request.user.role == 'donor':
        return redirect('donor_dashboard')
    else:
        return redirect('login')

# ----------------------------
# Organiser Dashboard
# ----------------------------

@login_required
def organiser_dashboard(request):
    if request.user.role != 'organiser':
        return redirect('dashboard')

    disasters = Disaster.objects.filter(organiser=request.user)
    active_disasters = disasters.filter(urgency_level='high')
    donations = Donation.objects.filter(disaster__organiser=request.user)
    feedbacks = Feedback.objects.filter(organiser=request.user)
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']

    context = {
        'disasters': disasters,
        'active_count': active_disasters.count(),
        'total_count': disasters.count(),
        'donation_count': donations.count(),
        'volunteer_count': 5,  # Placeholder
        'avg_rating': round(avg_rating or 0, 1),
        'feedbacks': feedbacks,
    }
    return render(request, 'core/organiser_dashboard.html', context)

# ----------------------------
# Donor Dashboard
# ----------------------------

@login_required
def donor_dashboard(request):
    # Ensure only donors access this view
    if request.user.role != 'donor':
        return redirect('dashboard')

    # Load all disasters for donor to view and act on
    disasters = Disaster.objects.all().order_by('-posted_at')

    # Load donor's donation history
    donations = Donation.objects.filter(donor=request.user).order_by('-donated_at')

    # Optional: preload messages or feedback if needed later
    # messages = Message.objects.filter(recipient=request.user)
    # feedbacks = Feedback.objects.filter(donor=request.user)

    return render(request, 'core/donor_dashboard.html', {
        'disasters': disasters,
        'donations': donations,
        # 'messages': messages,
        # 'feedbacks': feedbacks,
    })
# ----------------------------
# Disaster CRUD (Create, View, Edit, Delete)
# ----------------------------

@login_required
def post_disaster(request):
    if request.user.role != 'organiser':
        return redirect('dashboard')

    if request.method == 'POST':
        form = DisasterForm(request.POST, request.FILES)
        if form.is_valid():
            disaster = form.save(commit=False)
            disaster.organiser = request.user
            disaster.save()
            return redirect('organiser_dashboard')
    else:
        form = DisasterForm()

    return render(request, 'core/disaster_form.html', {
        'form': form,
        'mode': 'create'
    })

@login_required
def view_disaster(request, pk):
    disaster = get_object_or_404(Disaster, pk=pk, organiser=request.user)
    return render(request, 'core/disaster_form.html', {
        'disaster': disaster,
        'mode': 'view'
    })

@login_required
def edit_disaster(request, pk):
    disaster = get_object_or_404(Disaster, pk=pk, organiser=request.user)
    if request.method == 'POST':
        form = DisasterForm(request.POST, request.FILES, instance=disaster)
        if form.is_valid():
            form.save()
            messages.success(request, "Disaster updated successfully.")
            return redirect('organiser_dashboard')
    else:
        form = DisasterForm(instance=disaster)

    return render(request, 'core/disaster_form.html', {
        'form': form,
        'mode': 'edit'
    })

@login_required
def delete_disaster(request, pk):
    disaster = get_object_or_404(Disaster, pk=pk, organiser=request.user)
    if request.method == 'POST':
        disaster.delete()
        messages.success(request, "Disaster deleted successfully.")
        return redirect('organiser_dashboard')
    return render(request, 'core/disaster_form.html', {
        'disaster': disaster,
        'mode': 'delete'
    })




@login_required
def donate_to_disaster(request, pk):
    if request.user.role != 'donor':
        return redirect('dashboard')

    disaster = get_object_or_404(Disaster, pk=pk)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.disaster = disaster
            donation.save()
            messages.success(request, "Thank you for your donation!")
            return redirect('donor_dashboard')
    else:
        form = DonationForm()

    return render(request, 'core/donate.html', {
        'form': form,
        'disaster': disaster
    })

@login_required
def message_thread(request, disaster_id):
    disaster = get_object_or_404(Disaster, pk=disaster_id)
    messages_qs = Message.objects.filter(disaster=disaster).order_by('timestamp')

    # Determine recipient
    if request.user.role == 'donor':
        recipient = disaster.organiser
    else:
        # Show messages from all donors
        recipient = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.disaster = disaster
            message.save()
            return redirect('message_thread', disaster_id=disaster.id)
    else:
        form = MessageForm()

    return render(request, 'core/message_thread.html', {
        'disaster': disaster,
        'messages': messages_qs,
        'form': form
    })

@login_required
def submit_feedback(request, disaster_id):
    disaster = get_object_or_404(Disaster, pk=disaster_id)
    organiser = disaster.organiser

    if request.user.role != 'donor':
        return redirect('dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.donor = request.user
            feedback.organiser = organiser
            feedback.disaster = disaster
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('donor_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'core/submit_feedback.html', {
        'form': form,
        'disaster': disaster,
        'organiser': organiser
    })
from .models import Message

@login_required
def organiser_messages(request):
    if request.user.role != 'organiser':
        return redirect('dashboard')

    # Get all messages where the organiser is the recipient
    messages_qs = Message.objects.filter(recipient=request.user).order_by('-timestamp')

    return render(request, 'core/organiser_messages.html', {
        'messages': messages_qs
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disaster, Message
from .forms import MessageForm

@login_required
def message_thread(request, disaster_id):
    disaster = get_object_or_404(Disaster, pk=disaster_id)
    thread_messages = Message.objects.filter(disaster=disaster).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.disaster = disaster

            # ✅ Fix: Set recipient based on sender role
            if request.user.role == 'organiser':
                # Replying to donor
                last_msg = thread_messages.exclude(sender=request.user).last()
                msg.recipient = last_msg.sender if last_msg else None
            else:
                # Donor sending to organiser
                msg.recipient = disaster.organiser

            if msg.recipient:
                msg.save()
                messages.success(request, "Message sent.")
            else:
                messages.error(request, "Recipient could not be determined.")
            return redirect('message_thread', disaster_id=disaster.id)
    else:
        form = MessageForm()

    return render(request, 'core/message_thread.html', {
        'disaster': disaster,
        'messages': thread_messages,
        'form': form
    })

from .models import Feedback

@login_required
def organiser_feedback(request):
    if request.user.role != 'organiser':
        return redirect('dashboard')
    feedbacks = Feedback.objects.filter(organiser=request.user).order_by('-submitted_at')
    return render(request, 'core/organiser_feedback.html', {'feedbacks': feedbacks})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Donation, Disaster

@login_required
def organiser_donations(request):
    if request.user.role != 'organiser':
        return redirect('dashboard')

    disasters = Disaster.objects.filter(organiser=request.user)
    donations = Donation.objects.filter(disaster__organiser=request.user).order_by('-donated_at')

    return render(request, 'core/organiser_donations.html', {
        'donations': donations,
        'disasters': disasters,
        'donation_count': donations.count()
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Disaster, Donation
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Disaster, Donation

@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)  # ✅ Handle image uploads
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=user)

    context = {
        'form': form,
        'user': user
    }

    # Role-specific data
    if user.role == 'organiser':
        context['disasters'] = Disaster.objects.filter(organiser=user)
    elif user.role == 'donor':
        context['donations'] = Donation.objects.filter(donor=user)

    return render(request, 'core/user_profile.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Donation, Feedback, Message

@login_required
def donor_donations(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-donated_at')
    return render(request, 'core/donor_donations.html', {'donations': donations})

@login_required
def donor_feedback(request):
    feedbacks = Feedback.objects.filter(donor=request.user).order_by('-submitted_at')
    return render(request, 'core/donor_feedback.html', {'feedbacks': feedbacks})

@login_required
def donor_messages(request):
    messages_qs = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'core/donor_messages.html', {'messages': messages_qs})

from .forms import ManualDonationForm

@login_required
def donate_to_disaster(request, disaster_id):
    disaster = get_object_or_404(Disaster, pk=disaster_id)

    if request.method == 'POST':
        form = ManualDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.disaster = disaster
            donation.save()
            messages.success(request, "Thank you! Your donation has been recorded.")
            return redirect('donor_dashboard')
    else:
        form = ManualDonationForm()

    return render(request, 'core/manual_donation.html', {
        'disaster': disaster,
        'form': form
    })
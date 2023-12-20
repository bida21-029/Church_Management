from django.shortcuts import render,redirect

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm,LoginForm
from .models import Member, Event, Donation, Message
from .forms import MemberForm, EventForm, DonationForm, MessageForm
from django.contrib import messages





# Create your views here.
def home(request):
		return render(request, 'home.html', {})
        



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('church_app:home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('church_app:login')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

##############################
###########AUTO ADD TO MEMBER
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
#  signal to create a Member instance when a User is created
@receiver(post_save, sender=get_user_model())
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(
            user=instance,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
# Connect the signal
post_save.connect(create_member_profile, sender=get_user_model())

##############################
###########AUTO ADD TO PROFILE
from .models import Profile

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

# Connect the signal
post_save.connect(create_user_profile, sender=get_user_model())

########################
###########VIEW  AND EDIT PROFILE
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile_view.html', {'profile': profile})

####################################################
##########WHEN PROFILE UPDATED AUTO UPDATE MEMBER 
@receiver(post_save, sender=Profile)
def update_member(sender, instance, created, **kwargs):
    # If a Profile is created or updated, update the corresponding Member
    if created:
        member, created = Member.objects.get_or_create(user=instance.user)
    else:
        member = Member.objects.get(user=instance.user)

    member.first_name = instance.first_name
    member.last_name = instance.last_name
    member.birthdate = instance.birthdate
    member.category = instance.category
    member.phone_number = instance.phone_number
    member.email = instance.email
    member.save()


from .forms import ProfileForm  # Create this form in the next step

@login_required
def profile_edit(request,pk):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('church_app:profile_view')  # Redirect to the view profile page after successful update
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

#########################################
#####NEW MEMBER BY STAFF CAN ALSO LOGIN





##################################
#################LOGIN
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('church_app:staff_dashboard')
                else:
                    return redirect('church_app:member_dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def staff_dashboard(request):
    
    return render(request, 'staff_dashboard.html',{})

def member_dashboard(request):
    # Your staff dashboard logic here
    return render(request, 'member_dashboard.html',{})	


#####################################
####MEMBERS
@login_required
def member_list(request):
    members = Member.objects.all()
    return render(request, 'church_app/member_list.html', {'members': members})

@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'church_app/member_detail.html', {'member': member})

@login_required
def member_new(request):
    member = None

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, 'Member created successfully.')
            return redirect('church_app:member_detail', pk=member.pk)
    else:
        form = MemberForm()

    return render(request, 'church_app/member_new.html', {'form': form, 'member': member})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('church_app:member_detail', pk=pk)
    else:
        form = MemberForm(instance=member)

    return render(request, 'church_app/member_edit.html', {'form': form, 'member': member})

@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted successfully.')
        return redirect('church_app:member_list')
    return render(request, 'church_app/member_delete.html', {'member': member})


#####################################
##########################EVENT
def event_list(request):
    events = Event.objects.all()
    return render(request, 'church_app/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'church_app/event_detail.html', {'event': event})

@login_required
def event_new(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('church_app:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'church_app/event_edit.html', {'form': form})


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
 
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            # Add success message if needed
            return redirect('church_app:event_list')
    else:
        form = EventForm(instance=event)
 
    return render(request, 'church_app/event_edit.html', {'form': form, 'event': event})  

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
   
    if request.method == 'POST':
        event.delete()
        # Add success message if needed
        return redirect('church_app:event_list')
 
    return render(request, 'church_app/event_delete.html', {'event': event})      



#################################################
#####################DONATION
def donation_list(request):
    donations = Donation.objects.all()
    return render(request, 'church_app/donation_list.html', {'donations': donations})

def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'church_app/donation_detail.html', {'donation': donation})

@login_required
def donation_new(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            messages.success(request, 'Donation recorded successfully.')
            return redirect('church_app:donation_detail', pk=donation.pk)
    else:
        form = DonationForm()
    return render(request, 'church_app/donation_new.html', {'form': form})




#####################
############COMMUNICATION
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'church_app/message_list.html', {'messages': messages})

def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'church_app/message_detail.html', {'message': message})

@login_required
def message_new(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('church_app:message_detail', pk=message.pk)
    else:
        form = MessageForm()
    return render(request, 'church_app/message_new.html', {'form': form})




##################################################################
##########################UPCOMING BIRTHDAYS
from django.views.generic import ListView
from django.utils import timezone
from .models import Member

def upcoming_birthdays(request):
    today = date.today()
    upcoming_birthdays = Member.objects.filter(
        birthdate__month=today.month,
        birthdate__day__gte=today.day
    ).order_by('birthdate')
    return render(request, 'church_app:upcoming_birthdays.html', {'upcoming_birthdays': upcoming_birthdays})


##################################################
##################UPCOMING EVENTS
from django.shortcuts import render
from .models import Event
from datetime import date

def upcoming_events(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')[:10]  # Adjust the number of events to display as needed
    return render(request, 'church_app/upcoming_events.html', {'upcoming_events': upcoming_events})

@login_required
def upcoming_birthdays(request):
    today = datetime.today()
    upcoming_birthdays = CustomUser.objects.filter(
        birth_date__month=today.month,
        birth_date__day__gte=today.day
    ).order_by('birth_date__day')
 
    context = {'church_app/upcoming_birthdays': upcoming_birthdays}
    return render(request, 'church_app/upcoming-birthdays.html', context)

def donation_history(request):
    # Fetch all donations
    donations = Donation.objects.all()

    # Calculate total donation amount
    total_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum']
    print(donations)  # Add this line
    return render(request, 'church_app/donation_history.html', {
        'donations': donations,
        'total_amount': total_amount,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Appointment


def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)
    other_services = Service.objects.exclude(pk=service.pk)[:4]
    
    context = {
        'service': service,
        'other_services': other_services,
    }
    return render(request, 'services/service_detail.html', context)


@login_required
def book_service_view(request, slug=None):
    selected_service = None
    if slug:
        selected_service = get_object_or_404(Service, slug=slug)
    
    services = Service.objects.all()

    # Pre-fill user information
    initial_user = {
        'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'email': request.user.email,
        'phone': '',
    }
    if hasattr(request.user, 'profile') and request.user.profile.phone:
        initial_user['phone'] = request.user.profile.phone

    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        vehicle_model = request.POST.get('vehicle_model', '').strip()
        vehicle_reg = request.POST.get('vehicle_reg_number', '').strip()
        preferred_date = request.POST.get('preferred_date', '').strip()
        preferred_time = request.POST.get('preferred_time', '').strip()
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        notes = request.POST.get('notes', '').strip()

        if not (vehicle_model and preferred_date and preferred_time and customer_name and customer_email and customer_phone):
            messages.error(request, "Please fill in all required appointment fields.")
        else:
            appointment = Appointment.objects.create(
                user=request.user,
                service=service,
                vehicle_model=vehicle_model,
                vehicle_reg_number=vehicle_reg,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                notes=notes,
                status='Pending'
            )
            messages.success(request, f"Appointment #{appointment.appointment_id} scheduled! We look forward to servicing your {vehicle_model}.")
            return redirect('services:confirmation', appointment_id=appointment.appointment_id)

    context = {
        'selected_service': selected_service,
        'services': services,
        'initial_user': initial_user,
    }
    return render(request, 'services/book_service.html', context)


@login_required
def appointment_confirmation_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, user=request.user)
    return render(request, 'services/appointment_confirmation.html', {'appointment': appointment})


@login_required
def appointment_history_view(request):
    appointments = Appointment.objects.filter(user=request.user).select_related('service')
    return render(request, 'services/appointment_history.html', {'appointments': appointments})


@login_required
def cancel_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, user=request.user)
    if appointment.status in ['Pending', 'Confirmed']:
        appointment.status = 'Cancelled'
        appointment.save()
        messages.info(request, f"Appointment #{appointment.appointment_id} has been cancelled.")
    else:
        messages.warning(request, f"Appointment status is already {appointment.status}.")
    return redirect('services:history')

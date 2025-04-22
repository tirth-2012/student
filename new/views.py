from django.db.models import Q,Sum,F
from django.shortcuts import render,redirect,get_object_or_404
from .models import studentdata,fees,attendance,Note
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        # Validation
        if not username or not email or not password or not confirm_password:
            errors.append("All fields are required!")
        if password != confirm_password:
            errors.append("Passwords do not match!")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists!")

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return JsonResponse({"success": True})

    return render(request, "register.html")

# User Login (Without Forms)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "errors": "Invalid username or password!"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login_view')


def index(request):
    posts=studentdata.objects.all()
    return render(request,'index.html',{'posts': posts})

@login_required(login_url='login_view')
def addstudent(request):
    if request.method == 'POST':
        s=studentdata()
        s.fname=request.POST.get('fname')
        s.mname=request.POST.get('mname')
        s.lname=request.POST.get('lname')
        s.gender=request.POST.get('gender')
        s.email=request.POST.get('email')
        s.phone=request.POST.get('phone')
        s.city=request.POST.get('city')
        s.address=request.POST.get('address')
        s.coures=request.POST.get('coures')
        s.amount=request.POST.get('amount')
        s.admission_date=request.POST.get('admission_date')
        s.image=request.FILES.get('image')
        s.save()
        return redirect(showlist)
    else:
        return render(request,'addstudent.html')
    
@login_required(login_url='login_view')
def showlist(request):
    s = studentdata.objects.annotate(
        total_fees_paid=Sum('fees__payment'),
        remaining_fees=F('amount') - Sum('fees__payment')
    )
    return render(request,'showlist.html',{'s':s})

@login_required(login_url='login_view') 
def editstudent(request,pk):
    s=get_object_or_404(studentdata,pk=pk)
    if request.method == 'POST':
        s.fname=request.POST.get('fname')
        s.mname=request.POST.get('mname')
        s.lname=request.POST.get('lname')
        s.gender=request.POST.get('gender')
        s.email=request.POST.get('email')
        s.phone=request.POST.get('phone')
        s.city=request.POST.get('city')
        s.address=request.POST.get('address')
        s.coures=request.POST.get('coures')
        s.amount=request.POST.get('amount')
        s.admission_date=request.POST.get('admission_date')
        if request.FILES.get('image'):
            s.image = request.FILES.get('image')
        s.save()
        return redirect(showlist)
    else:
        posts=studentdata.objects.all()
        return render(request,'editstudent.html',{'s':s,'posts':posts})
 
@login_required(login_url='login_view')   
def deletestudent(request,pk):
    s=get_object_or_404(studentdata,pk=pk)
    s.delete()
    return redirect(showlist)

@login_required(login_url='login_view')
def searchlist(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        s = studentdata.objects.filter(
            Q(fname__icontains=query) |
            Q(mname__icontains=query) |
            Q(lname__icontains=query)
        )

    else:
        s = studentdata.objects.all()  # Fetch all students if no query
    return render(request, 'showlist.html', {'s': s, 'query': query})

@login_required(login_url='login_view')
def addpayment(request):
    if request.method == 'POST':
        f=fees()
        sa= request.POST.get('student')
        student = get_object_or_404(studentdata, pk=sa)
        f.student=student
        f.payment=request.POST.get('payment')
        f.date_paid=request.POST.get('date_paid')
        f.take=request.POST.get('take')
        f.pay_method=request.POST.get('pay_method')
        f.save()
        return redirect(paymentshowlist)
    else:
        students = studentdata.objects.annotate(
            total_paid=Sum('fees__payment')  # Calculate the total amount paid by each student
        ).filter(
            # total_paid__isnull=True,  # Students with no payments
            #total_paid__lt=F('amount')
            Q(total_paid__lt=F('amount')) | Q(total_paid__isnull=True)
        )
        return render(request,'addpayment.html',{'s':students})

@login_required(login_url='login_view')
def paymentshowlist(request):
    # Get the date range from the request
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Start with all payment records
    posts = fees.objects.all()

    # Filter based on the date range if provided
    if from_date and to_date:
        posts = posts.filter(date_paid__range=[from_date, to_date])
    elif from_date:  # Filter from a specific date
        posts = posts.filter(date_paid__gte=from_date)
    elif to_date:  # Filter up to a specific date
        posts = posts.filter(date_paid__lte=to_date)

    return render(request, 'paymentdetail.html', {'posts': posts, 'from_date': from_date, 'to_date': to_date})

@login_required(login_url='login_view')
def searchpay(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        s = studentdata.objects.filter(
            Q(fname__icontains=query) |
            Q(mname__icontains=query) |
            Q(lname__icontains=query)
        )

    else:
        s = fees.objects.all()  # Fetch all students if no query
    return render(request, 'payment.html', {'s': s, 'query': query})


@login_required(login_url='login_view')
def attendance_view(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('students')  # Get selected student IDs
        date = request.POST.get('date')
        status = request.POST.get('status')

        all_students = studentdata.objects.all()  # Fetch all students
        
        for student in all_students:
            # If the student is in the selected list, mark as Present
            if str(student.id) in selected_students:
                attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={"status": "Present"}
                )
            else:
                # If the student is NOT selected, mark as Absent
                attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={"status": "Absent"}
                )

        return redirect(attendance_view)
        
    # Filter attendance by selected date
    filter_date = request.GET.get('filter_date')
    if filter_date:
        att = attendance.objects.filter(date=filter_date).order_by('-date')
    else:
        att = attendance.objects.all().order_by('-date')

    student = studentdata.objects.all()  # Fetch all students

    return render(request, 'attendance.html', {
        'student': student,
        'att': att,
        'filter_date': filter_date,
    })


@login_required(login_url='login_view')
def show(request, pk):
    student = get_object_or_404(studentdata, id=pk)  # Get the student
    payment=fees.objects.filter(student=student)
    att = attendance.objects.filter(student=student)  # Get attendance

    return render(request, 'onlyview.html', {'s': student,'att':att,'payment':payment})

@login_required(login_url='login_view')
def note(request):
    return render(request,'note.html')

@login_required(login_url='login_view')
def attendancelist(request):
    query = request.GET.get('search', '').strip()  # Get search query
    filter_date = request.GET.get('filter_date', '').strip()  # Get filter date
    
    # Get all attendance records for the student, ordered by latest date
    att = attendance.objects.all().order_by('-date')

    # Apply search filter (if query exists)
    if query:
        att = att.filter(
            Q(student__fname__icontains=query) |
            Q(student__mname__icontains=query) |
            Q(student__lname__icontains=query)
        )

    # Apply date filter (if date exists)
    if filter_date:
        att = att.filter(date=filter_date)

    return render(request, 'attendancelist.html', {'att': att, 'query': query,})

@login_required(login_url='login_view')
def note_view(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            # Save the note to the database
            Note.objects.create(content=content)
            return redirect('note_view')  # Redirect to avoid form resubmission

    # If DELETE method, delete the note
    if request.method == "DELETE":
        note_id = request.POST.get('note_id')
        if note_id:
            note = get_object_or_404(Note, id=note_id)
            note.delete()
            return HttpResponse("Note deleted", status=200)

    # Get all notes from the database
    notes = Note.objects.all()

    return render(request, 'note_template.html', {'notes': notes})


    
    
    
    
   
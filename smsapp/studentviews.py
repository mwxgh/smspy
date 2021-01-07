import datetime
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from smsapp.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, FeedbackStudents, LeaveReportStudents


def Home(request):
    getstudent = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=getstudent).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=getstudent, status=True).count()
    attendance_present = AttendanceReport.objects.filter(student_id=getstudent, status=False).count()
    getcourse = Courses.objects.get(id=getstudent.course_id.id)
    getsubject = Subjects.objects.filter(course_id=getcourse).count()

    subject_name = []
    data_absent = []
    data_present = []
    subject_data = Subjects.objects.filter(course_id=getstudent.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=getstudent.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=getstudent.id).count()
        subject_name.append(subject.name)
        data_absent.append(attendance_absent_count)
        data_present.append(attendance_present_count)
    return render(request, 'student/home.html', {'total_attendance': attendance_total, 'absent_attendance': attendance_absent, 'present_attendance': attendance_present, 'subjects': getsubject, 'data_name': subject_name, 'data1': data_present, 'data2': data_absent})


def Profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request, 'student/profile.html', {'user': user, 'student': student})


def EditProfile(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        getfirstname = request.POST.get('firstname')
        getlastname = request.POST.get('lastname')
        getaddress = request.POST.get('address')
        getpassword = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = getfirstname
            customuser.last_name = getlastname
            if getpassword != None and getpassword != '':
                customuser.set_password(getpassword)
            customuser.save()
            student = Students.objects.get(admin=customuser.id)
            student.address = getaddress
            student.save()
            messages.success(request, 'Successfully Updated Profile')
            return HttpResponseRedirect(reverse('studentprofile'))
        except Exception:
            messages.error(request, 'Failed to Update Profile')
            return HttpResponseRedirect(reverse('studentprofile'))


def ViewAttendance(request):
    get_student = Students.objects.get(admin=request.user.id)
    get_course = get_student.course_id
    get_subject = Subjects.objects.filter(course_id=get_course)
    return render(request, 'student/viewattendance.html', {'subjects': get_subject})


def ViewAttendancePost(request):
    get_subject = request.POST.get('subject')
    get_start = request.POST.get('startdate')
    get_end = request.POST.get('enddate')

    start_data_parse = datetime.datetime.strptime(get_start, "%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(get_end, "%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=get_subject)
    user_obj = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(admin=user_obj)

    attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse, end_data_parse), subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)
    return render(request, 'student/attendancedata.html', {'attendance_reports': attendance_reports})


def ApplyLeave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudents.objects.filter(student_id=student_obj)
    return render(request, 'student/applyleave.html', {'leave_data': leave_data})


def DoApplyLeave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("studentapplyleave"))
    else:
        get_leavedate = request.POST.get('leavedate')
        get_leavereason = request.POST.get('leavemsg')
        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudents(student_id=student_obj, leave_date=get_leavedate, leave_message=get_leavereason, leave_status=0)
            leave_report.save()
            messages.success(request, 'Successfully Applied for Leave')
            return HttpResponseRedirect(reverse('studentapplyleave'))
        except Exception:
            messages.error(request, 'Failed to Apply for Leave')
            return HttpResponseRedirect(reverse('studentapplyleave'))


def Feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudents.objects.filter(student_id=student_obj)
    return render(request, 'student/feedback.html', {'feedback_data': feedback_data})


def DoFeedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("studentfeedback"))
    else:
        get_feedback = request.POST.get('feedbackmsg')
        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedbackStudents(student_id=student_obj, feedback=get_feedback, feedback_reply="")
            feedback.save()
            messages.success(request, 'Successfully Sent Feedback')
            return HttpResponseRedirect(reverse('studentfeedback'))
        except Exception:
            messages.error(request, 'Failed to Send Feedback')
            return HttpResponseRedirect(reverse('studentfeedback'))

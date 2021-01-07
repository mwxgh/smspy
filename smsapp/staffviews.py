import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from smsapp.models import Subjects, SessionYear, Courses, Students, CustomUser, Attendance, AttendanceReport, FeedbackStaffs, LeaveReportStaffs, Staffs
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def Home(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
# fetch all student on staff
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    final_course = []
# remove duplicate course ID to count student
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    student_count = Students.objects.filter(course_id__in=final_course).count()
# fetch attendance count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
# fetch approve leave count
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
# fetch subject
    subject_count = subjects.count()


# fetch attendance by subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.name)
        attendance_list.append(attendance_count1)


# fetch student
    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
    return render(request, 'staff/home.html', {'student_count': student_count, 'total_attendance': attendance_count, 'total_leave': leave_count, 'total_subject': subject_count, 'subject_list': subject_list, 'attendance_list': attendance_list, "student_list": student_list, "present_list": student_list_attendance_present, "absent_list": student_list_attendance_absent})


def Profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    return render(request, 'staff/profile.html', {'user': user, 'staff': staff})


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
            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = getaddress
            staff.save()
            messages.success(request, 'Successfully Updated Profile')
            return HttpResponseRedirect(reverse('staffprofile'))
        except Exception:
            messages.error(request, 'Failed to Update Profile')
            return HttpResponseRedirect(reverse('staffprofile'))


def TakeAttendance(request):
    get_subjects = Subjects.objects.filter(staff_id=request.user.id)
    get_sessions = SessionYear.objects.all()
    return render(request, 'staff/takeattendance.html', {'subjects': get_subjects, 'sessions': get_sessions})


@ csrf_exempt
def GetStudent(request):
    get_subject = request.POST.get('subject')
    get_session = request.POST.get('session')

    subject = Subjects.objects.get(id=get_subject)
    session_model = SessionYear.objects.get(id=get_session)
    get_students = Students.objects.filter(course_id=subject.course_id, session_id=session_model)
    list_data = []
    for student in get_students:
        data_element = {'id': student.admin.id, 'name': student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_element)
    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


@ csrf_exempt
def SaveAttendance(request):
    student_ids = request.POST.get("student_ids")
    get_subject = request.POST.get("subject_id")
    get_attendance_date = request.POST.get("attendance_date")
    get_session = request.POST.get("session_id")

    subject_model = Subjects.objects.get(id=get_subject)
    session_model = SessionYear.objects.get(id=get_session)
    json_student = json.loads(student_ids)

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=get_attendance_date, session_id=session_model)
        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except Exception:
        return HttpResponse("ERROR")


def UpdateAttendance(request):
    get_subjects = Subjects.objects.filter(staff_id=request.user.id)
    get_sessions = SessionYear.objects.all()
    return render(request, "staff/updateattendance.html", {'subjects': get_subjects, "sessions": get_sessions})


@ csrf_exempt
def GetExistingAttendance(request):
    get_subject = request.POST.get("subject")
    get_session = request.POST.get("session")

    subject_obj = Subjects.objects.get(id=get_subject)
    session_obj = SessionYear.objects.get(id=get_session)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_id=session_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date), "session_id": attendance_single.session_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), content_type='application/json', safe=False)


@ csrf_exempt
def GetStudentAttendance(request):
    get_attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=get_attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        data_element = {'id': student.student_id.admin.id, 'name': student.student_id.admin.first_name + " " + student.student_id.admin.last_name, 'status': student.status}
        list_data.append(data_element)
    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


@ csrf_exempt
def DoUpdateAttendance(request):
    student_ids = request.POST.get("student_ids")
    get_attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=get_attendance_date)
    json_student = json.loads(student_ids)

    try:

        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except Exception:
        return HttpResponse("ERROR")


def ApplyLeave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaffs.objects.filter(staff_id=staff_obj)
    return render(request, 'staff/applyleave.html', {'leave_data': leave_data})


def DoApplyLeave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staffapplyleave"))
    else:
        get_leavedate = request.POST.get('leavedate')
        get_leavereason = request.POST.get('leavemsg')
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaffs(staff_id=staff_obj, leave_date=get_leavedate, leave_message=get_leavereason, leave_status=0)
            leave_report.save()
            messages.success(request, 'Successfully Applied for Leave')
            return HttpResponseRedirect(reverse('staffapplyleave'))
        except Exception:
            messages.error(request, 'Failed to Apply for Leave')
            return HttpResponseRedirect(reverse('staffapplyleave'))


def Feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedbackStaffs.objects.filter(staff_id=staff_obj)
    return render(request, 'staff/feedback.html', {'feedback_data': feedback_data})


def DoFeedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("stafffeedback"))
    else:
        get_feedback = request.POST.get('feedbackmsg')
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            feedback = FeedbackStaffs(staff_id=staff_obj, feedback=get_feedback, feedback_reply="")
            feedback.save()
            messages.success(request, 'Successfully Sent Feedback')
            return HttpResponseRedirect(reverse('stafffeedback'))
        except Exception:
            messages.error(request, 'Failed to Send Feedback')
            return HttpResponseRedirect(reverse('stafffeedback'))

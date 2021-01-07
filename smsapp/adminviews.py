from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from smsapp.models import CustomUser, Courses, Subjects, Staffs, Students, SessionYear, AttendanceReport, Attendance, FeedbackStudents, FeedbackStaffs, LeaveReportStudents, LeaveReportStaffs
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from smsapp.forms import AddStudentForm, EditStudentForm, AddStaffForm, EditStaffForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def Home(request):
    staff_count = Staffs.objects.all().count()
    student_count = Students.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.name)
        subject_count_list.append(subjects)
        student_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count1 = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.name)
        student_in_subject.append(student_count1)

    staffs = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudents.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves + absent)
        student_name_list.append(student.admin.username)

    return render(request, 'admin/home.html', {'staff_count': staff_count, 'student_count': student_count, 'course_count': course_count, 'subject_count': subject_count, 'course_name_list': course_name_list, 'subject_count_list': subject_count_list, 'student_in_course': student_in_course, 'student_in_subject': student_in_subject, 'subject_list': subject_list, "staff_name_list": staff_name_list, "attendance_present_list_staff": attendance_present_list_staff, "attendance_absent_list_staff": attendance_absent_list_staff, "student_name_list": student_name_list, "attendance_present_list_student": attendance_present_list_student, "attendance_absent_list_student": attendance_absent_list_student})


def Profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'admin/profile.html', {'user': user})


def EditProfile(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        getfirstname = request.POST.get('firstname')
        getlastname = request.POST.get('lastname')
        getpassword = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = getfirstname
            customuser.last_name = getlastname
            if getpassword != None and getpassword != '':
                customuser.set_password(getpassword)
            customuser.save()
            messages.success(request, 'Successfully Updated Profile')
            return HttpResponseRedirect(reverse('adminprofile'))
        except Exception:
            messages.error(request, 'Failed to Update Profile')
            return HttpResponseRedirect(reverse('adminprofile'))


@ csrf_exempt
def CheckEmailExist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@ csrf_exempt
def CheckUserExist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def AddStaff(request):
    get_form = AddStaffForm()
    return render(request, 'admin/addstaff.html', {'form': get_form})


def DoAddStaff(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_form = AddStaffForm(request.POST, request.FILES)
        if get_form.is_valid():
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            address = request.POST.get('address')

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
                user.staffs.address = address
                user.staffs.profile_pic = profile_pic_url
                user.save()
                messages.success(request, 'Successfully Added Staff')
                return HttpResponseRedirect(reverse('addstaff'))
            except Exception:
                messages.error(request, 'Failed to Add Staff')
                return HttpResponseRedirect(reverse('addstaff'))
        else:
            get_form = AddStaffForm(request.POST)
            return render(request, 'admin/addstaff.html', {'form': get_form})


def AddCourse(request):
    return render(request, 'admin/addcourse.html')


def DoAddCourse(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(name=course)
            course_model.save()
            messages.success(request, 'Successfully Added Course')
            return HttpResponseRedirect(reverse('addcourse'))
        except Exception:
            messages.error(request, 'Failed to Add Course')
            return HttpResponseRedirect(reverse('addcourse'))


def AddSubject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'admin/addsubject.html', {'staffs': staffs, 'courses': courses})


def DoAddSubject(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        subject_name = request.POST.get('subject')
        get_course = request.POST.get('course')
        course = Courses.objects.get(id=get_course)
        get_staff = request.POST.get('staff')
        staff = CustomUser.objects.get(id=get_staff)
        try:
            subject = Subjects(name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, 'Successfully Added Subject')
            return HttpResponseRedirect(reverse('addsubject'))
        except Exception:
            messages.error(request, 'Failed to Add Subject')
            return HttpResponseRedirect(reverse('addsubject'))


def AddSession(request):
    return render(request, 'admin/addsession.html')


def DoAddSession(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('addsession'))
    else:
        start = request.POST.get('session_start')
        end = request.POST.get('session_end')
        try:
            session_year = SessionYear(session_start=start, session_end=end)
            session_year.save()
            messages.success(request, 'Successfully Added Session')
            return HttpResponseRedirect(reverse('addsession'))
        except Exception:
            messages.error(request, 'Failed to Add Session')
            return HttpResponseRedirect(reverse('addsession'))


def AddStudent(request):
    get_form = AddStudentForm()
    return render(request, 'admin/addstudent.html', {'form': get_form})


def DoAddStudent(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_form = AddStudentForm(request.POST, request.FILES)
        if get_form.is_valid():
            first_name = get_form.cleaned_data['firstname']
            last_name = get_form.cleaned_data['lastname']
            username = get_form.cleaned_data['username']
            email = get_form.cleaned_data['email']
            password = get_form.cleaned_data['password']
            address = get_form.cleaned_data['address']
            course_id = get_form.cleaned_data['course']
            session_id = get_form.cleaned_data['session_id']
            gender = get_form.cleaned_data['gender']

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                ses_obj = SessionYear.objects.get(id=session_id)
                user.students.session_id = ses_obj
                user.students.profile_pic = profile_pic_url
                user.students.gender = gender
                user.save()
                messages.success(request, 'Successfully Added Student')
                return HttpResponseRedirect(reverse('addstudent'))
            except Exception:
                messages.error(request, 'Failed to Add Student')
                return HttpResponseRedirect(reverse('addstudent'))

        else:
            get_form = AddStudentForm(request.POST)
            return render(request, 'admin/addstudent.html', {'form': get_form})


def ManageStaff(request):
    get_staffs = Staffs.objects.all()
    return render(request, 'admin/managestaff.html', {'staffs': get_staffs})


def ManageCourse(request):
    get_courses = Courses.objects.all()
    return render(request, 'admin/managecourse.html', {'courses': get_courses})


def ManageSubject(request):
    get_subjects = Subjects.objects.all()
    return render(request, 'admin/managesubject.html', {'subjects': get_subjects})


def ManageStudent(request):
    get_students = Students.objects.all()
    return render(request, 'admin/managestudent.html', {'students': get_students})


def EditStaff(request, id):
    request.session['get_staff_id'] = id
    get_staff = Staffs.objects.get(admin=id)
    get_form = EditStaffForm()
    get_form.fields['email'].initial = get_staff.admin.email
    get_form.fields['firstname'].initial = get_staff.admin.first_name
    get_form.fields['lastname'].initial = get_staff.admin.last_name
    get_form.fields['username'].initial = get_staff.admin.username
    get_form.fields['address'].initial = get_staff.address
    return render(request, 'admin/editstaff.html', {'form': get_form, 'id': id, 'username': get_staff.admin.username})


def DoEditStaff(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_staff_session = request.session.get('get_staff_id')
        if get_staff_session == None:
            return HttpResponseRedirect(reverse('managestaff'))

        get_form = EditStaffForm(request.POST, request.FILES)
        if get_form.is_valid():
            first_name = get_form.cleaned_data['firstname']
            last_name = get_form.cleaned_data['lastname']
            username = get_form.cleaned_data['username']
            email = get_form.cleaned_data['email']
            address = get_form.cleaned_data['address']
            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                user = CustomUser.objects.get(id=get_staff_session)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                staff_model = Staffs.objects.get(admin=get_staff_session)
                staff_model.address = address
                if profile_pic_url != None:
                    staff_model.profile_pic = profile_pic_url
                staff_model.save()

                messages.success(request, 'Successfully Updated Staff')
                return HttpResponseRedirect(reverse('editstaff', kwargs={'id': get_staff_session}))
            except Exception:
                messages.error(request, 'Failed to Update Staff')
                return HttpResponseRedirect(reverse('editstaff', kwargs={'id': get_staff_session}))
        else:
            get_form = EditStaffForm(request.POST)
            get_staff = Staffs.objects.get(admin=id)
            return render(request, 'admin/editstaff.html', {'form': get_form, 'id': get_staff_session, 'username': get_staff.admiin.username})


def EditCourse(request, id):
    get_course_id = Courses.objects.get(id=id)
    return render(request, 'admin/editcourse.html', {'course': get_course_id, 'id': id})


def DoEditCourse(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_course_id = request.POST.get('id')
        get_name = request.POST.get('course')

        try:
            course_model = Courses.objects.get(id=get_course_id)
            course_model.name = get_name
            course_model.save()

            messages.success(request, 'Successfully Updated Course')
            return HttpResponseRedirect(reverse('editcourse', kwargs={'id': get_course_id}))
        except Exception:
            messages.error(request, 'Failed to Update Course')
            return HttpResponseRedirect(reverse('editcourse', kwargs={'id': get_course_id}))


# def DeleteCourse(request, id):
#     course = Courses.objects.get(id=id)
#     try:
#         course.delete()
#         messages.success(request, "Course Deleted Successfully.")
#         return HttpResponseRedirect(reverse('managecourse'))
#     except Exception:
#         messages.error(request, "Failed to Delete Course.")
#         return HttpResponseRedirect(reverse('managecourse'))


def EditSubject(request, id):
    get_subject_id = Subjects.objects.get(id=id)
    get_course = Courses.objects.all()
    get_staff = CustomUser.objects.filter(user_type=2)
    return render(request, 'admin/editsubject.html', {'subject': get_subject_id, 'courses': get_course, 'staffs': get_staff, 'id': id})


def DoEditSubject(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_subject_id = request.POST.get('id')
        get_name = request.POST.get('subject')
        get_course = request.POST.get('course')
        get_staff = request.POST.get('staff')
        try:
            subject_model = Subjects.objects.get(id=get_subject_id)
            subject_model.name = get_name
            course_model = Courses.objects.get(id=get_course)
            subject_model.course_id = course_model
            staff_model = CustomUser.objects.get(id=get_staff)
            subject_model.staff_id = staff_model
            subject_model.save()

            messages.success(request, 'Successfully Updated Subject')
            return HttpResponseRedirect(reverse('editsubject', kwargs={'id': get_subject_id}))
        except Exception:
            messages.error(request, 'Failed to Update Subject')
            return HttpResponseRedirect(reverse('editsubject', kwargs={'id': get_subject_id}))


def EditStudent(request, id):
    request.session['get_student_id'] = id
    get_student = Students.objects.get(admin=id)
    get_form = EditStudentForm()
    get_form.fields['email'].initial = get_student.admin.email
    get_form.fields['firstname'].initial = get_student.admin.first_name
    get_form.fields['lastname'].initial = get_student.admin.last_name
    get_form.fields['username'].initial = get_student.admin.username
    get_form.fields['address'].initial = get_student.address
    get_form.fields['course'].initial = get_student.course_id.id
    get_form.fields['session_id'].initial = get_student.session_id.id
    get_form.fields['gender'].initial = get_student.gender
    return render(request, 'admin/editstudent.html', {'form': get_form, 'id': id, 'username': get_student.admin.username})


def DoEditStudent(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        get_student_session = request.session.get('get_student_id')
        if get_student_session == None:
            return HttpResponseRedirect(reverse('managestudent'))

        get_form = EditStudentForm(request.POST, request.FILES)
        if get_form.is_valid():
            first_name = get_form.cleaned_data['firstname']
            last_name = get_form.cleaned_data['lastname']
            username = get_form.cleaned_data['username']
            email = get_form.cleaned_data['email']
            address = get_form.cleaned_data['address']
            get_course = get_form.cleaned_data['course']
            get_ses = get_form.cleaned_data['session_id']
            gender = get_form.cleaned_data['gender']
            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                user = CustomUser.objects.get(id=get_student_session)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                student_model = Students.objects.get(admin=get_student_session)
                student_model.address = address
                student_model.gender = gender
                course_model = Courses.objects.get(id=get_course)
                ses_model = SessionYear.objects.get(id=get_ses)
                student_model.session_id = ses_model
                student_model.course_id = course_model
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                del request.session['get_student_id']
                messages.success(request, 'Successfully Updated Student')
                return HttpResponseRedirect(reverse('editstudent', kwargs={'id': get_student_session}))
            except Exception:
                messages.error(request, 'Failed to Update Student')
                return HttpResponseRedirect(reverse('editstudent', kwargs={'id': get_student_session}))
        else:
            get_form = EditStudentForm(request.POST)
            get_student = Students.objects.get(admin=id)
            return render(request, 'admin/editstudent.html', {'form': get_form, 'id': get_student_session, 'username': get_student.admiin.username})


# def DeleteStudent(request, id):
#     student = Students.objects.get(admin=id)
#     try:
#         student.delete()
#         messages.success(request, "Student Deleted Successfully.")
#         return HttpResponseRedirect(reverse('managestudent'))
#     except Exception:
#         messages.error(request, "Failed to Delete Student.")
#         return HttpResponseRedirect(reverse('managestudent'))


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


def FeedbackStaff(request):
    feedbacks = FeedbackStaffs.objects.all()
    return render(request, 'admin/feedbackstaff.html', {'feedbacks': feedbacks})


def FeedbackStudent(request):
    feedbacks = FeedbackStudents.objects.all()
    return render(request, 'admin/feedbackstudent.html', {'feedbacks': feedbacks})


@ csrf_exempt
def FeedbackStaffReply(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedbackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse('True')
    except Exception:
        return HttpResponse('False')


@ csrf_exempt
def FeedbackStudentReply(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedbackStudents.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse('True')
    except Exception:
        return HttpResponse('False')


def StaffLeave(request):
    leaves = LeaveReportStaffs.objects.all()
    return render(request, 'admin/staffleave.html', {'leaves': leaves})


def StaffLeaveApprove(request, id):
    leave = LeaveReportStaffs.objects.get(id=id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staffleave"))


def StaffLeaveDisapprove(request, id):
    leave = LeaveReportStaffs.objects.get(id=id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staffleave"))


def StudentLeave(request):
    leaves = LeaveReportStudents.objects.all()
    return render(request, 'admin/studentleave.html', {'leaves': leaves})


def StudentLeaveApprove(request, id):
    leave = LeaveReportStudents.objects.get(id=id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("studentleave"))


def StudentLeaveDisapprove(request, id):
    leave = LeaveReportStudents.objects.get(id=id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("studentleave"))


def ViewAttendance(request):
    get_subjects = Subjects.objects.all()
    get_sessions = SessionYear.objects.all()
    return render(request, "admin/viewattendance.html", {'subjects': get_subjects, "sessions": get_sessions})

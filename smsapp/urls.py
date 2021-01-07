from django.urls import path

from . import views, adminviews, staffviews, studentviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/passwordreset.html", subject_template_name='accounts/passwordresetsubject.txt',
                                                                 email_template_name='accounts/passwordresetemail.html'), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/passwordresetsent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/passwordresetform.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/passwordresetcomplete.html"), name="password_reset_complete"),


    # Genaral
    path('', views.Login, name='login'),
    path('dologin', views.DoLogin, name='dologin'),
    path('logout', views.LogOut, name='logout'),
    # Admin
    path('adminprofile', adminviews.Profile, name='adminprofile'),
    path('editprofileadmin', adminviews.EditProfile, name='editprofileadmin'),
    path('adminhome', adminviews.Home, name='adminhome'),
    # Admin Add
    path('checkemailexist', adminviews.CheckEmailExist, name='checkemailexist'),
    path('checkusernameexist', adminviews.CheckUserExist, name='checkusernameexist'),
    path('addstaff', adminviews.AddStaff, name='addstaff'),
    path('doaddstaff', adminviews.DoAddStaff, name='doaddstaff'),
    path('addcourse', adminviews.AddCourse, name='addcourse'),
    path('doaddcourse', adminviews.DoAddCourse, name='doaddcourse'),
    path('addsubject', adminviews.AddSubject, name='addsubject'),
    path('doaddsubject', adminviews.DoAddSubject, name='doaddsubject'),
    path('addsession', adminviews.AddSession, name='addsession'),
    path('doaddsession', adminviews.DoAddSession, name='doaddsession'),
    path('addstudent', adminviews.AddStudent, name='addstudent'),
    path('doaddstudent', adminviews.DoAddStudent, name='doaddstudent'),
    # Admin View
    path('managestaff/', adminviews.ManageStaff, name='managestaff'),
    path('managecourse/', adminviews.ManageCourse, name='managecourse'),
    path('managesubject/', adminviews.ManageSubject, name='managesubject'),
    path('managestudent/', adminviews.ManageStudent, name='managestudent'),
    # Admin Edit
    path('editstaff/<str:id>', adminviews.EditStaff, name='editstaff'),
    path('doeditstaff', adminviews.DoEditStaff, name='doeditstaff'),
    path('editcourse/<str:id>', adminviews.EditCourse, name='editcourse'),
    path('doeditcourse', adminviews.DoEditCourse, name='doeditcourse'),
    # path('deletecourse/<str:id>', adminviews.DeleteCourse, name='deletecourse'),
    path('editsubject/<str:id>', adminviews.EditSubject, name='editsubject'),
    path('doeditsubject', adminviews.DoEditSubject, name='doeditsubject'),
    path('editstudent/<str:id>', adminviews.EditStudent, name='editstudent'),
    path('doeditstudent', adminviews.DoEditStudent, name='doeditstudent'),
    # path('deletestudent/<str:id>', adminviews.DeleteStudent, name='deletestudent'),
    # Admin Attendance
    path('adminviewattendance', adminviews.ViewAttendance, name='adminviewattendance'),
    path('admingetattendance', adminviews.GetExistingAttendance, name='admingetattendance'),
    path('admingetstudentattendance', adminviews.GetStudentAttendance, name='admingetstudentattendance'),
    # Admin Feedback
    path('feedbackstudent', adminviews.FeedbackStudent, name='feedbackstudent'),
    path('feedbackstaff', adminviews.FeedbackStaff, name='feedbackstaff'),
    path('feedbackstaffreply', adminviews.FeedbackStaffReply, name='feedbackstaffreply'),
    path('feedbackstudentreply', adminviews.FeedbackStudentReply, name='feedbackstudentreply'),
    # Admin Leave
    path('staffleave', adminviews.StaffLeave, name='staffleave'),
    path('studentleave', adminviews.StudentLeave, name='studentleave'),
    path('studentleaveapprove/<str:id>', adminviews.StudentLeaveApprove, name='studentleaveapprove'),
    path('studentleavedisapprove/<str:id>', adminviews.StudentLeaveDisapprove, name='studentleavedisapprove'),
    path('staffleaveapprove/<str:id>', adminviews.StaffLeaveApprove, name='staffleaveapprove'),
    path('staffleavedisapprove/<str:id>', adminviews.StaffLeaveDisapprove, name='staffleavedisapprove'),



    # Staff
    path('staffprofile', staffviews.Profile, name='staffprofile'),
    path('editprofilestaff', staffviews.EditProfile, name='editprofilestaff'),
    path('staffhome', staffviews.Home, name='staffhome'),
    path('takeattendance', staffviews.TakeAttendance, name='takeattendance'),
    path('getstudent', staffviews.GetStudent, name='getstudent'),
    path('saveattendance', staffviews.SaveAttendance, name='saveattendance'),
    path('updateattendance', staffviews.UpdateAttendance, name='updateattendance'),
    path('getexistingattendance', staffviews.GetExistingAttendance, name='getexistingattendance'),
    path('getstudentattendance', staffviews.GetStudentAttendance, name='getstudentattendance'),
    path('doupdateattendance', staffviews.DoUpdateAttendance, name='doupdateattendance'),
    path('staffapplyleave', staffviews.ApplyLeave, name='staffapplyleave'),
    path('dostaffapplyleave', staffviews.DoApplyLeave, name='dostaffapplyleave'),
    path('stafffeedback', staffviews.Feedback, name='stafffeedback'),
    path('dostafffeedback', staffviews.DoFeedback, name='dostafffeedback'),




    # Student
    path('studentprofile', studentviews.Profile, name='studentprofile'),
    path('editprofilestudent', studentviews.EditProfile, name='editprofilestudent'),
    path('studenthome', studentviews.Home, name='studenthome'),
    path('viewattendance', studentviews.ViewAttendance, name='viewattendance'),
    path('viewattendancepost', studentviews.ViewAttendancePost, name='viewattendancepost'),
    path('studentapplyleave', studentviews.ApplyLeave, name='studentapplyleave'),
    path('dostudentapplyleave', studentviews.DoApplyLeave, name='dostudentapplyleave'),
    path('studentfeedback', studentviews.Feedback, name='studentfeedback'),
    path('dostudentfeedback', studentviews.DoFeedback, name='dostudentfeedback'),
]

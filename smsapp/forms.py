from django import forms
from smsapp.models import Courses, SessionYear


class DateInput(forms.DateInput):
    input_type = 'date'


class AddStaffForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    address = forms.CharField(label='Address', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.FileField(label='Profile Picture', max_length=100, widget=forms.FileInput(attrs={'class': 'form-control'}))


class EditStaffForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.FileField(label='Profile Picture', max_length=100, widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)


class AddStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    address = forms.CharField(label='Address', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))

    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            course_element = (course.id, course.name)
            course_list.append(course_element)
    except Exception:
        course_list = []

    session_list = []
    try:
        sessions = SessionYear.objects.all()
        for ses in sessions:
            ses_element = (ses.id, str(ses.session_start) + "   to  " + str(ses.session_end))
            session_list.append(ses_element)
    except Exception:
        session_list = []

    course = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={'class': 'form-control'}))
    session_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))

    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = forms.ChoiceField(label='Gender', choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    profile_pic = forms.FileField(label='Profile Picture', max_length=100, widget=forms.FileInput(attrs={'class': 'form-control'}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))

    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            course_element = (course.id, course.name)
            course_list.append(course_element)
    except Exception:
        course_list = []

    session_list = []
    try:
        sessions = SessionYear.objects.all()
        for ses in sessions:
            ses_element = (ses.id, str(ses.session_start) + "   to  " + str(ses.session_end))
            session_list.append(ses_element)
    except Exception:
        session_list = []

    course = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={'class': 'form-control'}))
    session_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = forms.ChoiceField(label='Gender', choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    profile_pic = forms.FileField(label='Profile Picture', max_length=100, widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

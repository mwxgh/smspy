from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class CheckLoginMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        get_user = request.user
        if get_user. is_authenticated:
            if get_user.user_type == '1':
                if module_name == 'smsapp.adminviews':
                    pass
                elif module_name == 'smsapp.views' or module_name == 'django.views.static':
                    pass
                elif module_name == "django.contrib.auth.views" or module_name == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse('adminhome'))
            elif get_user.user_type == '2':
                if module_name == 'smsapp.staffviews':
                    pass
                elif module_name == 'smsapp.views' or module_name == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('staffhome'))
            elif get_user.user_type == '3':
                if module_name == 'smsapp.studentviews':
                    pass
                elif module_name == 'smsapp.views' or module_name == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('studenthome'))
            else:
                return HttpResponseRedirect(reverse('login'))

        else:
            if request.path == reverse('login') or request.path == reverse('dologin') or module_name == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse('login'))

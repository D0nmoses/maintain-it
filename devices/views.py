from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .devices_settings import SYSTEM_MAINTENANCE_PAGINATE_BY
from .models import (Profile, DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceType, Software, SysAdmin, System)

# Create your views here.

@login_required(login_url='/accounts/login/')
def profile(request,id):
    '''	
    View function to display the profile of the logged in user when they click on the user icon	
    '''
    current_user = request.user

    try:

        single_profile = Profile.objects.get(user=current_user.id)

        title = f'{current_user.username}\'s'

        return render(request, 'all-devices/my_profile.html', {"title":title,"single_profile":single_profile,"current_user":current_user})

    except ObjectDoesNotExist:
        raise Http404()

def sysadmin_check(user):
    """
    Check whether user is a sysadmin and has an active account.
    """

    return user.is_active and hasattr(user, 'sysadmin')

class SysAdminRequiredMixin(object):
    """
    Checks whether user is a sysadmin and has an active account.
    """

    @method_decorator(user_passes_test(
        sysadmin_check,
        login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(SysAdminRequiredMixin, self).dispatch(*args, **kwargs)
    

@login_required(login_url='/accounts/login/')
@user_passes_test(sysadmin_check)
def home_view(request):
    '''
    View function to display the home page
    '''

    context = {
        'documentation_record_count':
            DocumentationRecord.objects.all().count(),
        'hardware_count': Hardware.objects.all().count(),
        'maintenance_record_count': MaintenanceRecord.objects.all().count(),
        'maintenance_type_count': MaintenanceType.objects.all().count(),
        'software_count': Software.objects.all().count(),
        'sys_admin_count': SysAdmin.objects.all().count(),
        'system_count': System.objects.all().count(),
    }
    return render(
        request, 'all-devices/home.html', context)
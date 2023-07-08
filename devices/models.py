from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import escape, linebreaks, urlize
from django.conf import settings
from django.core.exceptions import ValidationError

from markupfield_helpers.helpers import MarkupField


STATUS_CHOICES = [
    ('Complete', 'Complete'),
    ('In Progress', 'In Progress'),
    ('Failed', 'Failed'),
]

# Create your models here.
class Profile(models.Model):
    '''	
    Class to define a user's profile
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile-pic/", blank=True, default='/profile-pic/default-no-profile-pic.jpg')

    def __str__(self):

        return self.user.username

    @classmethod
    def get_profiles(cls):

        profiles = Profile.objects.all()

        return profiles

    @classmethod
    def get_other_profiles(cls,user_id):


        profiles = Profile.objects.all()

        other_profiles = []

        for profile in profiles:

            if profile.user.id != user_id:

                other_profiles.append(profile)

        return other_profiles


# Create Profile when creating a User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save Profile when saving a User
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Hardware(models.Model):

    name = models.CharField(
        max_length=255,
        help_text="Enter the type of hardware.",
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'hardware'

    def __str__(self):
        return self.name


class DocumentationRecord(models.Model):

    title = models.CharField(
        max_length=255,
        help_text="Enter a brief, descriptive title for this documentation.",
        unique=True,
    )

    maintenance_type = models.ForeignKey(
        'MaintenanceType',
        help_text='Select/Create a maintenance type.',
        on_delete=models.PROTECT,
    )

    documentation = MarkupField(
        blank=True,
        help_text='Document how to perform a task.',
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title



class MaintenanceRecord(models.Model):
    system = models.ForeignKey(
        'System',
        help_text='Select/Create a system.',
        on_delete=models.PROTECT,
    )

    sys_admin = models.ForeignKey(
        'SysAdmin',
        help_text='Select a system administrator.',
        on_delete=models.PROTECT,
    )

    maintenance_type = models.ForeignKey(
        'MaintenanceType',
        help_text='Select/Create a maintenance type.',
        on_delete=models.PROTECT,
    )

    hardware = models.ManyToManyField(
        'Hardware',
        blank=True,
        help_text='Select the hardware involved in the system maintenance.',
    )

    software = models.ManyToManyField(
        'Software',
        blank=True,
        help_text='Select the software involved in the system maintenance.',
    )

    description = MarkupField(
        blank=True,
        help_text='Enter a description of the system maintenance performed.',
        null=True,
    )

    procedure = MarkupField(
        blank=True,
        help_text='Enter details of how the system maintenance was performed.',
        null=True,
    )

    problems = MarkupField(
        blank=True,
        help_text='Describe problems that arose during system maintenance.',
        null=True,
    )

    referenced_records = models.ManyToManyField(
        'self',
        related_name='referencing_records',
        symmetrical=False,
        through='MaintenanceRecordRelationship',
    )

    documentation_records = models.ManyToManyField(
        'DocumentationRecord',
        blank=True,
        help_text='Select documentation relevant to this system maintenance.<br>',
        related_name='maintenance_records',
    )

    status = models.CharField(
        choices = STATUS_CHOICES,
        default='In Progress',
        help_text='What is the current status of the system maintenance?',
        max_length=15,
    )

    datetime = models.DateTimeField(
        'maintenance date/time',
        default=timezone.now,
        help_text='Specify the date/time that the system maintenance was '
                  'performed.',
    )

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'maintenance record'
        verbose_name_plural = 'maintenance records'

    def __str__(self):
        return '{} - {} ({})'.format(
            self.system, self.maintenance_type, self.datetime.date())


class MaintenanceRecordRelationship(models.Model):

    referencing_record = models.ForeignKey(
        'MaintenanceRecord',
        related_name='referencing_record',
        on_delete=models.CASCADE,
    )

    referenced_record = models.ForeignKey(
        'MaintenanceRecord',
        related_name='referenced_record',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['referencing_record']
        unique_together = ('referencing_record', 'referenced_record')

    def clean(self):
        if self.referencing_record == self.referenced_record:
            raise ValidationError('A record cannot by related to itself.')

    def __str__(self):
        return '{} ➤ {}'.format(
            self.referencing_record, self.referenced_record)


class MaintenanceType(models.Model):

    maintenance_type = models.CharField(
        help_text="Enter a type of maintenance "
                  "(e.g., 'Software Installation').",
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Enter a description of the maintenance type.',
    )

    class Meta:
        ordering = ['maintenance_type']

    def __str__(self):
        return self.maintenance_type


class Software(models.Model):

    name = models.CharField(
        max_length=255,
        help_text="Enter the software's name.",
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'software package'
        verbose_name_plural = 'software packages'

    def __str__(self):
        return self.name


class SysAdmin(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        help_text='Select a user.',
        on_delete=models.PROTECT,
        unique=True,
    )

    class Meta:
        verbose_name = 'system administrator'
        verbose_name_plural = 'system administrators'

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return '{} ({})'.format(
                ' '.join([self.user.first_name, self.user.last_name]),
                self.user.username)
        else:
            return self.user.username


class System(models.Model):

    name = models.CharField(
        'system name',
        help_text='Enter a brief, unique identifier for the system.',
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Enter a description of the system.',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
# Generated by Django 4.2.3 on 2023-07-08 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markupfield_helpers.helpers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a brief, descriptive title for this documentation.', max_length=255, unique=True)),
                ('documentation', markupfield_helpers.helpers.MarkupField(blank=True, help_text='Document how to perform a task.', null=True, rendered_field=True)),
                ('documentation_markup_type', models.CharField(choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')], default='Markdown', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('_documentation_rendered', models.TextField(editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the type of hardware.', max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'hardware',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', markupfield_helpers.helpers.MarkupField(blank=True, help_text='Enter a description of the system maintenance performed.', null=True, rendered_field=True)),
                ('description_markup_type', models.CharField(choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')], default='Markdown', max_length=30)),
                ('procedure', markupfield_helpers.helpers.MarkupField(blank=True, help_text='Enter details of how the system maintenance was performed.', null=True, rendered_field=True)),
                ('_description_rendered', models.TextField(editable=False, null=True)),
                ('procedure_markup_type', models.CharField(choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')], default='Markdown', max_length=30)),
                ('problems', markupfield_helpers.helpers.MarkupField(blank=True, help_text='Describe problems that arose during system maintenance.', null=True, rendered_field=True)),
                ('_procedure_rendered', models.TextField(editable=False, null=True)),
                ('problems_markup_type', models.CharField(choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')], default='Markdown', max_length=30)),
                ('_problems_rendered', models.TextField(editable=False, null=True)),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('In Progress', 'In Progress'), ('Failed', 'Failed')], default='In Progress', help_text='What is the current status of the system maintenance?', max_length=15)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, help_text='Specify the date/time that the system maintenance was performed.', verbose_name='maintenance date/time')),
                ('documentation_records', models.ManyToManyField(blank=True, help_text='Select documentation relevant to this system maintenance.<br>', related_name='maintenance_records', to='devices.documentationrecord')),
                ('hardware', models.ManyToManyField(blank=True, help_text='Select the hardware involved in the system maintenance.', to='devices.hardware')),
            ],
            options={
                'verbose_name': 'maintenance record',
                'verbose_name_plural': 'maintenance records',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_type', models.CharField(help_text="Enter a type of maintenance (e.g., 'Software Installation').", max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='Enter a description of the maintenance type.')),
            ],
            options={
                'ordering': ['maintenance_type'],
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the software's name.", max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'software package',
                'verbose_name_plural': 'software packages',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a brief, unique identifier for the system.', max_length=255, unique=True, verbose_name='system name')),
                ('description', models.TextField(blank=True, help_text='Enter a description of the system.')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SysAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(help_text='Select a user.', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'system administrator',
                'verbose_name_plural': 'system administrators',
            },
        ),
        migrations.CreateModel(
            name='MaintenanceRecordRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referenced_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referenced_record', to='devices.maintenancerecord')),
                ('referencing_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referencing_record', to='devices.maintenancerecord')),
            ],
            options={
                'ordering': ['referencing_record'],
                'unique_together': {('referencing_record', 'referenced_record')},
            },
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='maintenance_type',
            field=models.ForeignKey(help_text='Select/Create a maintenance type.', on_delete=django.db.models.deletion.PROTECT, to='devices.maintenancetype'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='referenced_records',
            field=models.ManyToManyField(related_name='referencing_records', through='devices.MaintenanceRecordRelationship', to='devices.maintenancerecord'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='software',
            field=models.ManyToManyField(blank=True, help_text='Select the software involved in the system maintenance.', to='devices.software'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='sys_admin',
            field=models.ForeignKey(help_text='Select a system administrator.', on_delete=django.db.models.deletion.PROTECT, to='devices.sysadmin'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='system',
            field=models.ForeignKey(help_text='Select/Create a system.', on_delete=django.db.models.deletion.PROTECT, to='devices.system'),
        ),
        migrations.AddField(
            model_name='documentationrecord',
            name='maintenance_type',
            field=models.ForeignKey(help_text='Select/Create a maintenance type.', on_delete=django.db.models.deletion.PROTECT, to='devices.maintenancetype'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-29 02:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_ip', models.GenericIPAddressField()),
                ('submitted_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('event_name', models.CharField(db_index=True, max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('datetime_setup_complete', models.DateTimeField()),
                ('datetime_start', models.DateTimeField(db_index=True)),
                ('datetime_end', models.DateTimeField()),
                ('internal_notes', models.TextField(blank=True, help_text='Notes that the client and general body should never see.', null=True)),
                ('billed_in_bulk', models.BooleanField(db_index=True, default=False, help_text='Check if billing of this event will be deferred so that it can be combined with other events in a single invoice')),
                ('sensitive', models.BooleanField(default=False, help_text='Nobody besides those directly involved should know about this event')),
                ('test_event', models.BooleanField(default=False, help_text="Check to lower the VP's blood pressure after they see the short-notice S4/L4")),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(blank=True, null=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('reviewed_on', models.DateTimeField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('closed_on', models.DateTimeField(blank=True, null=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('cancelled_on', models.DateTimeField(blank=True, null=True)),
                ('cancelled_reason', models.TextField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventapprovals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'ordering': ['-datetime_start'],
                'permissions': (('view_events', "Show an event that isn't hidden"), ('add_raw_event', 'Use the editor to create an event'), ('event_images', 'Upload images to an event'), ('view_hidden_event', 'Show hidden events'), ('cancel_event', 'Declare an event to be cancelled'), ('event_attachments', 'Upload attachments to an event'), ('edit_event_times', 'Modify the dates for an event'), ('add_event_report', 'Add reports about the event'), ('edit_event_fund', 'Change where money for an event comes from'), ('view_event_billing', 'See financial info for event'), ('view_event_reports', 'See reports for event'), ('edit_event_text', 'Update any event descriptions'), ('adjust_event_owner', 'Change the event contact and organization'), ('edit_event_hours', 'Modify the time sheets'), ('edit_event_flags', 'Add flags to an event'), ('event_view_sensitive', 'Show internal notes and other metadata marked as not public'), ('approve_event', 'Accept an event'), ('decline_event', 'Decline an event'), ('can_chief_event', 'Can crew chief an event'), ('review_event', 'Review an event for billing'), ('adjust_event_charges', 'Add charges and change event type'), ('bill_event', 'Send bills and mark event paid'), ('close_event', 'Lock an event after everything is done.'), ('view_test_event', 'Show events for testing'), ('event_view_granular', 'See debug data like ip addresses'), ('event_view_debug', 'See debug events'), ('reopen_event', 'Reopen a closed, declined, or cancelled event')),
            },
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_billed', models.DateField()),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billings', to='events.baseevent')),
            ],
            options={
                'ordering': ('-date_billed', 'date_paid'),
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('shortname', models.CharField(max_length=4)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('desc', models.TextField()),
                ('disappear', models.BooleanField(default=False, help_text='Disappear this extra instead of disable')),
                ('checkbox', models.BooleanField(default=False, help_text='Use a checkbox instead of an integer entry')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category')),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund', models.IntegerField()),
                ('organization', models.IntegerField()),
                ('account', models.IntegerField(default=71973)),
                ('name', models.CharField(max_length=128)),
                ('notes', models.TextField(blank=True, null=True)),
                ('last_used', models.DateField(null=True)),
                ('last_updated', models.DateField(null=True)),
            ],
            options={
                'permissions': (('manage_fund', 'Manage a fund'),),
            },
        ),
        migrations.CreateModel(
            name='MultiBilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_billed', models.DateField()),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('events', models.ManyToManyField(related_name='multibillings', to='events.BaseEvent')),
            ],
            options={
                'ordering': ('-date_billed', 'date_paid'),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('shortname', models.CharField(blank=True, max_length=8, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='normal_email_unused')),
                ('exec_email', models.EmailField(max_length=254, null=True, verbose_name='Email')),
                ('email_exec', models.BooleanField(default=True)),
                ('email_normal', models.BooleanField(default=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(max_length=32)),
                ('notes', models.TextField(blank=True, null=True)),
                ('personal', models.BooleanField(default=False)),
                ('delinquent', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('locked', models.BooleanField(blank=True, default=False)),
                ('accounts', models.ManyToManyField(related_name='orgfunds', to='events.Fund')),
                ('associated_orgs', models.ManyToManyField(blank=True, related_name='_organization_associated_orgs_+', to='events.Organization', verbose_name='Associated Clients')),
                ('associated_users', models.ManyToManyField(related_name='orgusers', to=settings.AUTH_USER_MODEL)),
                ('user_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orgowner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
                'permissions': (('view_org', "See an Organization's basic properties"), ('list_org_events', "View an Org's non-hidden events"), ('list_org_hidden_events', "View an Org's hidden events"), ('edit_org', "Edit an Org's name and description"), ('show_org_billing', "See an Org's account and billing info"), ('edit_org_billing', "Modify an Org's account and billing info"), ('list_org_members', 'View who is in an Org'), ('edit_org_members', 'Edit who is in an Org'), ('create_org_event', "Create an event in an Org's name"), ('view_verifications', 'Show proofs of Org account ownership'), ('create_verifications', 'Create proofs of Org account ownership'), ('transfer_org_ownership', 'Give an Org a new owner'), ('add_org', 'Create an Organization'), ('deprecate_org', 'Mark an Organization as defunct'), ('view_org_notes', 'View internal notes for an org')),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(max_length=2)),
                ('longname', models.CharField(max_length=64)),
                ('base_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('addtl_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('help_desc', models.TextField(blank=True, null=True)),
                ('enabled_event2012', models.BooleanField(default=False, verbose_name='Enabled for 2012 Events')),
                ('enabled_event2019', models.BooleanField(default=True, verbose_name='Enabled for 2019 Events')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category')),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('instructors', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'permissions': (('edit_workshops', 'Modify workshops'),),
            },
        ),
        migrations.CreateModel(
            name='Lighting',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.service')),
            ],
            bases=('events.service',),
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.service')),
            ],
            bases=('events.service',),
        ),
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.service')),
            ],
            bases=('events.service',),
        ),
        migrations.CreateModel(
            name='WorkshopDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='events.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(blank=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.baseevent')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.service')),
            ],
        ),
        migrations.CreateModel(
            name='ReportReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('crew_chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ccreportreminders', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ccreportreminders', to='events.baseevent')),
            ],
        ),
        migrations.CreateModel(
            name='PostEventSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services_quality', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], verbose_name='Please rate the overall quality of the services Lens and Lights provided.')),
                ('lighting_quality', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], verbose_name='How satisfied were you with the lighting?')),
                ('sound_quality', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], verbose_name='How satisfied were you with the sound system?')),
                ('work_order_method', models.IntegerField(choices=[(None, 'Please select...'), (1, 'Via the website at lnl.wpi.edu/workorder'), (2, 'Emailed lnl@wpi.edu'), (3, 'Emailed an LNL representative directly'), (4, 'By phone'), (5, 'In person'), (0, 'Other'), (-1, "I don't know")], verbose_name='How did you submit the workorder?')),
                ('work_order_experience', models.IntegerField(blank=True, choices=[(-1, 'Not applicable'), (0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], default=-1, null=True, verbose_name='How would you rate your overall experience using the workorder tool?')),
                ('work_order_ease', models.IntegerField(blank=True, choices=[(-1, 'Not applicable'), (0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], default=-1, null=True, verbose_name="How would you rate the workorder tool's clarity and ease of use?")),
                ('work_order_comments', models.TextField(blank=True, verbose_name='Please provide any additional comments you may have regarding your experience with the workorder tool. Is there anything you would like to see us improve?')),
                ('communication_responsiveness', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='Lens and Lights was responsive to my communications.')),
                ('pricelist_ux', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='It was easy to determine which services to request and I had no problem finding what I needed.')),
                ('setup_on_time', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='My event was set up and the crew was ready on time.')),
                ('crew_respectfulness', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='When interacting with the crew, they were helpful and respectful.')),
                ('price_appropriate', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='The price quoted for the event matched my expectations and was appropriate for the services provided.')),
                ('customer_would_return', models.IntegerField(choices=[(-1, 'Not applicable'), (0, 'Strongly disagree'), (1, 'Disagree'), (2, 'Neither agree nor disagree'), (3, 'Agree'), (4, 'Strongly agree')], verbose_name='I would use Lens and Lights in the future.')),
                ('comments', models.TextField(blank=True, verbose_name='Please use this area to provide any additional feedback you may have about your event.')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='surveys', to='events.baseevent')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['event', 'person'],
                'permissions': (('view_posteventsurveyresults', 'View post-event survey results'),),
            },
        ),
        migrations.CreateModel(
            name='OrgBillingVerificationEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('note', models.TextField(blank=True, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifications', to='events.organization')),
                ('verified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-id'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='OrganizationTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xfer_initiated', to=settings.AUTH_USER_MODEL)),
                ('new_user_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xfer_new', to=settings.AUTH_USER_MODEL)),
                ('old_user_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xfer_old', to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('hour_start', models.TimeField()),
                ('hour_end', models.TimeField()),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Office Hour',
                'permissions': (('manage_hours', 'Manage Office Hours'),),
            },
        ),
        migrations.CreateModel(
            name='MultiBillingEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('email_to_orgs', models.ManyToManyField(to='events.Organization')),
                ('email_to_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('multibilling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.multibilling')),
            ],
        ),
        migrations.AddField(
            model_name='multibilling',
            name='org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='multibillings', to='events.organization'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('setup_only', models.BooleanField(default=False)),
                ('show_in_wo_form', models.BooleanField(default=True, verbose_name='Event Location')),
                ('available_for_meetings', models.BooleanField(default=False)),
                ('holds_equipment', models.BooleanField(default=False)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.building')),
            ],
            options={
                'ordering': ['building', 'name'],
            },
        ),
        migrations.CreateModel(
            name='HourChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now=True)),
                ('expires', models.DateTimeField()),
                ('message', models.TextField(max_length=244)),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Office Hour Update',
            },
        ),
        migrations.CreateModel(
            name='ExtraInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quant', models.PositiveIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.baseevent')),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.extra')),
            ],
        ),
        migrations.AddField(
            model_name='extra',
            name='services',
            field=models.ManyToManyField(to='events.Service'),
        ),
        migrations.CreateModel(
            name='EventCCInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setup_start', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ccinstances', to='events.category')),
                ('crew_chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ccinstances', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ccinstances', to='events.baseevent')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ccinstances', to='events.service')),
                ('setup_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ccinstances', to='events.location')),
            ],
            options={
                'ordering': ('-event__datetime_start',),
            },
        ),
        migrations.CreateModel(
            name='EventAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=events.models.attachment_file_name)),
                ('note', models.TextField(blank=True, default='', null=True)),
                ('externally_uploaded', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='events.baseevent')),
                ('for_service', models.ManyToManyField(blank=True, related_name='attachments', to='events.Service')),
            ],
        ),
        migrations.CreateModel(
            name='EventArbitrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=64)),
                ('key_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('key_quantity', models.PositiveSmallIntegerField(default=1)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arbitraryfees', to='events.baseevent')),
            ],
        ),
        migrations.CreateModel(
            name='CCReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.TextField(validators=[django.core.validators.MinLengthValidator(20)])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('crew_chief', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.baseevent')),
                ('for_service_cat', models.ManyToManyField(blank=True, to='events.Category', verbose_name='Services')),
            ],
        ),
        migrations.CreateModel(
            name='BillingEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.billing')),
                ('email_to_orgs', models.ManyToManyField(to='events.Organization')),
                ('email_to_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='baseevent',
            name='billing_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='billedevents', to='events.organization'),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='cancelled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventcancellations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventclosings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Contact'),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.location'),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='org',
            field=models.ManyToManyField(blank=True, related_name='events', to='events.Organization', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_events.baseevent_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventbillingreview', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='submitted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submitter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Hours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hours', to='events.category')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to='events.baseevent')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hours', to='events.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('event', 'user', 'service')},
            },
        ),
        migrations.CreateModel(
            name='Event2019',
            fields=[
                ('baseevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.baseevent')),
                ('workday_fund', models.IntegerField(blank=True, choices=[(810, 'Student Organization (810-FD)'), (110, 'Operating (110-FD)'), (220, 'Gift (220-FD)'), (250, 'Gift (250-FD)'), (500, 'Gift (500-FD)'), (210, 'Grant (210-FD)'), (900, 'Project (900-FD)'), (120, 'Designated (120-FD)')], null=True)),
                ('worktag', models.CharField(blank=True, max_length=10, null=True)),
                ('workday_form_comments', models.TextField(blank=True, null=True)),
                ('entered_into_workday', models.BooleanField(default=False, help_text='Checked when the Treasurer has created an Internal Service Delivery in Workday for this event')),
                ('send_survey', models.BooleanField(default=False, help_text='Check if the event contact should be emailed the post-event survey after the event')),
                ('survey_sent', models.BooleanField(default=False, help_text='The post-event survey has been sent to the client')),
                ('max_crew', models.PositiveIntegerField(blank=True, null=True)),
                ('workday_entered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workdayentries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '2019 Event',
            },
            bases=('events.baseevent',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('baseevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.baseevent')),
                ('datetime_setup_start', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('lighting_reqs', models.TextField(blank=True, null=True)),
                ('sound_reqs', models.TextField(blank=True, null=True)),
                ('proj_reqs', models.TextField(blank=True, null=True)),
                ('otherservice_reqs', models.TextField(blank=True, null=True)),
                ('payment_amount', models.IntegerField(blank=True, default=None, null=True)),
                ('ccs_needed', models.PositiveIntegerField(db_index=True, default=0)),
                ('billing_fund', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_accounts', to='events.fund')),
                ('crew', models.ManyToManyField(blank=True, related_name='crewx', to=settings.AUTH_USER_MODEL)),
                ('crew_chief', models.ManyToManyField(blank=True, related_name='crewchiefx', to=settings.AUTH_USER_MODEL)),
                ('lighting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lighting', to='events.lighting')),
                ('otherservices', models.ManyToManyField(blank=True, to='events.Service')),
                ('projection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projection', to='events.projection')),
                ('setup_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='setuplocation', to='events.location')),
                ('sound', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sound', to='events.sound')),
            ],
            options={
                'verbose_name': '2012 Event',
            },
            bases=('events.baseevent',),
        ),
        migrations.CreateModel(
            name='CrewAttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateTimeField(default=django.utils.timezone.now)),
                ('checkout', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_records', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crew_attendance', to='events.event2019')),
            ],
            options={
                'permissions': (('view_attendance_records', 'View Attendance Records'),),
            },
        ),
    ]

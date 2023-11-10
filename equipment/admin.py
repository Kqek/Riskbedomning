from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Equipment, Component, Task
from django.db import connections
from django.db import models

#===============================================================================
#===============================================================================
#===============================================================================
class TaskInline(admin.TabularInline):
    model=Task # To assign this class to a model
    fields = ('task', 'responsible', 'duedate') # the fields automatically filled in cannot be shown here.
    extra = 0 # Show no extra fields in the admin panel.

#===============================================================================
#===============================================================================
#EquipmentAdmin=================================================================
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'objectid', 'risk_class', 'assessment')
    
    def risk_class(self, obj):
        # This is a custom method to display the risk_class value
        return obj.risk_class
    
    
    risk_class.short_description = 'Risk Class'  # Display name in the admin panel
    risk_class.admin_order_field = 'risk_class'  # Allow sorting by risk_class
    
    
    def get_queryset(self, request):
        # Get the default queryset
        queryset = super().get_queryset(request)

        # Connect to the PostgreSQL database
        with connections['risk'].cursor() as cursor:
            # Execute a query to get risk_class for each objectid in the Equipment queryset
            object_ids = list(queryset.values_list('objectid', flat=True))
            cursor.execute("SELECT objectid, risk_class FROM equipment WHERE objectid IN %s", [tuple(object_ids)])
            risk_class_mapping = dict(cursor.fetchall())

        # Update the risk_class field for each Equipment object in the queryset
        for equipment in queryset:
            equipment.risk_class = risk_class_mapping.get(equipment.objectid, None)
            print(equipment.risk_class)

        return queryset

    def risk_class(self, obj):
        return obj.risk_class

    risk_class.admin_order_field = 'risk_class'  # Allow sorting by risk_class


#===============================================================================
#===============================================================================
#ComponentAdmin=================================================================
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'articleNMR', 'description', 'manufacturer', 'preparation_Status',
                    'balance', 'average_usage_per3year', 'average_usage_per5year', 'num_of_devices_use_item',
                    'suggested_assessment', 'assessment', 'assess_Date', 'tasks_count_link')

    inlines=[TaskInline]
    def tasks_count_link(self, obj):
        if obj.tasks_count() > 0:
            url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label,  obj._meta.model_name))
            return format_html('<a href="{}?post__id__exact={}">{}</a>', url, obj.id, obj.tasks_count())
        else:
            return obj.tasks_count()

    tasks_count_link.admin_order_field = 'tasks_count'
    tasks_count_link.short_description = 'Number of tasks'


#===============================================================================
#===============================================================================
#TaskAdmin======================================================================
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'component', 'task', 'responsible', 'duedate', 'registerdate')


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Task, TaskAdmin)
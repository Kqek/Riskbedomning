from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import connections

class Equipment(models.Model):
    objectid = models.CharField(max_length=10, unique=True)
    #risk_class = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    condition_EL_assess = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    condition_MEC_assess = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    components_EL_assess = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    components_MEC_assess = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    assessment = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    
    
    _risk_class = None  # private variable to store risk_class value

    @property
    def risk_class(self):
        if self._risk_class is None:
            # Connect to the PostgreSQL database
            with connections['risk'].cursor() as cursor:
                # Execute a query to get risk_class based on objectid
                cursor.execute("SELECT risk_class FROM equipment WHERE objectid = %s", [self.objectid])
                row = cursor.fetchone()
                self._risk_class = row[0] if row else None
        return self._risk_class

    @risk_class.setter
    def risk_class(self, value):
        # You can implement a custom setter logic if needed
        # For example, raise an exception or log a warning
        pass
        
        
    
    def __str__(self): 
        return'{}'.format(self.objectid)
 

class Component(models.Model):
    equipments = models.ManyToManyField('Equipment', blank=True, verbose_name=_('Equipments')) # many products can be connected to many category
    articleNMR = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    preparation_Status = models.CharField(max_length=1)
    balance = models.IntegerField(default=0)
    average_usage_per3year = models.IntegerField(default=0)
    average_usage_per5year = models.IntegerField(default=0)
    num_of_devices_use_item = models.IntegerField(default=0)
    suggested_assessment = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    assessment = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    assess_Date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Components'
        verbose_name = _('Component')
        verbose_name_plural = _('Components')
        
        
    def __str__(self): 
        return'{}'.format(self.articleNMR)
    
    
    def tasks_count(self):
        return self.tasks.count()

class Task(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='tasks')
    task = models.TextField(blank=True,default='')
    responsible = models.CharField(max_length=255)
    duedate = models.DateTimeField()
    registerdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return'{}-{}'.format(self.task,self.responsible)

"""     class Meta:
        unique_together = ('component', 'task') """
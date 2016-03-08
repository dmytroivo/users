from django.db import models

class User(models.Model):
        f_name = models.CharField(max_length=50)
        l_name = models.CharField(max_length=50)
        adress = models.CharField(max_length=100)
        email = models.EmailField(max_length=50)
        tel = models.CharField(max_length=20)
        name_plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, verbose_name='Тарифный план')
        status = models.CharField(max_length=1)
        descript = models.TextField(max_length=500, null=True)

        def __str__(self):              # __unicode__ on Python 2
                return self.name

class Plan(models.Model):
        name = models.CharField(max_length=100, unique=True)
        price = models.DecimalField(max_digits=5, decimal_places=2)
        relise_date = models.DateField()
        expired_date = models.DateField()
        status = models.CharField(max_length=1)

        def __str__(self):              # __unicode__ on Python 2
                return self.name

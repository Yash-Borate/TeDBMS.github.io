from django.db import models

# Create your models here.

class Employee(models.Model):
	emp_name = models.CharField(max_length=100)
	emp_gender = models.CharField(max_length=100, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
	emp_age = models.PositiveIntegerField()
	emp_salary = models.PositiveIntegerField()

	def __str__(self):
		return self.emp_name
	
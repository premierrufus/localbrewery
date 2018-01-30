from django.db import models

# Create your models here.


class Account(models.Model):
	contact = models.CharField('Contact Name', max_length=50)
	name = models.CharField('Account Name', max_length=50)
	notes = models.TextField()
	user = models.ForeignKey('auth.User')

	ACCOUNT_STATUS = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),
	)


	status = models.CharField('Account Status', max_length=20, choices=ACCOUNT_STATUS, blank=True, default='a')

	def __str__(self):
		return self.name
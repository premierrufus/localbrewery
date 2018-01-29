from django.db import models
from django.utils import timezone

# Create your models here.

SEP = ' | '

# Classes

class Beer(models.Model):
    name = models.CharField('Trade Name', max_length=50)

    def __str__(self):
        return self.name


class Gyle(models.Model):
    batch_number = models.CharField('#', max_length=7)

    def __str__(self):
        return self.batch_number

    
class BrewingEvent(models.Model):
    user = models.ForeignKey('auth.User')
    brewed_beer = models.ForeignKey(
        'Beer',
        on_delete=models.CASCADE,
    )
    gyle = models.ForeignKey(
        'Gyle',
        on_delete=models.CASCADE,
    )
    gyle2 = models.ForeignKey(
        'Gyle',
        on_delete=models.CASCADE,
        related_name='+'
    )
    brew_date = models.DateField(default=timezone.now)

    def __str__(self):
        if self.gyle2:
            return str(self.brew_date) + SEP + self.brewed_beer.name + SEP + str(self.gyle) + ', ' + str(self.gyle2)
        else:
            return str(self.brew_date) + SEP + self.brewed_beer.name + SEP + str(self.gyle)


    class Meta:
        verbose_name = "Brewing Event"




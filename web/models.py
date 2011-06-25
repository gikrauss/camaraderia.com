from django.db import models
import datetime

class Event(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return self.name

class Quote(models.Model):
    event = models.ForeignKey(Event, null=True)
    quote = models.CharField(max_length=2000)
    date = models.DateField(default=datetime.date.today())
    votes_up = models.IntegerField(default=0, editable=False)
    votes_down = models.IntegerField(default=0, editable=False)

    def save(self):
        if (self.event != None):
            self.date = self.event.date

        super(Quote, self).save()

    def __unicode__(self):
        return self.quote


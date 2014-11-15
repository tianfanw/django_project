from django.db import models

# Create your models here.
class Event(models.Model):
  id         = models.IntegerField(primary_key=True)
  title      = models.CharField(max_length=200)
  venue      = models.CharField(max_length=100)
  performer  = models.CharField(max_length=200)
  grouping   = models.CharField(max_length=100)

class Ticket(models.Model):
  id = models.IntegerField(primary_key=True)
  event = models.ForeignKey(Event)
  quantity = models.IntegerField()
  zoneId = models.IntegerField(null=True)
  zoneName = models.CharField(max_length=200,null=True)
  sectionId = models.IntegerField(null=True)
  sectionName = models.CharField(max_length=200,null=True)
  row = models.CharField(max_length=200)
  seatNumbers = models.CharField(max_length=200)
  currentPrice = models.FloatField()

class SoldTicket(models.Model):
  id = models.IntegerField(primary_key=True)
  event = models.ForeignKey(Event)
  quantity = models.IntegerField()
  zoneId = models.IntegerField(null=True)
  zoneName = models.CharField(max_length=200,null=True)
  sectionId = models.IntegerField(null=True)
  sectionName = models.CharField(max_length=200,null=True)
  row = models.CharField(max_length=200)
  seatNumbers = models.CharField(max_length=200)
  currentPrice = models.FloatField()

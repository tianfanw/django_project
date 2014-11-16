from django.db import models

# Create your models here.
class Event(models.Model):
  id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=200,null=True)
  venue = models.CharField(max_length=100,null=True)
  primaryPerformer = models.CharField(max_length=200,null=True)
  secondaryPerformer = models.CharField(max_length=200,null=True)
  grouping = models.CharField(max_length=100,null=True)

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

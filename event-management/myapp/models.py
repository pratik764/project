from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(upload_to="profile_picture/default.jpg")
	usertype=models.CharField(max_length=100,default="user")

	def __str__(self):
		return self.fname+" "+self.lname

class Event(models.Model):
	manager=models.ForeignKey(User,on_delete=models.CASCADE)
	event_name=models.CharField(max_length=100)
	event_date=models.CharField(max_length=100)
	event_time=models.CharField(max_length=100)
	event_venue=models.TextField()
	event_picture=models.ImageField(upload_to="event_picture/")
	event_price=models.PositiveIntegerField()

	def __str__(self):
		return self.manager.fname+" - "+self.event_name	

class BookEvent(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	event=models.ForeignKey(Event,on_delete=models.CASCADE)
	event_price=models.PositiveIntegerField()
	ticket_qty=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField(default=0)
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return self.user.fname+" - "+self.event.event_name		
from django.shortcuts import render,redirect
from .models import User,Event,BookEvent
import requests
import random
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'


@csrf_exempt
def create_checkout_session(request):
	user=User.objects.get(email=request.session['email'])
	#amount = int(json.load(request)['post_data'])
	#be=int(json.load(request)['post_data1'])
	#print(be)
	data=json.load(request)
	amount=int(data['post_data'])
	be=int(data['post_data1'])
	bookevent=BookEvent.objects.get(pk=be)
	bookevent.payment_status=True
	bookevent.save()
	print(bookevent.user.fname)
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	print(session.id)
	return JsonResponse({'id': session.id})

def success(request):
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

# Create your views here.
def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="user":
			return render(request,'index.html')
		else:
			return render(request,'manager-index.html')
	except:				
		return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def rent_venue(request):
	return render(request,'rent-venue.html')

def shows_events(request):
	events=Event.objects.all()
	return render(request,'shows-events.html',{'events':events})

def tickets(request):
	return render(request,'tickets.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Alredy Registered"
			return render(request,'login.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_picture=request.FILES['profile_picture'],
						usertype=request.POST['usertype']
				)
			msg="User Sign Up Successfully"
			return render(request,'login.html',{'msg':msg})
		else:
			msg="password & Confirm Password Dose Not Matched"
			return render(request,'signup.html',{'msg':msg})	
	else:		
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_picture']=user.profile_picture.url
				if user.usertype=="user":
					return render(request,'index.html')
				else:
					return render(request,'manager-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'signup.html',{'msg':msg})
	else:	
		return render(request,'login.html')		

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})	

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				msg="Password Change Successfully"
				del request.session['email']
				del request.session['fname']
				return render(request,'login.html',{'msg':msg})
			else:
				msg="New Password & Confirm New Password Dose Not Matched"
				if user.usertype=="user":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'manager-change-password.html',{'msg':msg})
		else:
			msg="Old Password Dose Not Matched"
			if user.usertype=="user":	
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'manager-change-password.html',{'msg':msg})			
	else:	
		if user.usertype=="user":
			return render(request,'change-password.html')
		else:
			return render(request,'manager-change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			otp=str(random.randint(1000,9999))
			mobile=str(request.POST['mobile'])
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"flpSsL9oOwDtHyxXLA5dRupXuOwr7IQEC8QWoMVEM3IU0oo122Kk6LrX1yMH","variables_values":otp,"route":"otp","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			return render(request,'otp.html',{'otp':otp,'mobile':mobile})
		except:
			msg="Mobile Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})	
	else:	
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	mobile=request.POST['mobile']

	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'otp':otp,'mobile':mobile,'msg':msg})	

def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Dose Not Matched"
		return render(request,'new-password.html',{'mobile':mobile,'msg':msg})	

def profile(request):
    user = User.objects.get(email=request.session['email'])

    if request.method == "POST":
        user.fname = request.POST.get('fname')
        user.lname = request.POST.get('lname')
        user.mobile = request.POST.get('mobile')
        user.address = request.POST.get('address')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()

        # Update session with profile picture URL if it exists
        if user.profile_picture:
            request.session['profile_picture'] = user.profile_picture.url

        msg = "Profile Updated Successfully"

        # Redirect based on user type
        if user.usertype == "user":
            return render(request, 'profile.html', {'user': user, 'msg': msg})
        else:
            return render(request, 'manager-profile.html', {'user': user})

    else:
        # Render the profile page based on user type
        if user.usertype == "user":
            return render(request, 'profile.html', {'user': user})
        else:
            return render(request, 'manager-profile.html', {'user': user})

def manager_add_event(request):
	if request.method=="POST":
		manager=User.objects.get(email=request.session['email'])
		Event.objects.create(
				manager=manager,
				event_name=request.POST['event_name'],
				event_date=request.POST['event_date'],
				event_time=request.POST['event_time'],
				event_venue=request.POST['event_venue'],
				event_picture=request.FILES['event_picture'],
				event_price=request.POST['event_price']
			)
		msg="Event Added Successfully"
		return render(request,'manager-add-event.html',{'msg':msg})
	else:	
		return render(request,'manager-add-event.html')

def manager_view_event(request):
	manager=User.objects.get(email=request.session['email'])
	events=Event.objects.filter(manager=manager)
	return render(request,'manager-view-event.html',{'events':events})

def manager_edit_event(request, pk):
    event=Event.objects.get(pk=pk)
    
    if request.method == "POST":
        # Gather input data
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        event_venue = request.POST.get('event_venue')
        event_price = request.POST.get('event_price')
        event_picture = request.FILES.get('event_picture')  # Assuming picture is a file upload
        
        # Validate and assign
        try:
            event.event_name = event_name
            event.event_date = event_date
            event.event_time = event_time
            event.event_venue = event_venue

            # Convert event_price to the correct type, ensuring it's a valid number
            if event_price:
                event.event_price = float(event_price)
            else:
                raise ValidationError("Event price cannot be empty.")

            # If a new picture is uploaded, update it
            if event_picture:
                event.event_picture = event_picture
            
            # Save the updated event
            event.save()

            msg = "Event Updated Successfully"
        except ValueError:
            msg = "Invalid input for event price. Please enter a valid number."
        except ValidationError as e:
            msg = str(e)

        return render(request, 'manager-edit-event.html', {'event': event, 'msg': msg})
    
    # For GET request, just render the form with the existing event data
    return render(request, 'manager-edit-event.html', {'event': event})	

def manager_delete_event(request,pk):
	event=Event.objects.get(pk=pk)
	event.delete()
	return redirect('manager-view-event')

def event_details(request,pk):
	event=Event.objects.get(pk=pk)
	return render(request,'event-details.html',{'event':event})	

def book_event(request,pk):
	event=Event.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		BookEvent.objects.create(
			user=user,
			event=event,
			event_price=event.event_price,
			ticket_qty=int(request.POST['ticket_qty']),
			total_price=event.event_price*int(request.POST['ticket_qty']),
			)
		msg="Event Booked Successfully"
		events=BookEvent.objects.filter(user=user)
		return render(request,'myevents.html',{'events':events,'msg':msg})
	else:	
		return render(request,'book-event.html',{'event':event,'user':user})	

def myevents(request):
	user=User.objects.get(email=request.session['email'])
	events=BookEvent.objects.filter(user=user)
	return render(request,'myevents.html',{'events':events})

def payment(request,pk):
	bookevent=BookEvent.objects.get(pk=pk)
	total_price=bookevent.total_price
	be=bookevent.pk
	print("BE : ",be)
	return render(request,'payment.html',{'bookevent':bookevent,'total_price':total_price,'be':be})
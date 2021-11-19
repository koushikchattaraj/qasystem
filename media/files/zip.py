from email.message import Message
import json
import urllib
from django.db.models.indexes import Index
from django.http.response import HttpResponse
import requests
from .forms import *
from .models import *
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,View
import logging

app_logger = logging.getLogger('aviox-logger')


class IndexView(TemplateView):
	template = 'aviox_app/index.html'

	def get(self, request):
		app_logger.info(f"In the {IndexView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

	def post(self,request):
		app_logger.info(f"In the {IndexView.__name__} class and {request.method} method.")
			
		try:
			if request.method=='POST':
				form = RegForm(request.POST)
				if form.is_valid():
					app_logger.info(f"Transfer in the {RegForm.__name__} form  for save data.")
					recaptcha_response = request.POST.get('g-recaptcha-response')
					url = 'https://www.google.com/recaptcha/api/siteverify'
					values = {
						'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
						'response': recaptcha_response
						}
					data = urllib.parse.urlencode(values).encode()
					req =  urllib.request.Request(url, data=data)
					response = urllib.request.urlopen(req)
					result = json.loads(response.read().decode())
					app_logger.info(f"reCAPTCHA validation is Sucessful.")
					#print(result)
				
					''' End reCAPTCHA validation '''
					if result['success']:
						app_logger.info("Filed are store into variable")
						fullname = request.POST.get('fullname')
						emailid = request.POST.get('email')
						country = request.POST.get('country')
						isd = request.POST.get('isd')
						phone = request.POST.get('phone')
						message = request.POST.get('message')
						app_logger.info("data are store into email")
						email = EmailMessage('Aviox Home Page', f'Name :: {fullname}\n Email :: {emailid}\n country :: {country}\n phone :: {isd} {phone}\n Message :: {message}' , to=settings.EMAIL_TO)
						app_logger.info(f"Email send to admin.")
						email.send()
						app_logger.info(f"Email send to admin.")
						form.save()
						app_logger.info(f"Transfer Index form data in to database.")
						messages.success(request, 'Thanks for contacting us!!')
					else:
						messages.error(request, 'Invalid reCAPTCHA. Please try again.')
						app_logger.error(f"Invalid reCAPTCHA. Please try again.")
				else:
					messages.error(request,"please enter correct data you have entered invalid data")
					app_logger.error("Error is Enter incorrect data")
			return HttpResponseRedirect('/#contactus')
		except Exception as e:
			app_logger.error(f"Something went wrong {str(e)}")
			return render(request,"aviox_app/500.html", {})


class AboutView(TemplateView):
	template = 'aviox_app/about.html'
	def get(self, request):
		app_logger.info(f"In the {AboutView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class ContactView(TemplateView):
	template = 'aviox_app/contact.html'
	def get(self, request):
			
		app_logger.info(f"In the {ContactView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

	def post(self,request):
		app_logger.info(f"In the {ContactView.__name__} class and {request.method} method.")
		try:
			# form = ContactForm(request.POST)
			# if form.is_valid():
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			app_logger.info(f"reCAPTCHA Validation Sucessfully")
			''' End reCAPTCHA validation '''
			if result['success']:
				f_name = request.POST.get('name')
				l_name = request.POST.get('last_name')
				email = request.POST.get('email')
				country_code = request.POST.get('country_code')
				phone = request.POST.get('phone')
				message = request.POST.get('message')
				app_logger.info("Contact View Form send to form variable")
				instance = ContactUs(
					name=f"{f_name} {l_name}",
					email=email,
					country_code=country_code,
					phone=phone,
					message=message
				)
				
				instance.save()

				app_logger.info(f"email send Contact Us Form.")
				email = EmailMessage('Aviox Contact Page', f'Name:: {f_name} {l_name}\n Email :: {email}\n Phone::{phone}\n Message:: {message}', to=settings.EMAIL_TO)
				email.send()
				
				app_logger.info(f"Contact Us from sucessfully submited")
				messages.success(request, 'Thanks for contacting us!!')
				
				return redirect('contact')

				#return render(request, self.post, {})
			else:
    			#
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
				app_logger.error(f"Invalid reCAPTCHA. Please try again.")
				
				return redirect('contact')
		except Exception as e:
			app_logger.error(f"Something went wrong {str(e)}")
			return render(request, "aviox_app/500.html", {})
			
	
				

#======================services===================
class ServiceView(TemplateView):
	template = 'aviox_app/services.html'
	def get(self, request):
		app_logger.info(f"In the {ServiceView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class MobileDevView(TemplateView):
	template = 'aviox_app/mobile-development.html'
	def get(self, request):
		app_logger.info(f"In the {MobileDevView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class WebDevView(TemplateView):
	template = 'aviox_app/php-frameworks.html'
	def get(self, request):
		app_logger.info(f"In the {WebDevView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class WebDesignView(TemplateView):
	template = 'aviox_app/designing-services.html'
	def get(self, request):
		app_logger.info(f"In the {WebDesignView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class MvcView(TemplateView):
	template = 'aviox_app/mvc.html'
	def get(self, request):
		app_logger.info(f"In the {MvcView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class CmsView(TemplateView):
	template = 'aviox_app/cms-development.html'
	def get(self, request):
		app_logger.info(f"In the {CmsView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class ApiView(TemplateView):
	template = 'aviox_app/api-integration.html'
	def get(self, request):
		app_logger.info(f"In the {ApiView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class SeoView(TemplateView):
	template = 'aviox_app/seo.html'
	def get(self, request):
		app_logger.info(f"In the {SeoView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class PythonView(TemplateView):
	template = 'aviox_app/python.html'
	def get(self, request):
		app_logger.info(f"In the {PythonView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

#==================================sub-menus==============================
class IosPageView(View):
	template = 'aviox_app/sub-services/ios-application.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {IosPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class MobilePageView(View):
	template = 'aviox_app/sub-services/mobile-application.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {MobilePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})
class ReactPageView(View):
	template = 'aviox_app/sub-services/react-native.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {ReactPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})
#=======================php================
class LaravelPageView(View):
	template = 'aviox_app/sub-services/laravel-development.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {LaravelPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class YiiPageView(View):
	template = 'aviox_app/sub-services/yii-development.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {YiiPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class ZendPageView(View):
	template = 'aviox_app/sub-services/zend-framework.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {ZendPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class CakePageView(View):
	template = 'aviox_app/sub-services/cake-php.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {CakePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class SymfonyPageView(View):
	template = 'aviox_app/sub-services/symfony-development.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {SymfonyPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})


#==================mvc=======================
class AngularPageView(View):
	template = 'aviox_app/sub-services/angular-js.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {AngularPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class NodePageView(View):
	template = 'aviox_app/sub-services/node-js.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {NodePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class VuePageView(View):
	template = 'aviox_app/sub-services/vue-js.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {VuePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class KnockoutPageView(View):
	template = 'aviox_app/sub-services/knockout.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {KnockoutPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class ReactJsPageView(View):
	template = 'aviox_app/sub-services/react-js.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {ReactJsPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

#=========================design=======================
class UiPageView(View):
	template = 'aviox_app/sub-services/ui-design.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {UiPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class FrontPageView(View):
	template = 'aviox_app/sub-services/front-end.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {FrontPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})
class ResponsivePageView(View):
	template = 'aviox_app/sub-services/responsive-website-design.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {ResponsivePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class MobileApplicationPageView(View):
	template = 'aviox_app/sub-services/mobile-application-design.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {MobileApplicationPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class DesignPageView(View):
	template = 'aviox_app/sub-services/design-prototype.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {DesignPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

#======================cms===================			
class WordpressPageView(View):
	template = 'aviox_app/sub-services/wordpress-website.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {WordpressPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class JoomlaPageView(View):
	template = 'aviox_app/sub-services/joomla-website.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {JoomlaPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class DrupalPageView(View):
	template = 'aviox_app/sub-services/drupal-cms.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {DrupalPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

#==================api-integration=====================

class PaymentPageView(View):
	template = 'aviox_app/sub-services/payment-api.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {PaymentPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class AuthenticationPageView(View):
	template = 'aviox_app/sub-services/authentication-api.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {AuthenticationPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class ShippingPageView(View):
	template = 'aviox_app/sub-services/shipping-api.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {ShippingPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class PhonePageView(View):
	template = 'aviox_app/sub-services/phone-verification.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {PhonePageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

#=========================seo=============
class SeoPageView(View):
	template = 'aviox_app/sub-services/sco.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {SeoPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

class SmoPageView(View):
	template = 'aviox_app/sub-services/smo.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {SmoPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class PpcPageView(View):
	template = 'aviox_app/sub-services/ppc.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {PpcPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	


class OrmPageView(View):
	template = 'aviox_app/sub-services/orm.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {OrmPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

#==========================python====================
class DjangoPageView(View):
	template = 'aviox_app/sub-services/django.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {DjangoPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class FlaskPageView(View):
	template = 'aviox_app/sub-services/flask.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {FlaskPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class FastapiPageView(View):
	template = 'aviox_app/sub-services/fastapi.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {FastapiPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class Webapp2PageView(View):
	template = 'aviox_app/sub-services/webapp2.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {Webapp2PageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	

class Web2pyPageView(View):
	template = 'aviox_app/sub-services/web2py.html'

	def get(self,request,**kwargs):
		app_logger.info(f"In the {Web2pyPageView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	





class PortfolioView(TemplateView):
	template = 'aviox_app/portfolio.html'
	def get(self, request):
		app_logger.info(f"In the {PortfolioView.__name__} class and {request.method} method.")
		return render(request, self.template, {})	
	

class CareerView(TemplateView):
	template = 'aviox_app/career.html'
	
	def get(self, request):
		app_logger.info(f"In the {CareerView.__name__} class and {request.method} method.")
		return render(request, self.template, {})

	def post(self,request):		
			app_logger.info(f"In the {CareerView.__name__} class and {request.method} method.")
			try:
				firstname = request.POST.get('firstname')
				lastname = request.POST.get('lastname')
				date = request.POST.get('date')
				qualification = request.POST.get('user_qualification')
				file = request.FILES.get('file')
				number = request.POST.get('number')
				email = request.POST.get('email')
				message = request.POST.get('message')
				post1= request.POST.get('title_name')

				app_logger.info("Career View Form send to form variable")

				form = ApplyJob(firstname=firstname,lastname=lastname,date=date,number=number,qualification=qualification,email=email,file=file
						,message=message,job_title=post1)
				# form.save()

				################

				email = EmailMessage(f'Apply for Job {post1}',f'Name :: {firstname} {lastname}\n Phone Number :: {number} \n Email :: {email}\n Qualification :: {qualification} \n Message :: {message}' , to=settings.EMAIL_TO)
				email.attach(file.name,file.read(),file.content_type)

				email.send()
				app_logger.info(f"email send Career page Form.")

				################
				app_logger.info(f"Transfer in the Career page  form  for save data.")
				form.save()
				
		
				messages.success(request, 'Thanks, We will respond to your query within 24 hours. Please stand by until you will hear from us!!')
				app_logger.info(f"Career page  form  for save data succesfully save.")
				# else:
				# 	messages.success(request, 'Something went wrong')
				return render(request, self.template, {})
			except Exception as e:
				app_logger.error(f"Something went wrong {str(e)}")
				return render(request,"aviox_app/500.html", {})


class BlogView(TemplateView):
	template = 'aviox_app/blog.html'
	def get(self, request):
		app_logger.error(f"In the {BlogView.__name__} class and {request.method} method.")
		return render(request, self.template, {})						
 

def error_404(request, exception):
	app_logger.error(f"In the {error_404.__name__} function.")
	data = {}
	return render(request,'aviox_app/404.html', data)


def error_500(request):
	app_logger.error(f"In the {error_500.__name__} function.")
	data = {}
	return render(request,'aviox_app/500.html', data)
    
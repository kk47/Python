# coding: utf-8
from django import forms
from models import *
#from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget

class FormRoom(forms.ModelForm):
        class Meta:
                model = Room

class FormSwitch(forms.ModelForm):
	idroom = forms.ModelChoiceField(queryset=Room.objects.all(),widget=forms.Select(),empty_label=None,label='机柜' )
        class Meta:
                model = Switch




class FormMac(forms.ModelForm):
	idroom = forms.ModelChoiceField(queryset=Room.objects.all(),widget=forms.Select(),empty_label=None,label='机柜' )
	class Meta:
		model = Mac

	
class  FormServer(forms.ModelForm):
	idroom = forms.ModelChoiceField(queryset=Room.objects.all(),widget=forms.Select(),empty_label=None,label='机柜' )
	start_time = forms.DateTimeField(error_messages={'required':u'必填:时间格式0000-00-00'},label='开始时间')
	end_time = forms.DateTimeField(error_messages={'required':u'必填:时间格式0000-00-00'},label='截止时间')
	class Meta:
		model = Server
		exclude = ('is_avlie',);


class  FormRepair(forms.ModelForm):
        class Meta:
                model = Repair




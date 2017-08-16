# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import random
from django.db import transaction
import reportlab
from constants import *

#pdf modules
from io import BytesIO
from reportlab.pdfgen import canvas
#from django.http import HttpResponse
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

from django.db.models import Max


from quizapp.models import QuizLogin,School,Question,Quizattended,Quizdetails

# Create your views here.

def index(request):
	'''loginobj = QuizLogin.objects.all()
	for user in loginobj:
		if user is not None:
			print user.username'''
	return render(request, 'quizapp/index.html')

def loginpage(request):
	'''loginobj = QuizLogin.objects.all()
	for user in loginobj:
		if user is not None:
			print user.username'''
	return render(request, 'quizapp/index.html')

def loginrequest(request):
	uname = request.POST.get('uname')
	pwd = request.POST.get('pwd')
	if QuizLogin.objects.filter(username=uname, password=pwd).exists():
		request.session['sessionuname']=uname
		loginobject = QuizLogin.objects.filter(username=uname, password=pwd)
		if loginobject[0].usertype == 'STUDENT':
			return render(request, 'quizapp/homepage.html',{'username':uname, 'usertype':loginobject[0].usertype})
		else:
			return render(request, 'quizapp/teacherhomepage.html',{'username':uname, 'usertype':loginobject[0].usertype})
	else:
		return render(request, 'quizapp/index.html', {'loginmsg':'Login Failed.'})
	return HttpResponse(uname+pwd)

def homeviewurl(request):
	return render(request, 'quizapp/homeview.html')

def signuppage(request):
	return render(request, 'quizapp/signuppage.html')

def startquizpage(request):
	return render(request, 'quizapp/startquizpage.html')

def quizreportpage(request):
	return render(request, 'quizapp/quizreportpage.html')

def teacherhomeviewurl(request):
	return render(request, 'quizapp/teacherhomeview.html')

def performance(request):
	return render(request, 'quizapp/performance.html')

def leaderboard(request):
	return render(request, 'quizapp/leaderboard.html')


'''
def signuprequest(request):
	uname = request.POST.get('uname')
	pwd = request.POST.get('pwd')
	confirmpwd = request.POST.get('confirmpwd')
	if pwd != confirmpwd:
		return render(request, 'quizapp/signuppage.html', {"errmsg":"Passwords should be same.", "uservalue":uname})
	elif QuizLogin.objects.filter(username__iexact=uname).exists():
		return render(request, 'quizapp/signuppage.html', {"errmsg":"User already existing.", "uservalue":""})
	elif uname==None or pwd==None or confirmpwd==None:
		return render(request, 'quizapp/signuppage.html', {"errmsg":"Fields cannot be null.", "uservalue":uname})
	else:
		quizloginobject=QuizLogin(username=uname, password=pwd).save()
		return render(request, 'quizapp/index.html')
	#return HttpResponse(uname+pwd+confirmpwd)
'''

def getschools(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	schoolobject = School.objects.all()
	for school in schoolobject:
		dict_single_row['schoolid']=school.schoolid
		dict_single_row['schoolname']=school.schoolname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['Schools'] = list_of_rows
	response = JsonResponse(dict_full_content, safe=False)
	return HttpResponse(response)



@csrf_protect
def signuprequest(request):
	if request.method == 'POST':
		print request.body
		params = json.loads(request.body)
		uname = params['uname']
		pwd = params['pwd']
		confirmpwd = params['confirmpwd']
		selectedschool = params['selectedschool']
		user_type = params['usertype']
		std = params['std']
		city = params['city']
		if user_type == 'TEACHER':
			quizloginobject=QuizLogin(username=uname, password=pwd, usertype=user_type, city=city, schoolid_id=selectedschool).save()
		else:
			quizloginobject=QuizLogin(username=uname, password=pwd, usertype=user_type, city=city, schoolid_id=selectedschool, standard=std).save()

		#print uname+pwd+confirmpwd
		'''if pwd != confirmpwd:
			return render(request, 'quizapp/signuppage.html', {"errmsg":"Passwords should be same.", "uservalue":uname})
		elif QuizLogin.objects.filter(username__iexact=uname).exists():
			return render(request, 'quizapp/signuppage.html', {"errmsg":"User already existing.", "uservalue":""})
		elif uname==None or pwd==None or confirmpwd==None:
			return render(request, 'quizapp/signuppage.html', {"errmsg":"Fields cannot be null.", "uservalue":uname})
		else:
			quizloginobject=QuizLogin(username=uname, password=pwd).save()
			return render(request, 'quizapp/index.html')'''
		return HttpResponse("success")

def logout(request):
	try:
		del request.session['sessionuname']
		return render(request, 'quizapp/index.html')
	except Exception as e:
		return render(request, 'quizapp/index.html')

def startaquiz(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if 'POST'=='POST':		
		#print random.randint(1,4)
		questioncount = Question.objects.all().count()
		question_start_id = random.randint(1,questioncount)
		questionobject = Question.objects.filter(qid=question_start_id)
		request.session['currentqid'] = question_start_id
		request.session['currentscore'] = 0
		request.session['currentquestionno'] = 1

		#insearting a quiz
		loginobj = QuizLogin.objects.filter(username=request.session['sessionuname'])
		quizattendedobject = Quizattended(userid_id = loginobj[0].userid, score=0)
		quizattendedobject.save()
		request.session['currentquizid'] = quizattendedobject.quizid
		quizdetailsobj = Quizdetails(quizid_id=quizattendedobject.quizid, qid_id=request.session['currentqid']).save()

		for singlequestion in questionobject:
			dict_single_row['qid']=singlequestion.qid
			dict_single_row['question']=singlequestion.question
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Question'] = list_of_rows

		dict_single_row = {}
		list_of_rows = []
		optionlist = questionobject[0].options.split(',')
		for option in optionlist:
			dict_single_row['option']=option
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Options'] = list_of_rows
		dict_full_content['qtype'] = questionobject[0].qtype
		if questionobject[0].qtype == 'MULTIPLE':
			request.session['currentqmark'] = 1
			request.session['examtotal'] = 1
		else: #if essay question then
			keycount = len(questionobject[0].options.split(','))
			request.session['currentqmark'] = keycount
			request.session['examtotal'] = keycount
		dict_full_content['currentqmark'] = request.session['currentqmark']
		dict_full_content['examtotal'] = request.session['examtotal']
		response = JsonResponse(dict_full_content, safe=False)
		return HttpResponse(response)
	else:
		return HttpResponse("Only post request is possible.")

def submitnext(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if request.method=='POST':
		print request.body
		params = json.loads(request.body)
		answeredvalue = params['answeredvalue']
		questionobject = Question.objects.filter(qid=request.session['currentqid'])
		quizdetailsobj = Quizdetails.objects.filter(qid_id=request.session['currentqid'], quizid_id=request.session['currentquizid']).update(answeredoption=answeredvalue)
		if questionobject[0].qtype == "MULTIPLE": #evaluate objective questions
			if questionobject[0].correct == answeredvalue: #answer correct
				request.session['currentscore'] = request.session['currentscore'] + 1
		else: #evaluate essay questions
			keylist = questionobject[0].options.split(',')
			answeredvalue = answeredvalue.replace('.',' ')
			answeredlist = answeredvalue.split(' ')
			for keyvalue in keylist:
				if keyvalue in answeredlist:
					request.session['currentscore'] = request.session['currentscore'] + 1
		quizattendedobj = Quizattended.objects.filter(quizid=request.session['currentquizid']).update(score=request.session['currentscore'])
		#print request.session['currentscore']
		allquestions = Question.objects.all()
		if request.session['currentqid'] == allquestions.latest('qid').qid:
			request.session['currentqid'] = 1
		else:
			request.session['currentqid'] = request.session['currentqid'] + 1
		request.session['currentquestionno'] = request.session['currentquestionno'] + 1

		if request.session['currentquestionno'] <= NO_OF_QUESTIONS:
			quizdetailsobj = Quizdetails(quizid_id=request.session['currentquizid'], qid_id=request.session['currentqid']).save()
		questionobject = Question.objects.filter(qid=request.session['currentqid'])
		for singlequestion in questionobject:
			dict_single_row['qid']=singlequestion.qid
			dict_single_row['question']=singlequestion.question
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Question'] = list_of_rows

		dict_single_row = {}
		list_of_rows = []
		optionlist = questionobject[0].options.split(',')
		for option in optionlist:
			dict_single_row['option']=option
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Options'] = list_of_rows
		dict_full_content['qtype'] = questionobject[0].qtype
		dict_full_content['qno'] = request.session['currentquestionno']
		dict_full_content['score'] = request.session['currentscore']

		if questionobject[0].qtype == 'MULTIPLE':
			request.session['currentqmark'] = 1
			request.session['examtotal'] = request.session['examtotal'] + 1
		else: #if essay question then
			keycount = len(questionobject[0].options.split(','))
			request.session['currentqmark'] = keycount
			request.session['examtotal'] = request.session['examtotal'] + keycount
		dict_full_content['currentqmark'] = request.session['currentqmark']
		dict_full_content['examtotal'] = request.session['examtotal']

		response = JsonResponse(dict_full_content, safe=False)
		#print response
		return HttpResponse(response)
		#return HttpResponse("Success")
	else:
		return HttpResponse("Only post request is possible.")

def skipanswer(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if 'POST'=='POST':
		quizdetailsobj = Quizdetails.objects.filter(qid_id=request.session['currentqid'], quizid_id=request.session['currentquizid']).update(answeredoption="SKIPPED")
		questionobject = Question.objects.filter(qid=request.session['currentqid'])
		allquestions = Question.objects.all()
		if request.session['currentqid'] == allquestions.latest('qid').qid:
			request.session['currentqid'] = 1
		else:
			request.session['currentqid'] = request.session['currentqid'] + 1
		request.session['currentquestionno'] = request.session['currentquestionno'] + 1

		if request.session['currentquestionno'] <= NO_OF_QUESTIONS:
			quizdetailsobj = Quizdetails(quizid_id=request.session['currentquizid'], qid_id=request.session['currentqid']).save()
		questionobject = Question.objects.filter(qid=request.session['currentqid'])
		for singlequestion in questionobject:
			dict_single_row['qid']=singlequestion.qid
			dict_single_row['question']=singlequestion.question
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Question'] = list_of_rows

		dict_single_row = {}
		list_of_rows = []
		optionlist = questionobject[0].options.split(',')
		for option in optionlist:
			dict_single_row['option']=option
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Options'] = list_of_rows
		dict_full_content['qtype'] = questionobject[0].qtype
		dict_full_content['qno'] = request.session['currentquestionno']
		dict_full_content['score'] = request.session['currentscore']

		if questionobject[0].qtype == 'MULTIPLE':
			request.session['currentqmark'] = 1
			request.session['examtotal'] = request.session['examtotal'] + 1
		else: #if essay question then
			keycount = len(questionobject[0].options.split(','))
			request.session['currentqmark'] = keycount
			request.session['examtotal'] = request.session['examtotal'] + keycount
		dict_full_content['currentqmark'] = request.session['currentqmark']
		dict_full_content['examtotal'] = request.session['examtotal']
		response = JsonResponse(dict_full_content, safe=False)
		#print response
		return HttpResponse(response)
		#return HttpResponse("Success")
	else:
		return HttpResponse("Only post request is possible.")

def getallquiz(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	loginobj = QuizLogin.objects.filter(username=request.session['sessionuname'])
	quizattendedobject = Quizattended.objects.filter(userid_id=loginobj[0].userid)
	for quiz in quizattendedobject:
		dict_single_row['quizid']=quiz.quizid
		dict_single_row['score']=quiz.score
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['Quizids'] = list_of_rows
	response = JsonResponse(dict_full_content, safe=False)
	return HttpResponse(response)

def getquizdetails(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if request.method=='POST':
		#print request.body
		params = json.loads(request.body)
		quiz_id = params['quizid']
		quizdetailsobject = Quizdetails.objects.filter(quizid_id=quiz_id).select_related()
		for quizdetail in quizdetailsobject:
			wrongflag=True
			dict_single_row['question']=quizdetail.qid.question
			dict_single_row['answeredoption']=quizdetail.answeredoption
			questionobject = Question.objects.filter(qid=quizdetail.qid_id)
			if questionobject[0].qtype == "MULTIPLE":
				if questionobject[0].correct == quizdetail.answeredoption:
					dict_single_row['status']=True
				else:
					dict_single_row['status']=False
			else:
				keylist = questionobject[0].options.split(',')
				answeredvalue = quizdetail.answeredoption.replace('.',' ')
				answeredlist = answeredvalue.split(' ')
				for keyvalue in keylist:
					if keyvalue in answeredlist:
						dict_single_row['status']=True
						wrongflag = False
						break
				if wrongflag==True:
					dict_single_row['status']=False
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Quizdetails'] = list_of_rows
		response = JsonResponse(dict_full_content, safe=False)
		#print response
		return HttpResponse(response)
		#return HttpResponse("Success")
	else:
		return HttpResponse("Only post request is possible.")

def getstudents(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	loginobj = QuizLogin.objects.filter(usertype='STUDENT')
	for student in loginobj:
		dict_single_row['userid']=student.userid
		dict_single_row['username']=student.username
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['Students'] = list_of_rows
	response = JsonResponse(dict_full_content, safe=False)
	return HttpResponse(response)

def getallquizforuid(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if request.method=='POST':
		params = json.loads(request.body)
		uid = params['uid']
		quizattendedobject = Quizattended.objects.filter(userid_id=uid)
		for quiz in quizattendedobject:
			dict_single_row['quizid']=quiz.quizid
			dict_single_row['score']=quiz.score
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['Quizids'] = list_of_rows
		response = JsonResponse(dict_full_content, safe=False)
		return HttpResponse(response)
	else:
		return HttpResponse("only post request is possible.")

def getleaderdata(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	studexist = []
	if request.method=='POST':
		print request.body
		params = json.loads(request.body)
		filtertype = params['filtertype']
		if filtertype == 'ALL':
			print "ALL"
			quizattendedobject = Quizattended.objects.all().order_by('-score').select_related()
			for quiz in quizattendedobject:
				if quiz.userid_id not in studexist:
					studexist.append(quiz.userid_id)
				else:
					continue
				dict_single_row['username']=quiz.userid.username
				schoolobj = School.objects.filter(schoolid=quiz.userid.schoolid_id)
				dict_single_row['school']=schoolobj[0].schoolname
				dict_single_row['city']=quiz.userid.city
				dict_single_row['score']=quiz.score
				list_of_rows.append(dict_single_row.copy())
		elif filtertype == 'CITY':
			quizattendedobject = Quizattended.objects.all().select_related()
			for quiz in quizattendedobject:
				dict_single_row['username']=quiz.userid.username
				schoolobj = School.objects.filter(schoolid=quiz.userid.schoolid_id)
				dict_single_row['school']=schoolobj[0].schoolname
				dict_single_row['city']=quiz.userid.city
				dict_single_row['score']=quiz.score
				list_of_rows.append(dict_single_row.copy())
		else:
			print "SCHOOL"			
		
		dict_full_content['Leader'] = list_of_rows
		response = JsonResponse(dict_full_content, safe=False)
		#print response
		return HttpResponse(response)
		#return HttpResponse("success")
	else:
		return HttpResponse("only post request is possible.")

def loadcities(request):
	city_data_list = []
	loginobj = QuizLogin.objects.values('city').distinct()
	for user in loginobj:
		city_data_list.append(user['city'])
	response = JsonResponse(city_data_list, safe=False)
	return HttpResponse(response)

'''
def loadschools(request):
	school_data_list = []
	schoolobj = School.objects.all()
	for school in schoolobj:
		school_data_list.append(school.schoolname)
	response = JsonResponse(school_data_list, safe=False)
	return HttpResponse(response)
'''

def getfilteredleaderdata(request):
	dict_full_content = {}
	dict_single_row = {}
	list_of_rows = []
	if request.method=='POST':
		print request.body
		params = json.loads(request.body)
		filtertype = params['filtertype']
		cityvalue = params['city']
		school_id = params['schoolid']
		if filtertype == 'CITY':
			print "CITY"
			loginobj = QuizLogin.objects.filter(city__iexact=cityvalue)
			for user in loginobj:
				quizattendedobj = Quizattended.objects.filter(userid_id=user.userid).order_by('-score')[:1]
				if quizattendedobj.exists():
					for quiz in quizattendedobj:
						dict_single_row['username']=user.username
						schoolobj = School.objects.filter(schoolid=user.schoolid_id)
						dict_single_row['school']=schoolobj[0].schoolname
						dict_single_row['city']=user.city
						dict_single_row['score']=quiz.score
						list_of_rows.append(dict_single_row.copy())
		if filtertype == 'SCHOOL':
			loginobj = QuizLogin.objects.filter(schoolid_id=school_id)
			for user in loginobj:
				quizattendedobj = Quizattended.objects.filter(userid_id=user.userid).order_by('-score')[:1]
				if quizattendedobj.exists():
					for quiz in quizattendedobj:
						dict_single_row['username']=user.username
						schoolobj = School.objects.filter(schoolid=user.schoolid_id)
						dict_single_row['school']=schoolobj[0].schoolname
						dict_single_row['city']=user.city
						dict_single_row['score']=quiz.score
						list_of_rows.append(dict_single_row.copy())
		else:
			print "no operation"

		dict_full_content['Leader'] = list_of_rows
		response = JsonResponse(dict_full_content, safe=False)
		print response
		return HttpResponse(response)
		#return HttpResponse("success")
	else:
		return HttpResponse("only post request is possible.")

def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
    scorevalue = request.GET.get('scorevalue')
    totalvalue = request.GET.get('totalvalue')

    if int(scorevalue) <=2:
    	return HttpResponse("Minimum 3 is the pass mark")

    logo = ImageReader('https://vntesters.com/wp-content/uploads/2014/08/Certification_alphacertified.com_.au_.jpg')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.setFont('Helvetica-Bold', 13)
    p.drawString(170, 750, 'CERTIFICATE OF PARTICIPATION')
    # End writing

    loginobj = QuizLogin.objects.filter(username=request.session['sessionuname']).select_related()
    p.setFont('Helvetica-Bold', 10)
    str_content_text = "We certify that the student named "+ request.session['sessionuname'] + " of " +loginobj[0].schoolid.schoolname
    str_content_text2 = " school has passed the quiz program conducted by QUIZAPP with " + scorevalue + " points out of total of "+totalvalue + " points."
    p.drawString(170, 700, str_content_text)
    p.drawString(50, 680, str_content_text2)
    p.drawImage(logo, 250, 285, mask='auto', preserveAspectRatio=True, width=100)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


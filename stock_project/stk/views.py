from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import ldap
from django.template import loader
from django.template import Context, Template
from django.http import JsonResponse
from datetime import datetime
import json
import xlrd #package to work on excel sheets
import reportlab #package to make pdf
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from  reportlab.lib.styles import ParagraphStyle as PS
from django.db import transaction
from django.db import connection
from django.views.decorators.csrf import csrf_protect
#from stk.models import StkSample2
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from stk.models import stkCompanyMaster,stkStoreMaster,stkDept,stkLocation,stkPrivilegeGroup,stkLogintab,stkPrivilegeDescription,stkUnits,stkMainCategory,stkSubCategory, stkBrandMaster,stkModelMaster,stkItemMaster, stkFirmAccess, stkSupplier, stkPurchaseMaster, stkPurchaseInfo, stkPurchaseOrder, stkServiceCompany, stkOutgoing, stkAssembled, stkIssue, stkIssueDetails,  stkItemDetails, stkWarrantyOrAmc, stkPurchaseReturn, stkPurchaseReturnDetails, stkReturnFromDept, stkHealthStatus, stkCurrentStatus, stkSampleUpload, stkBreakdown


def index(request):
	'''request.session['session_empcode'] = "EMP56"
	print "session set..."
	request.session['session_firmid'] = 1
	firm_obj=stkCompanyMaster.objects.filter(firmid=1)
	query = "SELECT * FROM \"hrmBasicInfo\" WHERE empcode='EMP56'"
	result_data = dictFetchAll(cursorHelp(query))
	request.session['session_empid'] = result_data[0]['personalid']
	return render(request, 'stk/adminMain.html',{'user':result_data[0]['fullname'],'currentFirm':firm_obj[0].firmname})'''
	return render(request, 'stk/index.html') #only this line is required. remaining is just to trial login

def ldapCheck(username,password):
	ldap_server="cim.fisat.edu"
	# the following is the user_dn format provided by the ldap server
	user_dn = "uid="+username+",ou=Users,dc=fisat,dc=edu"
	# adjust this to your base dn for searching
	base_dn = "dc=fisat,dc=edu"
	connect = ldap.open(ldap_server)
	#search_filter = "uid="+username
	try:
		#if authentication successful, get the full user data
		connect.bind_s(user_dn,password)
		#result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
		# return all user data results
		connect.unbind_s()
		return True
		#print result
		#request.session['session_empcode'] = username
		#print "session set..."
		#return render(request, 'stk/adminMain.html')
		#return HttpResponse("Successfull login to ldap server." + str(result))
	except ldap.LDAPError:
		connect.unbind_s()
		print "authentication error"
		#msg="Username or password is incorrect."
		#return render(request, 'stk/index.html',{'msg': msg,'uname':username,})
		return False

def cursorHelp(query):
	cursor = connection.cursor()
	cursor.execute(query)
	return cursor


#LDAP login...
def loginrequest(request):
	username = request.POST.get('usertext').upper()
	password = request.POST.get('passwdtext')
	firm_id = request.POST.get('firm_select') #in the form number:firmid
	'''
	try:
		#delete all existing sessions...
		#del request.session['session_empcode']
		#del request.session['session_empid']
		#del request.session['session_firmid']
		del request.session['selected_store_id'] #It is for getting store name. All remaining will be recreated at login time.
	except:
		print "session delete before login request completed."
	'''
	try:
		if firm_id == '?':
			msg="Firm Required."
			return render(request, 'stk/index.html',{'msg': msg,'uname':username,})
		firm_id = str(firm_id).split(":",1)[1] #spliting only firmid part

		status = ldapCheck(username,password)
		if status == True:
			request.session['session_empcode'] = username
			print "session set..."
			#firmaccess_obj = stkFirmAccess.objects.filter(empcode=username)
			#request.session['session_firmid'] = firmaccess_obj[0].firmid_id
			request.session['session_firmid'] = int(firm_id)
			print "firmid set to "+str(request.session['session_firmid'])
			firm_obj=stkCompanyMaster.objects.filter(firmid=firm_id)
			query = "SELECT * FROM \"hrmBasicInfo\" WHERE empcode='"+username+"'"
			result_data = dictFetchAll(cursorHelp(query))
			request.session['session_empid'] = result_data[0]['personalid']
			return render(request, 'stk/adminMain.html',{'user':result_data[0]['fullname'],'currentFirm':firm_obj[0].firmname})
		else:
			msg="Username or password is incorrect."
			return render(request, 'stk/index.html',{'msg': msg,'uname':username,})
	except:
		return render(request, 'stk/index.html')

	'''ldap_server="cim.fisat.edu"
	# the following is the user_dn format provided by the ldap server
	user_dn = "uid="+username+",ou=Users,dc=fisat,dc=edu"
	# adjust this to your base dn for searching
	base_dn = "dc=fisat,dc=edu"
	connect = ldap.open(ldap_server)
	search_filter = "uid="+username
	try:
		#if authentication successful, get the full user data
		connect.bind_s(user_dn,password)
		result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
		# return all user data results
		connect.unbind_s()
		print result
		request.session['session_empcode'] = username
		print "session set..."
		return render(request, 'stk/adminMain.html')
		#return HttpResponse("Successfull login to ldap server." + str(result))
	except ldap.LDAPError:
		connect.unbind_s()
		print "authentication error"
		msg="Username or password is incorrect."
		return render(request, 'stk/index.html',{'msg': msg,'uname':username,})'''

@csrf_protect
def firmForLogin(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		emp_code= request.GET.get('emp_code')
		firm_details_obj = stkFirmAccess.objects.filter(empcode=emp_code).select_related()
		for firm in firm_details_obj:
			dict_single_row['firm_name'] = firm.firmid.firmname
			dict_single_row['firm_id'] = firm.firmid_id
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkCompanyMaster']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		print str(response.content)
		return HttpResponse(response.content)
	else:
		print "not post"
		return HttpResponse("Only Accicible with post request")

def logout(request):
	try:
		del request.session['session_empcode']
		del request.session['session_empid']
		del request.session['session_firmid']
		del request.session['selected_store_id']
		print "session unset..."
		return render(request, 'stk/index.html')
	#except KeyError:
	except:
		return render(request, 'stk/index.html')


#check session...
def checkSession(request):
	if 'session_empcode' not in request.session:
		return HttpResponse("failed")
	else:
		return HttpResponse("success")

#check whether any stores are selected...
@csrf_protect
def checkStoreSelected(request):
	dict_single_row={}
	list_of_rows = []
	if request.method == 'POST':
		if 'selected_store_id' not in request.session:
			return HttpResponse("failed") #store not already selected
		else:
			store_obj = stkStoreMaster.objects.defer('mainstorename').filter(storeid=request.session['selected_store_id'])
			dict_single_row['status'] = "success"
			dict_single_row['storename'] = store_obj[0].mainstorename
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only available with post request")

#function convert cursor to dictionary...
def dictFetchAll(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


	
def sampleurl(request):
	'''sample_names = StkSample2.objects.raw("SELECT * FROM \"hrmBasicInfo\"")
	for s in sample_names:
		print(s.fullname)
	return HttpResponse("success")'''
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM \"hrmBasicInfo\"")
	resultss = dictFetchAll(cursor)
	print(type(StkSample2.objects.all()))
	for i in resultss:
		print(i['empcode'])
	return HttpResponse("success")

'''def handler404(request):
    response = render_to_response('404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response'''

def adminHome(request):
	return render(request, 'stk/adminHome.html')

def firmReg(request):
	return render(request, 'stk/firmReg.html')

def mainstoreRegistration(request):
	return render(request, 'stk/mainstoreRegistration.html')

def locationRegistration(request):
	return render(request, 'stk/locationRegistration.html')

def connectStoreDept(request):
	return render(request, 'stk/connectStoreDept.html')

def unitRegistration(request):
	return render(request, 'stk/unitRegistration.html')

def subCategoryRegistration(request):
	return render(request, 'stk/subCategoryRegistration.html')

def itemRegistration(request):
	return render(request, 'stk/itemRegistration.html')

def supplierRegistration(request):
	return render(request, 'stk/supplierRegistration.html')

def purchase(request):
	return render(request, 'stk/purchase.html')

def issueItem(request):
	return render(request, 'stk/issue.html')

def existing(request):
	return render(request, 'stk/existing.html')

def purchaseReturn(request):
	return render(request, 'stk/purchaseReturn.html')

def returnFromDept(request):
	return render(request, 'stk/returnFromDept.html')

def outgoing(request):
	return render(request, 'stk/outgoing.html')

def miscellaneous(request):
	return render(request, 'stk/miscellaneous.html')

def searchsample(request):
	return render(request, 'stk/Search.html')

def samplepurchase(request):
	return render(request, 'stk/samplepurchase.html')

def itemRegistrationPreview(request):
	json_items_var = request.GET.get('jsondata')
	headingdata = request.GET.get('headingdata')
	json_items=json.loads(json_items_var)
	#print json_items
	return render(request, 'stk/itemRegistrationPreview.html',{'headingdata':headingdata, 'json_items':json_items})

def selectStore(request):
	query = "SELECT * FROM \"hrmBasicInfo\" WHERE empcode='"+request.session['session_empcode']+"'"
	result_data = dictFetchAll(cursorHelp(query))
	print result_data[0]['personalid']
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dependent_group_ids= stkLogintab.objects.filter(staffid = result_data[0]['personalid'])
	for dependent_group_id in dependent_group_ids:
		dependent_store_ids = stkPrivilegeGroup.objects.filter(groupid = dependent_group_id.groupid_id)
		for dependent_store_id in dependent_store_ids:
			storemaster_object = stkStoreMaster.objects.filter(storeid = dependent_store_id.storeid_id)
			print storemaster_object[0].mainstorename
			dict_single_row['storeid'] = storemaster_object[0].storeid
			dict_single_row['mainstorename'] = storemaster_object[0].mainstorename
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkStoreMaster']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

def confirmSelectedStore(request):
	store_id = request.GET.get('store_id')
	request.session['selected_store_id'] = store_id
	print "session store set"
	return HttpResponse("success")

#firm registration...
def firmRegistration(request):
	firm_name = request.GET.get('firm_name')
	firm_object = stkCompanyMaster(firmname = firm_name)
	firm_object.save()
	return HttpResponse("success")


def loadFirm(request):
	dict_full_content={}
	dict_single_row={}
	#head=("firmid","firmname")
	#dict.append(dict(zip(head,firm))
	list_of_rows=[]
	firm_object = stkCompanyMaster.objects.all()
	for firm in firm_object:
		dict_single_row['firmid'] = firm.firmid
		dict_single_row['firmname'] = firm.firmname
		storemaster_firmcount = stkStoreMaster.objects.filter(firmid=firm.firmid).count()
		if storemaster_firmcount == 0:
			dict_single_row['editable'] = 'true'  #can be edited
		else:
			dict_single_row['editable'] = 'false' #can't be edited
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkCompanyMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

def firmUpdate(request):
	firm_name = request.GET.get('firm_name')
	firm_id = request.GET.get('firm_id')
	try:
		with transaction.atomic():
			firm_obj= stkCompanyMaster.objects.filter(firmid=firm_id).update(firmname=firm_name)
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Mainstore Registration Failed.")

#delete firm...
def firmDelete(request):
	firm_id = request.GET.get('firm_id')
	try:
		with transaction.atomic():
			firm_obj = stkCompanyMaster.objects.filter(firmid=firm_id).delete()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Firm Deletion Failed.")



'''
def loadFirm(request):
	dict_full_content={}
	dict_single_row={}
	#head=("firmid","firmname")
	#dict.append(dict(zip(head,firm))
	list_of_rows=[]
	col=('firmid','firmname')
	firm_object = stkCompanyMaster.objects.all()
	for firm in firm_object:
		list_of_rows.append(dict(zip(col,firm)))
	
	return HttpResponse(json.dumps(list_of_rows), content_type="application/json")'''


def loadMainstores(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	mainstore_object = stkStoreMaster.objects.defer('storeid', 'mainstorename') #objects.values('col1_name','col2_name') will return result as dictionary
	for store in mainstore_object:
		dict_single_row['storeid'] = store.storeid
		dict_single_row['mainstorename'] = store.mainstorename
		list_of_rows.append(dict_single_row.copy())
	dict_single_row['storeid'] = '0'
	dict_single_row['mainstorename'] = 'INDEPENDENT STORE'
	list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkStoreMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

'''
@csrf_protect
def loadMainstores(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_data={}
		data=[]
		col=['mainstorename','storeid']
		mainstore_object = stkStoreMaster.objects.values('storeid','mainstorename') #objects.values('col1_name','col2_name') will return result as dictionary
		for store in mainstore_object:
			data.append(dict(zip(col,store.values())))
		dict_full_content['stkStoreMaster']=data
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
'''


#submit mainstore...
def mainstoreSubmit(request):
	main_store_name= request.GET.get('main_store_name')
	firm_id = request.GET.get('firm_id')
	under_which_store= request.GET.get('under_which_store')
	try:
		with transaction.atomic():
			storemaster_object = stkStoreMaster(mainstorename=main_store_name,firmid_id=firm_id,underwhichstore=under_which_store)
			storemaster_object.save()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Mainstore Registration Failed.")

def mainstoreTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	all_mainstores = stkStoreMaster.objects.all()
	for single_mainstore in all_mainstores:
		dict_single_row['mainstorename'] = single_mainstore.mainstorename
		dict_single_row['storeid'] = single_mainstore.storeid
		if single_mainstore.underwhichstore == 0:
			dict_single_row['understoreid'] = single_mainstore.underwhichstore
			dict_single_row['understorename'] = "INDEPENDENT STORE"
		else:
			understore_obj = stkStoreMaster.objects.filter(storeid=single_mainstore.underwhichstore)
			dict_single_row['understoreid'] = understore_obj[0].storeid  #store details corresponding to understore
			dict_single_row['understorename'] = understore_obj[0].mainstorename
		firm_obj = stkCompanyMaster.objects.filter(firmid=single_mainstore.firmid_id)
		dict_single_row['firmid'] = firm_obj[0].firmid
		dict_single_row['firmname'] = firm_obj[0].firmname
		#check whether editable...
		count_in_understore = stkStoreMaster.objects.filter(underwhichstore = single_mainstore.storeid).count()
		count_in_dept_table = stkDept.objects.filter(storeid_id=single_mainstore.storeid).count()
		if count_in_understore or count_in_dept_table > 0:
			dict_single_row['editable'] = 'false'
		else:
			dict_single_row['editable'] = 'true'  #can be edited
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkStoreMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#delete mainstore...
def deleteMainstore(request):
	store_id = request.GET.get('store_id')
	try:
		with transaction.atomic():
			store_obj = stkStoreMaster.objects.filter(storeid=store_id).delete()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Firm Deletion Failed.")

#get names from ids...
def storeUpdateParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	firm_id = request.GET.get('firm_id')
	understore_id = request.GET.get('understore_id')
	if understore_id == '0':
		dict_single_row['understore_name'] = 'INDEPENDENT STORE'
	else:
		store_obj = stkStoreMaster.objects.filter(storeid=understore_id)
		dict_single_row['understore_name'] = store_obj[0].mainstorename
	firm_obj = stkCompanyMaster.objects.filter(firmid=firm_id)
	dict_single_row['firm_name'] = firm_obj[0].firmname
	list_of_rows.append(dict_single_row.copy())
	response = JsonResponse(list_of_rows,safe=False)
	return HttpResponse(response.content)

#update mainstore...
def updateMainstore(request):
	store_id= request.GET.get('store_id')
	mainstore_name= request.GET.get('mainstore_name')
	understore_id= request.GET.get('understore_id')
	firm_id = request.GET.get('firm_id')
	print store_id+mainstore_name+understore_id+firm_id
	try:
		with transaction.atomic():
			firm_obj= stkStoreMaster.objects.filter(storeid=store_id).update(mainstorename=mainstore_name, underwhichstore=understore_id, firmid_id=firm_id)
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Mainstore Updation Failed.")


def test(request):
	dict_data={}
	data=[]
	col=("name","id")
	for i in (1,10):
		data.append(dict(zip(col,str(i))))
	response = JsonResponse(data,safe=False)
	return HttpResponse(response.content)


#load dept details [only those not already registered]...
def loadDeptInfo(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dept_obj = stkDept.objects.defer('deptid')
	deptid_list = [single_dept.deptid for single_dept in dept_obj]
	query = "select * from \"hrmDepartment\" where displayinstock=1"
	dept_data = dictFetchAll(cursorHelp(query))
	for dept in dept_data:
		if dept['did'] in deptid_list: #excepting already registered depts
			continue
		dict_single_row['did'] = dept['did']
		dict_single_row['department_name'] = dept['department']
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['hrmDepartment']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#load registered depts...
def loadRegisteredDeptInfo(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	query = "select * from \"hrmDepartment\" where did in (select deptid from \"stkDept\")"
	dept_data = dictFetchAll(cursorHelp(query))
	for dept in dept_data:
		dict_single_row['did'] = dept['did']
		dict_single_row['department_name'] = dept['department']
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['hrmDepartment']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#connect store to dept submitting...
def connectStoreDeptSubmit(request):
	dept_id= request.GET.get('dept_id')
	store_id= request.GET.get('store_id')
	try:
		with transaction.atomic():
			if stkDept.objects.filter(deptid=dept_id).exists() == True: #return if already inserted
				return HttpResponse("Department already connected.")
			dept_object = stkDept(deptid=dept_id, storeid_id=store_id)
			dept_object.save()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse(e.message)

#load data for connect store dept module table view...
def connectStoreDeptTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dept_objs = stkDept.objects.all()
	for single_dept in dept_objs:
		query = "select * from \"hrmDepartment\" where did="+str(single_dept.deptid)
		dept_data = dictFetchAll(cursorHelp(query))
		#print dept_data[0]['department']
		dict_single_row['dept_id'] = single_dept.deptid
		dict_single_row['department_name'] = dept_data[0]['department']
		store_objs = stkStoreMaster.objects.filter(storeid=single_dept.storeid_id)
		dict_single_row['store_id'] = single_dept.storeid_id
		dict_single_row['mainstore_name'] = store_objs[0].mainstorename
		used_dept_count = stkLocation.objects.filter(deptid_id=single_dept.deptid).count()
		if used_dept_count == 0:
			dict_single_row['editable'] = 'true'
		else:
			dict_single_row['editable'] = 'false'			
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkStoreDeptData']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#delete store dept connection...
def deleteStoreDeptConnection(request):
	dept_id = request.GET.get('dept_id')
	try:
		with transaction.atomic():
			dept_obj = stkDept.objects.filter(deptid=dept_id).delete()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Store - Dept Connection Deletion Failed.")

#get store name from store_id for row editing in connect store dept connect...
def storeDeptUpdateParams(request):
	store_id = request.GET.get('store_id')
	store_obj = stkStoreMaster.objects.filter(storeid=store_id).defer('mainstorename')
	return HttpResponse(store_obj[0].mainstorename)

#perform update of store and dept connection...
def updateStoreDeptConnection(request):
	dept_id = request.GET.get('dept_id')
	store_id = request.GET.get('store_id')
	try:
		with transaction.atomic():
			dept_obj = stkDept.objects.filter(deptid=dept_id).update(storeid_id=store_id)
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse(e.message)

#submit location...
def locationSubmit(request):
	try:
		with transaction.atomic():
			location_name = request.GET.get('location_name')
			dept_id = request.GET.get('dept_id')
			location_object = stkLocation(locationname=location_name, deptid_id=dept_id)
			location_object.save()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse(e.message)

#location table view...
def locationTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	all_locations = stkLocation.objects.all()
	for single_location in all_locations:
		dict_single_row['location_id'] = single_location.locationid
		dict_single_row['location_name'] = single_location.locationname
		dict_single_row['dept_id'] = single_location.deptid_id
		query = "select * from \"hrmDepartment\" where did="+str(single_location.deptid_id)
		dept_data = dictFetchAll(cursorHelp(query))
		dict_single_row['department_name'] = dept_data[0]['department']
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkLocation']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#update location and return location name corresponding to location id...
def updateLocation(request):
	location_id = request.GET.get('location_id')
	location_name = request.GET.get('location_name')
	dept_id = request.GET.get('dept_id')
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	try:
		with transaction.atomic():
			location_obj = stkLocation.objects.filter(locationid=location_id).update(locationname=location_name, deptid_id=dept_id)
			dict_single_row['status'] = 'success'
			query = "select * from \"hrmDepartment\" where did="+str(dept_id)
			dept_data = dictFetchAll(cursorHelp(query))
			dict_single_row['department_name'] = dept_data[0]['department']
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	except Exception as e:
		return HttpResponse(e.message)

#submit Unit...
#@csrf_protect
def unitSubmit(request):
	#if request.method == 'POST':
	try:
		with transaction.atomic():
			unit_name = request.GET.get('unit_name')
			no_of_contents = request.GET.get('no_of_contents')
			unit_object = stkUnits(unitname=unit_name, noofcontentsifany=no_of_contents)
			unit_object.save()
			print unit_name
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse(e.message)

#table view of unit registration...
def unitTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	all_units = stkUnits.objects.all()
	for single_unit in all_units:
		dict_single_row['unit_id'] = single_unit.unitid
		dict_single_row['unit_name'] = single_unit.unitname
		dict_single_row['no_of_contents'] = single_unit.noofcontentsifany
		'''#check whether editable...
		count_in_understore = stkStoreMaster.objects.filter(underwhichstore = single_mainstore.storeid).count()
		count_in_dept_table = stkDept.objects.filter(storeid_id=single_mainstore.storeid).count()
		if count_in_understore or count_in_dept_table > 0:
			dict_single_row['editable'] = 'false'
		else:
			dict_single_row['editable'] = 'true'  #can be edited'''
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkUnits']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#update unit...
def updateUnit(request):
	unit_id= request.GET.get('unit_id')
	unit_name= request.GET.get('unit_name')
	nos_contents= request.GET.get('nos_contents')
	try:
		with transaction.atomic():
			unit_obj= stkUnits.objects.filter(unitid=unit_id).update(unitname=unit_name, noofcontentsifany=nos_contents)
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse("Unit Updation Failed.")

#load main category informations...
def loadMaincatInfo(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	maincat_object = stkMainCategory.objects.all()
	for maincat in maincat_object:
		dict_single_row['maincatid'] = maincat.maincatid
		dict_single_row['maincatname'] = maincat.maincatname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkMainCategory']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

#submit subcategory...
def subCategorySubmit(request):
	try:
		with transaction.atomic():
			subcat_name = request.GET.get('subcat_name')
			maincat_id = request.GET.get('maincat_id')
			print subcat_name+maincat_id
			subcat_object = stkSubCategory(subcatname=subcat_name, maincatid_id=maincat_id)
			subcat_object.save()
			return HttpResponse("success")
	except Exception as e:
		return HttpResponse(e.message)

def subcatTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	subcat_object = stkSubCategory.objects.all()
	for subcat in subcat_object:
		dict_single_row['subcat_id'] = subcat.subcatid
		dict_single_row['subcat_name'] = subcat.subcatname
		maincat_obj = stkMainCategory.objects.filter(maincatid=subcat.maincatid_id)
		dict_single_row['maincat_id'] = maincat_obj[0].maincatid
		dict_single_row['maincat_name'] = maincat_obj[0].maincatname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkSubCategory']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

def updateSubcat(request):
	subcat_id = request.GET.get('subcat_id')
	subcat_name = request.GET.get('subcat_name')
	maincat_id = request.GET.get('maincat_id')
	print subcat_id+subcat_name+maincat_id
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	try:
		with transaction.atomic():
			subcat_obj = stkSubCategory.objects.filter(subcatid = subcat_id).update(subcatname= subcat_name, maincatid_id= maincat_id)
			dict_single_row['status'] = 'success'
			maincat_obj = stkMainCategory.objects.filter(maincatid= maincat_id)
			dict_single_row['maincat_name'] = maincat_obj[0].maincatname
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	except Exception as e:
		return HttpResponse(e.message)

#return values for loading selectboxes of item registration window...
def itemRegistrationParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	#get basic brand details...
	brand_object = stkBrandMaster.objects.all()
	for brand in brand_object:
		dict_single_row['brand_id'] = brand.brandid
		dict_single_row['brand_name'] = brand.brandname
		dict_single_row['brand_code'] = brand.brandcode
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkBrandMaster']=list_of_rows

	'''#get model details...
	list_of_rows=[]
	dict_single_row={}
	model_object = stkModelMaster.objects.defer('modelid','modelname')
	for model in model_object:
		dict_single_row['model_id'] = model.modelid
		dict_single_row['model_name'] = model.modelname
		dict_single_row['brand_id'] = model.brandid_id
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkModelMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)'''

	#get unit details...
	list_of_rows=[]
	dict_single_row={}
	unit_object = stkUnits.objects.defer('unitid','unitname')
	for unit in unit_object:
		dict_single_row['unit_id'] = unit.unitid
		dict_single_row['unit_name'] = unit.unitname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkUnits']=list_of_rows

	#get subcategory details...
	list_of_rows=[]
	dict_single_row={}
	subcat_object = stkSubCategory.objects.defer('subcatid','subcatname')
	for subcat in subcat_object:
		dict_single_row['subcat_id'] = subcat.subcatid
		dict_single_row['subcat_name'] = subcat.subcatname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkSubCategory']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)

	#get firm details...
	list_of_rows=[]
	dict_single_row={}
	firm_object = stkCompanyMaster.objects.all()
	for firm in firm_object:
		dict_single_row['firm_id'] = firm.firmid
		dict_single_row['firm_name'] = firm.firmname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkCompanyMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)

	#get mainstore details...
	list_of_rows=[]
	dict_single_row={}
	store_object = stkStoreMaster.objects.all()
	for store in store_object:
		dict_single_row['store_id'] = store.storeid
		dict_single_row['mainstore_name'] = store.mainstorename
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkStoreMaster']=list_of_rows

	#get maincategory (in item registration it is status) details...
	list_of_rows=[]
	dict_single_row={}
	maincat_object = stkMainCategory.objects.all()
	for maincat in maincat_object:
		dict_single_row['maincat_id'] = maincat.maincatid
		dict_single_row['maincat_name'] = maincat.maincatname
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkMainCategory']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

'''#load brands corresponding to maincatid
def brandsForMaincatId(request):
	dict_full_content={}
	list_of_rows=[]
	dict_single_row={}
	maincat_id = request.GET.get('maincat_id')
	subcat_obj = stkSubCategory.objects.defer('subcatid').filter(maincatid_id=maincat_id)
	for subcat in subcat_obj:
		model_obj = stkModelMaster.objects.defer('brandid_id').filter(subcatid_id=subcat.subcatid).distinct('brandid_id') #all models of a purticular brand [distinct based on brand field. ie multiple models with same brand]
		for model in model_obj:
			brand_object = stkBrandMaster.objects.filter(brandid=model.brandid_id)
			for brand in brand_object:
				dict_single_row['brand_id'] = brand.brandid
				dict_single_row['brand_name'] = brand.brandname
				dict_single_row['brand_code'] = brand.brandcode
				list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkBrandMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)'''

def brandsForMaincatId(request):
	dict_full_content={}
	list_of_rows=[]
	dict_single_row={}
	maincat_id = request.GET.get('maincat_id')
	item_object = stkItemMaster.objects.filter(maincatid_id=maincat_id).select_related().distinct('brandid_id')
	for item in item_object:
		dict_single_row['brand_id'] = item.brandid_id
		dict_single_row['brand_name'] = item.brandid.brandname
		dict_single_row['brand_code'] = item.brandid.brandcode
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkBrandMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)		

#load model names corresponding to selected brand...
def itemModelForBrand(request):
	dict_full_content={}
	list_of_rows=[]
	dict_single_row={}
	brand_id = request.GET.get('brand_id')
	model_object = stkModelMaster.objects.filter(brandid_id=brand_id)
	for model in model_object:
		dict_single_row['model_id'] = model.modelid
		dict_single_row['model_name'] = model.modelname
		dict_single_row['brand_id'] = model.brandid_id
		'''dict_single_row['product_info'] = model.productinfo
		dict_single_row['specification'] = model.specification
		dict_single_row['remarks'] = model.remarks
		dict_single_row['subcat_id'] = model.subcatid_id
		dict_single_row['unit_id'] = model.unitid_id'''
		list_of_rows.append(dict_single_row.copy())
	dict_full_content['stkModelMaster']=list_of_rows
	response = JsonResponse(dict_full_content,safe=False)
	return HttpResponse(response.content)

def itemSubmit(request):
	list_of_rows=[]
	dict_single_row={}
	brand_name = request.GET.get('brand_name')
	model_name = request.GET.get('model_name')
	brand_code = request.GET.get('brand_code')
	model_code = request.GET.get('model_code')
	product_info = request.GET.get('product_info')
	remark = request.GET.get('remark')
	spec = request.GET.get('specification')
	is_subitem = request.GET.get('is_subitem')
	qty_available = request.GET.get('qty_available') #in this module this qty_available means existing qty
	no_of_contents = request.GET.get('no_of_contents')
	unit_id = request.GET.get('unit_id')
	subcat_id = request.GET.get('subcat_id')
	#firm_id = request.GET.get('firm_id')
	#store_id = request.GET.get('store_id')
	maincat_id = request.GET.get('maincat_id')#it is the status indicate consummable/asset
	temp_brandid = None;
	try:
		with transaction.atomic():
			if stkBrandMaster.objects.filter(brandname=brand_name).exists() == False: #brand name not already existing so insert it.
				print "not exist"
				brand_obj= stkBrandMaster(brandname=brand_name,brandcode=brand_code)
				brand_obj.save()
				temp_brandid = brand_obj.brandid #storing brandid temporarily
				print "brand insert"
			else:
				print "exist"
				brand_obj = stkBrandMaster.objects.filter(brandname=brand_name)
				temp_brandid = brand_obj[0].brandid 
				print brand_obj[0].brandid
			model_obj = stkModelMaster(modelname=model_name, specification=spec, productinfo=product_info, remarks=remark, qtyavailable=0, modelcode=model_code, unitid_id=unit_id, subcatid_id=subcat_id, brandid_id=temp_brandid)
			model_obj.save()
			print "model insert"
			if is_subitem == "true":
				subitem = 'Y'
			else:
				subitem = 'N'
			print subitem
			item_obj = stkItemMaster(qtyavailable=0, existingqty=qty_available, totalnoofcontents=no_of_contents, whethersubitem=subitem, maincatid_id=maincat_id, brandid_id=temp_brandid, modelid_id=model_obj.modelid, unitid_id=unit_id, subcatid_id=subcat_id, firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'],itemcode=model_code)
			item_obj.save()

			dict_single_row['status'] = "success"

			item_master_object = stkItemMaster.objects.filter(itemid=item_obj.itemid).select_related() #join stkItemMaster and other foreign key associated tables
			for item in item_master_object:
				dict_single_row['item_id'] = item.itemid
				dict_single_row['qty_available'] = item.existingqty #old item.qtyavailable
				dict_single_row['no_of_contents'] = item.totalnoofcontents
				dict_single_row['whether_subitem'] = item.whethersubitem
				dict_single_row['unit_id'] = item_obj.unitid_id
				dict_single_row['unit_name'] = item.unitid.unitname #field of stkUnits table addressed with its primary key unitid
				dict_single_row['subcat_id'] = item.subcatid_id
				dict_single_row['subcat_name'] = item.subcatid.subcatname
				dict_single_row['firm_id'] = item.firmid_id
				dict_single_row['firm_name'] = item.firmid.firmname
				dict_single_row['maincat_id'] = item.maincatid_id
				dict_single_row['maincat_name'] = item.maincatid.maincatname
				dict_single_row['store_id'] = item.storeid_id
				dict_single_row['mainstore_name'] = item.storeid.mainstorename
				#model details...
				dict_single_row['model_id'] = item.modelid_id
				dict_single_row['model_name'] = item.modelid.modelname
				dict_single_row['model_code'] = item.modelid.modelcode
				dict_single_row['specification'] = item.modelid.specification
				dict_single_row['product_info'] = item.modelid.productinfo
				dict_single_row['remarks'] = item.modelid.remarks
				#brand details...
				dict_single_row['brand_id'] = item.brandid_id
				dict_single_row['brand_name'] = item.brandid.brandname
				dict_single_row['brand_code'] = item.brandid.brandcode
				list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	except Exception as e:
		return HttpResponse(e.message)

@csrf_protect
def itemTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		#join itemMaster table backwards...
		item_master_object = stkItemMaster.objects.select_related() #join stkItemMaster and other foreign key associated tables
		for item in item_master_object:
			#if not the selected firm or store
			if (item.firmid_id != request.session['session_firmid']) and (item.storeid_id != request.session['selected_store_id']):
				continue
			dict_single_row['item_id'] = item.itemid
			dict_single_row['qty_available'] = item.existingqty #old item.qtyavailable
			dict_single_row['no_of_contents'] = item.totalnoofcontents
			dict_single_row['whether_subitem'] = item.whethersubitem
			dict_single_row['unit_id'] = item.unitid_id
			dict_single_row['unit_name'] = item.unitid.unitname #field of stkUnits table addressed with its primary key unitid
			dict_single_row['subcat_id'] = item.subcatid_id
			dict_single_row['subcat_name'] = item.subcatid.subcatname
			dict_single_row['firm_id'] = item.firmid_id
			dict_single_row['firm_name'] = item.firmid.firmname
			dict_single_row['maincat_id'] = item.maincatid_id
			dict_single_row['maincat_name'] = item.maincatid.maincatname
			dict_single_row['store_id'] = item.storeid_id
			dict_single_row['mainstore_name'] = item.storeid.mainstorename
			#model details...
			dict_single_row['model_id'] = item.modelid_id
			dict_single_row['model_name'] = item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			dict_single_row['specification'] = item.modelid.specification
			dict_single_row['product_info'] = item.modelid.productinfo
			dict_single_row['remarks'] = item.modelid.remarks
			#brand details...
			dict_single_row['brand_id'] = item.brandid_id
			dict_single_row['brand_name'] = item.brandid.brandname
			dict_single_row['brand_code'] = item.brandid.brandcode
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only available with post request.")

@csrf_protect
def itemUpdate(request): #not implemented post..
		brand_name = request.GET.get('brand_name')
		model_name = request.GET.get('model_name')
		brand_code = request.GET.get('brand_code')
		model_code = request.GET.get('model_code')
		product_info = request.GET.get('product_info')
		remark = request.GET.get('remark')
		spec = request.GET.get('specification')
		is_subitem = request.GET.get('is_subitem')
		qty_available = request.GET.get('qty_available') #it is existing quantity
		no_of_contents = request.GET.get('no_of_contents')
		unit_id = request.GET.get('unit_id')
		subcat_id = request.GET.get('subcat_id')
		maincat_id = request.GET.get('maincat_id')
		brand_id = request.GET.get('brand_id')
		model_id = request.GET.get('model_id')
		item_id = request.GET.get('item_id')
		#print brand_id + model_id + item_id
		#print brand_name+model_name+brand_code+model_code+product_info+remark+spec+is_subitem+qty_available+no_of_contents
		try:
			with transaction.atomic():
				if is_subitem == "true":
					subitem = 'Y'
				else:
					subitem = 'N'
				itemdetailscount = stkItemDetails.objects.filter(itemid_id=item_id,existing="Y").count()
				if int(qty_available) < int(itemdetailscount): #already more items are registered these cannot be deleted here.
					return HttpResponse("counterror")
				brand_obj= stkBrandMaster.objects.filter(brandid=brand_id).update(brandname=brand_name,brandcode=brand_code)
				model_obj = stkModelMaster.objects.filter(modelid=model_id).update(modelname=model_name, specification=spec, productinfo=product_info, remarks=remark, modelcode=model_code, unitid_id=unit_id, subcatid_id=subcat_id, brandid_id=brand_id)#qtyavailable=0, 
				item_obj = stkItemMaster.objects.filter(itemid=item_id).update(existingqty=qty_available, totalnoofcontents=no_of_contents, whethersubitem=subitem, maincatid_id=maincat_id, brandid_id=brand_id, modelid_id=model_id, unitid_id=unit_id, subcatid_id=subcat_id, itemcode=model_code)#qtyavailable=0,
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse(e.message)

@csrf_protect
def itemDelete(request):
	if request.method == 'POST':
		item_id = request.GET.get('item_id')
		model_id = request.GET.get('model_id')
		try:
			with transaction.atomic():
				item_obj = stkItemMaster.objects.filter(itemid=item_id).delete()
				model_obj = stkModelMaster.objects.filter(modelid=model_id).delete()
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse(e.message)

@csrf_protect
def supplierSubmit(request):
	list_of_rows=[]
	dict_single_row={}
	if request.method == 'POST':
		params = json.loads(request.body)
		supplier_name = params['supplier_name']
		address = params['address']
		city = params['city'].capitalize()
		district = params['district'].upper()
		state = params['state'].upper()
		country = params['country'].upper()
		mail_id = params['mail_id']
		phone = params['phone']
		vat_no = params['vat_no']
		#print request.body
		#print supplier_name,address,city,district,state,country,mail_id,phone,vat_no
		try:
			with transaction.atomic():
				supplier_obj = stkSupplier(suppliername=supplier_name, address=address, city=city, district=district, country=country, state=state, mailid=mail_id, mobileorlandline=phone, vatno=vat_no)
				supplier_obj.save()
				dict_single_row['status'] = "success"
				dict_single_row['supplier_id'] = supplier_obj.supplierid
				dict_single_row['supplier_name'] = supplier_obj.suppliername
				dict_single_row['address'] = supplier_obj.address
				dict_single_row['city'] = supplier_obj.city
				dict_single_row['district'] = supplier_obj.district
				dict_single_row['country'] = supplier_obj.country
				dict_single_row['state'] = supplier_obj.state
				dict_single_row['mailid'] = supplier_obj.mailid
				dict_single_row['mobileorlandline'] = supplier_obj.mobileorlandline
				dict_single_row['vatno'] = supplier_obj.vatno
				dict_single_row['rating'] = supplier_obj.rating
				list_of_rows.append(dict_single_row.copy())
				response = JsonResponse(list_of_rows,safe=False)
				return HttpResponse(response.content)
		except Exception as e:
			dict_single_row['status'] = "failed"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def supplierTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		supplier_obj = stkSupplier.objects.all()
		for supplier in supplier_obj:
			dict_single_row['supplier_id'] = supplier.supplierid
			dict_single_row['supplier_name'] = supplier.suppliername
			dict_single_row['address'] = supplier.address
			dict_single_row['city'] = supplier.city
			dict_single_row['district'] = supplier.district
			dict_single_row['country'] = supplier.country
			dict_single_row['state'] = supplier.state
			dict_single_row['mailid'] = supplier.mailid
			dict_single_row['mobileorlandline'] = supplier.mobileorlandline
			dict_single_row['vatno'] = supplier.vatno
			dict_single_row['rating'] = supplier.rating
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSupplier']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def supplierUpdate(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		supplier_id = params['supplier_id']
		supplier_name = params['supplier_name']
		address = params['address']
		city = params['city'].capitalize()
		district = params['district'].upper()
		state = params['state'].upper()
		country = params['country'].upper()
		mail_id = params['mail_id']
		phone = params['phone']
		vat_no = params['vat_no']
		#print request.body
		print supplier_id,supplier_name,address,city,district,state,country,mail_id,phone,vat_no
		supplier_obj = stkSupplier.objects.filter(supplierid=supplier_id).update(suppliername=supplier_name, address=address, city=city, district=district, country=country, state=state, mailid=mail_id, mobileorlandline=phone, vatno=vat_no)
		return HttpResponse("success")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def supplierDelete(request):
	if request.method == 'POST':
		try:
			with transaction.atomic():
				params = json.loads(request.body)
				supplier_id = params['supplier_id']
				supplier_obj = stkSupplier.objects.filter(supplierid=supplier_id).delete()
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse("can't be deleted.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def supplierParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		supplier_obj = stkSupplier.objects.defer('state').distinct('state')
		for supplier in supplier_obj:
			dict_single_row['state'] = supplier.state
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['supplierStates']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		supplier_obj = stkSupplier.objects.defer('country').distinct('country')
		for supplier in supplier_obj:
			dict_single_row['country'] = supplier.country
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['supplierCountries']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		supplier_obj = stkSupplier.objects.defer('city').distinct('city')
		for supplier in supplier_obj:
			dict_single_row['city'] = supplier.city
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['supplierCities']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		supplier_obj = stkSupplier.objects.defer('district').distinct('district')
		for supplier in supplier_obj:
			dict_single_row['district'] = supplier.district
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['supplierDistricts']=list_of_rows


		response = JsonResponse(dict_full_content,safe=False)
		#print response.content
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		maincat_obj = stkMainCategory.objects.all()
		for maincat in maincat_obj:
			dict_single_row['maincat_id'] = maincat.maincatid
			dict_single_row['maincat_name'] = maincat.maincatname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkMainCategory']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		item_obj = stkItemMaster.objects.all().select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		supplier_obj = stkSupplier.objects.all()
		for supplier in supplier_obj:
			dict_single_row['supplier_id'] = supplier.supplierid
			dict_single_row['supplier_name'] = supplier.suppliername
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSupplier']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		unit_obj = stkUnits.objects.all()
		for unit in unit_obj:
			dict_single_row['unit_id'] = unit.unitid
			dict_single_row['unit_name'] = unit.unitname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkUnits']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		#print response.content
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#function generate fisatid for items...
def generateFisatId(quantity):
	subcat_obj = stkSubCategory.objects.defer('lastvalue').filter(subcatid=1)
	new_lastvalue = subcat_obj[0].lastvalue + int(quantity)
	subcat_obj = stkSubCategory.objects.filter(subcatid=1).update(lastvalue=new_lastvalue)
	return "FIT"+str(new_lastvalue)

@csrf_protect
def purchaseSubmit(request):
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		invoice_no = params['invoice_no']
		invoice_date = params['invoice_date']
		purchase_date = params['purchase_date']
		total_price = params['total_price']
		total_tax = params['total_tax']
		net_amount = params['net_amount']
		total_discount = params['total_discount']
		#entered_date = params['entered_date']
		supplier_id = params['supplier_id']
		json_details = json.loads(params['jsonDetails'])
		try:
			with transaction.atomic():
				purchasemaster_obj = stkPurchaseMaster(totprice=total_price, tottax=total_tax, netamount=net_amount, totdiscount=total_discount, invoiceno=invoice_no, invoicedate=invoice_date, purchasedate=purchase_date, enteredbyid=request.session['session_empid'], entereddate=datetime.now().date(), supplierid_id=supplier_id)
				purchasemaster_obj.save()
				dict_single_subrow={} #reinitialize
				list_of_subrows=[]
				for detail in json_details:
					purchaseinfo_obj = stkPurchaseInfo(description=detail['description'], quantity=detail['quantity'], unitprice=detail['unit_price'], individualdiscount=detail['individual_discount'], individualtaxpercentage=detail['individual_tax_percentage'], individualtaxamount=detail['individual_tax_amount'], stkregtrpageno=detail['stk_regtr_pageno'], purchaseid_id=purchasemaster_obj.purchaseid, unitid_id=detail['unit_id'], itemid_id=detail['item_id'], maincatid_id=detail['maincat_id'])
					purchaseinfo_obj.save()
					#insert to stkItemDetails [generate quantity number of items]...
					for i in range(0, int(detail['quantity'])): #[i=0;i<(qty+1);i++]
						itemdetails_obj = stkItemDetails(fisatid=generateFisatId(1), itemid_id=detail['item_id'], purchaseid_id=purchasemaster_obj.purchaseid, firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'])
						itemdetails_obj.save()
						warranty_obj = stkWarrantyOrAmc(warrantyfrom=invoice_date,warrantyto=detail['warranty_todate'],itemdetailsid_id=itemdetails_obj.itemdetailsid) #woramc is default 'W'
						warranty_obj.save()
						stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetails_obj.itemdetailsid).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);
					#update qty available in stkItemMaster and in stkModelMaster
					itemmaster_obj = stkItemMaster.objects.defer('qtyavailable','modelid_id').filter(itemid=detail['item_id'])
					new_qty = itemmaster_obj[0].qtyavailable + detail['quantity']
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					#data to fill purchase table view...
					dict_single_subrow['recordid'] = purchaseinfo_obj.recordid
					dict_single_subrow['description'] = purchaseinfo_obj.description
					dict_single_subrow['quantity'] = purchaseinfo_obj.quantity
					dict_single_subrow['unitprice'] = purchaseinfo_obj.unitprice
					dict_single_subrow['individualdiscount'] = purchaseinfo_obj.individualdiscount
					dict_single_subrow['individualtaxpercentage'] = purchaseinfo_obj.individualtaxpercentage
					dict_single_subrow['individualtaxamount'] = purchaseinfo_obj.individualtaxamount
					dict_single_subrow['stkregtrpageno'] = purchaseinfo_obj.stkregtrpageno
					dict_single_subrow['purchaseid'] = purchaseinfo_obj.purchaseid_id
					dict_single_subrow['unitid'] = purchaseinfo_obj.unitid_id
					unit_obj=stkUnits.objects.defer('unitname').filter(unitid=purchaseinfo_obj.unitid_id)
					dict_single_subrow['unitname'] = unit_obj[0].unitname
					dict_single_subrow['itemid'] = purchaseinfo_obj.itemid_id
					item_obj = stkItemMaster.objects.filter(itemid=purchaseinfo_obj.itemid_id).select_related()
					dict_single_subrow['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname
					dict_single_subrow['maincatid'] = purchaseinfo_obj.maincatid_id
					maincat_obj=stkMainCategory.objects.filter(maincatid=purchaseinfo_obj.maincatid_id)
					dict_single_subrow['maincatname'] = maincat_obj[0].maincatname
					item_total = (purchaseinfo_obj.quantity * purchaseinfo_obj.unitprice) - purchaseinfo_obj.individualdiscount + purchaseinfo_obj.individualtaxamount
					dict_single_subrow['itemtotal'] = item_total
					#dict_single_subrow['supplier_name'] = purchase.supplierid.suppliername
					#warranty information...
					itemdetails_obj = stkItemDetails.objects.filter(itemid_id=purchaseinfo_obj.itemid_id, purchaseid_id=purchaseinfo_obj.purchaseid_id)
					if itemdetails_obj[0].warrantyoramcid_id == None:
						#dict_single_subrow['warrantyoramcid'] = ""
						dict_single_subrow['warrantytodate'] = ""
					else:
						#dict_single_subrow['warrantyoramcid'] = itemdetails_obj[0].warrantyoramcid_id
						warranty_obj = stkWarrantyOrAmc.objects.defer('warrantyoramcid','warrantyto').filter(warrantyoramcid=itemdetails_obj[0].warrantyoramcid_id)
						dict_single_subrow['warrantytodate'] = warranty_obj[0].warrantyto
					list_of_subrows.append(dict_single_subrow.copy())
				dict_single_row['purchaseInfo'] = list_of_subrows			

				dict_single_row['status'] = "success"
				#data to fill purchase table view...
				dict_single_row['purchaseid'] = purchasemaster_obj.purchaseid
				dict_single_row['totprice'] = total_price
				dict_single_row['tottax'] = total_tax
				dict_single_row['netamount'] = net_amount
				dict_single_row['totdiscount'] = total_discount
				dict_single_row['invoiceno'] = invoice_no
				dict_single_row['invoicedate'] = invoice_date
				dict_single_row['purchasedate'] = purchase_date
				dict_single_row['supplierid'] = supplier_id
				supplier_obj=stkSupplier.objects.defer('suppliername').filter(supplierid=supplier_id)
				dict_single_row['suppliername'] = supplier_obj[0].suppliername
				list_of_rows.append(dict_single_row.copy())
				response = JsonResponse(list_of_rows,safe=False)
				return HttpResponse(response.content)

		except ObjectDoesNotExist:#Exception as e
			dict_single_row['status'] = "failed"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method == 'POST':
		purchasemaster_obj = stkPurchaseMaster.objects.all().select_related()
		for purchase in purchasemaster_obj:
			dict_single_row['purchaseid'] = purchase.purchaseid
			dict_single_row['totprice'] = purchase.totprice
			dict_single_row['tottax'] = purchase.tottax
			dict_single_row['netamount'] = purchase.netamount
			dict_single_row['totdiscount'] = purchase.totdiscount
			dict_single_row['invoiceno'] = purchase.invoiceno
			dict_single_row['invoicedate'] = purchase.invoicedate
			dict_single_row['purchasedate'] = purchase.purchasedate
			dict_single_row['supplierid'] = purchase.supplierid_id
			dict_single_row['suppliername'] = purchase.supplierid.suppliername
			dict_single_row['status'] = "nil"
			#json format of stkPurchaseInfo part
			purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchase.purchaseid).select_related()
			dict_single_subrow={} #reinitialize
			list_of_subrows=[]
			for info in purchaseinfo_obj:
				dict_single_subrow['recordid'] = info.recordid
				dict_single_subrow['description'] = info.description
				dict_single_subrow['quantity'] = info.quantity
				dict_single_subrow['unitprice'] = info.unitprice
				dict_single_subrow['individualdiscount'] = info.individualdiscount
				dict_single_subrow['individualtaxpercentage'] = info.individualtaxpercentage
				dict_single_subrow['individualtaxamount'] = info.individualtaxamount
				dict_single_subrow['stkregtrpageno'] = info.stkregtrpageno
				#dict_single_subrow['purchasereturnstatus'] = info.purchasereturnstatus
				#dict_single_subrow['purchasereturnid'] = info.purchasereturnid_id
				dict_single_subrow['purchaseid'] = info.purchaseid_id
				dict_single_subrow['unitid'] = info.unitid_id
				dict_single_subrow['unitname'] = info.unitid.unitname
				dict_single_subrow['itemid'] = info.itemid_id
				item_obj = stkItemMaster.objects.filter(itemid=info.itemid_id).select_related()
				dict_single_subrow['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname
				dict_single_subrow['maincatid'] = info.maincatid_id
				dict_single_subrow['maincatname'] = info.maincatid.maincatname
				item_total = (info.quantity * info.unitprice) - info.individualdiscount + info.individualtaxamount
				dict_single_subrow['itemtotal'] = item_total
				#dict_single_subrow['supplier_name'] = purchase.supplierid.suppliername
				#warranty information...
				itemdetails_obj = stkItemDetails.objects.filter(itemid_id=info.itemid_id, purchaseid_id=info.purchaseid_id)
				if itemdetails_obj[0].warrantyoramcid_id == None:
					#dict_single_subrow['warrantyoramcid'] = ""
					dict_single_subrow['warrantytodate'] = ""
				else:
					#dict_single_subrow['warrantyoramcid'] = itemdetails_obj[0].warrantyoramcid_id
					warranty_obj = stkWarrantyOrAmc.objects.defer('warrantyoramcid','warrantyto').filter(warrantyoramcid=itemdetails_obj[0].warrantyoramcid_id)
					dict_single_subrow['warrantytodate'] = warranty_obj[0].warrantyto
				list_of_subrows.append(dict_single_subrow.copy())
			dict_single_row['purchaseInfo'] = list_of_subrows			
			list_of_rows.append(dict_single_row.copy())

		dict_full_content['stkPurchaseMaster']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		#print response.content
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseUpdate(request):
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		print request.body
		purchase_id = params['purchase_id']
		invoice_no = params['invoice_no']
		invoice_date = params['invoice_date']
		purchase_date = params['purchase_date']
		total_price = params['total_price']
		total_tax = params['total_tax']
		net_amount = params['net_amount']
		total_discount = params['total_discount']
		#entered_date = params['entered_date']
		supplier_id = params['supplier_id']
		json_details = json.loads(params['jsonDetails'])
		try:
			with transaction.atomic():
				purchasemaster_obj = stkPurchaseMaster.objects.filter(purchaseid=purchase_id).update(totprice=total_price, tottax=total_tax, netamount=net_amount, totdiscount=total_discount, invoiceno=invoice_no, invoicedate=invoice_date, purchasedate=purchase_date,  supplierid_id=supplier_id)
				purchasemaster_obj = stkPurchaseMaster.objects.filter(purchaseid=purchase_id)
				dict_single_subrow={} #reinitialize
				list_of_subrows=[]

				'''
				for detail in json_details:
					#here detail id is the recordid...
					purchaseinfo_obj = stkPurchaseInfo.objects.filter(recordid=detail['detail_id']) #here detail_id is record_id of purchaseInfo
					old_qty_of_item = purchaseinfo_obj[0].quantity
					purchaseinfo_obj = stkPurchaseInfo.objects.filter(recordid=detail['detail_id']).update(description=detail['description'], quantity=detail['quantity'], unitprice=detail['unit_price'], individualdiscount=detail['individual_discount'], individualtaxpercentage=detail['individual_tax_percentage'], individualtaxamount=detail['individual_tax_amount'], stkregtrpageno=detail['stk_regtr_pageno'], unitid_id=detail['unit_id'], itemid_id=detail['item_id'], maincatid_id=detail['maincat_id'])
					purchaseinfo_obj = stkPurchaseInfo.objects.filter(recordid=detail['detail_id'])
					
					#######################how to remove items when qty is modified###############################################
					#update qty information;generate extra if qty is more;remove items if qty is less;
					itemmaster_obj = stkItemMaster.objects.defer('qtyavailable','modelid_id').filter(itemid=detail['item_id'])
					qty_difference = detail['quantity'] - old_qty_of_item #if +ve then generate if -ve then delete, 0 no change
					if qty_difference == 0:
						print "no change"
					elif qty_difference > 0: #then generate the extra ones...
						print "greater then generated"
						for i in range(0, qty_difference): #[i=0;i<(qty_difference);i++]
							itemdetails_obj = stkItemDetails(fisatid=generateFisatId(1), itemid_id=detail['item_id'], purchaseid_id=purchasemaster_obj[0].purchaseid, firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'])
							itemdetails_obj.save()
						print i
						new_qty = itemmaster_obj[0].qtyavailable + qty_difference
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					else:
						print "lesser then remove"
						itemdetails_obj = stkItemDetails.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid)
						for i in range(0, abs(qty_difference)): #[i=0;i<(qty_difference);i++]
							itemdetails_obj[i].delete()
						new_qty = itemmaster_obj[0].qtyavailable - abs(qty_difference)
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					'''
				
				#first delete all purchase infos then insert new...
				purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid=purchase_id)
				for info in purchaseinfo_obj:
					itemmaster_obj = stkItemMaster.objects.filter(itemid=info.itemid_id)
					new_qty = itemmaster_obj[0].qtyavailable - info.quantity
					itemmaster_obj.update(qtyavailable=new_qty)
					stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				itemdetails_obj = stkItemDetails.objects.filter(purchaseid=purchase_id).delete() #warranty info automatically deleted
				purchaseinfo_obj.delete()

				#then insert new values...
				for detail in json_details:
					purchaseinfo_obj = stkPurchaseInfo(description=detail['description'], quantity=detail['quantity'], unitprice=detail['unit_price'], individualdiscount=detail['individual_discount'], individualtaxpercentage=detail['individual_tax_percentage'], individualtaxamount=detail['individual_tax_amount'], stkregtrpageno=detail['stk_regtr_pageno'], purchaseid_id=purchase_id, unitid_id=detail['unit_id'], itemid_id=detail['item_id'], maincatid_id=detail['maincat_id'])
					purchaseinfo_obj.save()
					#insert to stkItemDetails [generate quantity number of items]...
					for i in range(0, int(detail['quantity'])): #[i=0;i<(qty+1);i++]
						itemdetails_obj = stkItemDetails(fisatid=generateFisatId(1), itemid_id=detail['item_id'], purchaseid_id=purchase_id, firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'])
						itemdetails_obj.save()
						#warranty_obj = stkWarrantyOrAmc(warrantyfrom=invoice_date,warrantyto=detail['warranty_todate'],itemdetailsid_id=itemdetails_obj.itemdetailsid) #woramc is default 'W'
						#warranty_obj.save()
						#stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetails_obj.itemdetailsid).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);
					#update qty available in stkItemMaster and in stkModelMaster
					itemmaster_obj = stkItemMaster.objects.defer('qtyavailable','modelid_id').filter(itemid=detail['item_id'])
					new_qty = itemmaster_obj[0].qtyavailable + detail['quantity']
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)

					#update warranty information...
					itemdetails_obj = stkItemDetails.objects.filter(itemid_id=detail['item_id'], purchaseid_id=purchase_id)
					for itemdetail in itemdetails_obj:
						print "it detid: "+str(itemdetail.itemdetailsid)
						if itemdetail.warrantyoramcid_id != None: #already in database [in itemdetails table]
							if detail['warranty_todate'] != "": #also in params list [so update]
								stkWarrantyOrAmc.objects.filter(itemdetailsid_id=itemdetail.itemdetailsid).update(warrantyto=detail['warranty_todate'])
								print "updated"
							else: #currently have a warrenty in database but not in the params so delete warranty entry...
								stkItemDetails.objects.filter(itemdetailsid=itemdetail.itemdetailsid).update(warrantyoramcid="")
								warranty_obj = stkWarrantyOrAmc.objects.filter(itemdetailsid_id=itemdetail.itemdetailsid).delete()
						else: #not already in database [in itemdetails table]
							if detail['warranty_todate'] != "": #also present in params list
								warranty_obj = stkWarrantyOrAmc(warrantyfrom=invoice_date,warrantyto=detail['warranty_todate'],itemdetailsid_id=itemdetail.itemdetailsid) #woramc is default 'W'
								warranty_obj.save()
								stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetail.itemdetailsid).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);
								print "created"

					#data to fill purchase table view(fill purchaseInfo)...
					purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchase_id).select_related()
					itemdetails_obj = stkItemDetails.objects.filter(itemid_id=detail['item_id'], purchaseid_id=purchase_id)
					if itemdetails_obj[0].warrantyoramcid_id == None:
						#dict_single_subrow['warrantyoramcid'] = ""
						dict_single_subrow['warrantytodate'] = ""
					else:
						#dict_single_subrow['warrantyoramcid'] = itemdetails_obj[0].warrantyoramcid_id
						warranty_obj = stkWarrantyOrAmc.objects.defer('warrantyoramcid','warrantyto').filter(warrantyoramcid=itemdetails_obj[0].warrantyoramcid_id)
						dict_single_subrow['warrantytodate'] = warranty_obj[0].warrantyto
					dict_single_subrow['recordid'] = 1#purchaseinfo_obj[0].recordid not required
					dict_single_subrow['description'] = purchaseinfo_obj[0].description
					dict_single_subrow['quantity'] = purchaseinfo_obj[0].quantity
					dict_single_subrow['unitprice'] = purchaseinfo_obj[0].unitprice
					dict_single_subrow['individualdiscount'] = purchaseinfo_obj[0].individualdiscount
					dict_single_subrow['individualtaxpercentage'] = purchaseinfo_obj[0].individualtaxpercentage
					dict_single_subrow['individualtaxamount'] = purchaseinfo_obj[0].individualtaxamount
					dict_single_subrow['stkregtrpageno'] = purchaseinfo_obj[0].stkregtrpageno
					dict_single_subrow['purchaseid'] = purchaseinfo_obj[0].purchaseid_id
					dict_single_subrow['unitid'] = purchaseinfo_obj[0].unitid_id
					unit_obj=stkUnits.objects.defer('unitname').filter(unitid=purchaseinfo_obj[0].unitid_id)
					dict_single_subrow['unitname'] = unit_obj[0].unitname
					dict_single_subrow['itemid'] = purchaseinfo_obj[0].itemid_id
					item_obj = stkItemMaster.objects.filter(itemid=purchaseinfo_obj[0].itemid_id).select_related()
					dict_single_subrow['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname
					dict_single_subrow['maincatid'] = purchaseinfo_obj[0].maincatid_id
					maincat_obj=stkMainCategory.objects.filter(maincatid=purchaseinfo_obj[0].maincatid_id)
					dict_single_subrow['maincatname'] = maincat_obj[0].maincatname
					item_total = (purchaseinfo_obj[0].quantity * purchaseinfo_obj[0].unitprice) - purchaseinfo_obj[0].individualdiscount + purchaseinfo_obj[0].individualtaxamount
					dict_single_subrow['itemtotal'] = item_total
					#dict_single_subrow['supplier_name'] = purchase.supplierid.suppliername
					list_of_subrows.append(dict_single_subrow.copy())
				dict_single_row['purchaseInfo'] = list_of_subrows			

				dict_single_row['status'] = "success"
				#data to fill purchase table view(fill purchaseMaster data)...
				dict_single_row['purchaseid'] = purchasemaster_obj[0].purchaseid
				dict_single_row['totprice'] = total_price
				dict_single_row['tottax'] = total_tax
				dict_single_row['netamount'] = net_amount
				dict_single_row['totdiscount'] = total_discount
				dict_single_row['invoiceno'] = invoice_no
				dict_single_row['invoicedate'] = invoice_date
				dict_single_row['purchasedate'] = purchase_date
				dict_single_row['supplierid'] = supplier_id
				supplier_obj=stkSupplier.objects.defer('suppliername').filter(supplierid=supplier_id)
				dict_single_row['suppliername'] = supplier_obj[0].suppliername
				list_of_rows.append(dict_single_row.copy())
				response = JsonResponse(list_of_rows,safe=False)
				return HttpResponse(response.content)

		except ObjectDoesNotExist:#Exception as e
			dict_single_row['status'] = "failed"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseDelete(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		purchase_id = params['purchase_id']
		try:
			with transaction.atomic():
				purchasereturn_obj = stkPurchaseReturn.objects.filter(purchaseid_id=purchase_id).exists()
				if purchasereturn_obj:
					return HttpResponse("depent") #have dependent entries, so cannot be deleted.
				itemdetails_obj=stkItemDetails.objects.filter(purchaseid_id=purchase_id, issuedornot='Y').exists()
				if itemdetails_obj:
					return HttpResponse("depent") #have dependent entries, so cannot be deleted.
				itemdetails_obj=stkItemDetails.objects.filter(purchaseid_id=purchase_id)
				affected_no_of_items_count=itemdetails_obj.count()
				itemdetails_obj.delete()
				print "item details deleted:"+str(affected_no_of_items_count)
				purchaseinfo_obj=stkPurchaseInfo.objects.filter(purchaseid_id=purchase_id)
				item_id=purchaseinfo_obj[0].itemid_id
				purchaseinfo_obj.delete()
				print("info deleted")
				purchasemaster_obj=stkPurchaseMaster.objects.filter(purchaseid=purchase_id).delete()
				print "master deleted"
				#update(reduce) qty...
				itemmaster_obj = stkItemMaster.objects.defer('qtyavailable','modelid_id').filter(itemid=item_id)
				new_qty = itemmaster_obj[0].qtyavailable - affected_no_of_items_count
				itemmaster_obj.update(qtyavailable=new_qty)
				modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				print "qty updated"
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Delete Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def issueParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		dept_obj = stkDept.objects.defer('deptid')
		deptid_list = [single_dept.deptid for single_dept in dept_obj]
		query = "select * from \"hrmDepartment\" where displayinstock=1"
		dept_data = dictFetchAll(cursorHelp(query))
		for dept in dept_data:
			if dept['did'] not in deptid_list: #take only the registered depts
				continue
			dict_single_row['did'] = dept['did']
			dict_single_row['department_name'] = dept['department']
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkDept']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		maincat_obj = stkMainCategory.objects.all()
		for maincat in maincat_obj:
			dict_single_row['maincat_id'] = maincat.maincatid
			dict_single_row['maincat_name'] = maincat.maincatname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkMainCategory']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		unit_obj = stkUnits.objects.all()
		for unit in unit_obj:
			dict_single_row['unit_id'] = unit.unitid
			dict_single_row['unit_name'] = unit.unitname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkUnits']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		subcat_obj = stkSubCategory.objects.defer('subcatid','subcatname')
		for subcat in subcat_obj:
			dict_single_row['subcat_id'] = subcat.subcatid
			dict_single_row['subcat_name'] = subcat.subcatname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSubCategory']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		item_obj = stkItemMaster.objects.all().select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			#dict_single_row['qty_available'] = item.modelid.qtyavailable
			free_itemcount = stkItemDetails.objects.filter(itemid_id=item.itemid,issuedornot='N', healthid_id=1,purchasereturnid_id__isnull=True).count() #purchase return part is new [purchase return id of free item is null]
			dict_single_row['qty_available'] = free_itemcount
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadLocations(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		dept_id = params['did']
		location_obj = stkLocation.objects.filter(deptid=dept_id)
		for location in location_obj:
			dict_single_row['location_id'] = location.locationid
			dict_single_row['location_name'] = location.locationname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkLocation']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
		return HttpResponse("success")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadItemsForSubcatId(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		subcat_id = params['subcatid']
		item_obj = stkItemMaster.objects.filter(subcatid_id=subcat_id).select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			#dict_single_row['qty_available'] = item.modelid.qtyavailable
			free_itemcount = stkItemDetails.objects.filter(itemid_id=item.itemid,issuedornot='N', healthid_id=1).count()
			dict_single_row['qty_available'] = free_itemcount
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def issueSubmit(request):
	list_of_rows=[]
	dict_single_row={}
	if request.method == 'POST':
		#print request.body
		params = json.loads(request.body)
		todept = params['todept']
		tolocation = params['tolocation']
		item_id = params['itemid']
		qty = params['qty']
		unitid = params['unitid']
		maincatid = params['maincatid']
		try:
			with transaction.atomic():
				itemmaster_obj = stkItemMaster.objects.filter(itemid=item_id)
				if itemmaster_obj[0].qtyavailable < qty:
					return HttpResponse("No sufficient quantity available.")
				issue_obj = stkIssue(issuedate=datetime.now().date(), issuedqty=qty, issuedbyid=request.session['session_empid'], issueddeptid_id=todept, unitid_id=unitid, maincatid_id=maincatid)
				issue_obj.save()
				itemdetails_obj = stkItemDetails.objects.filter(itemid_id=item_id, issuedornot='N', healthid_id=1, purchasereturnid_id__isnull=True).order_by('itemdetailsid')#purchasereturn is newly added
				for i in range(0 , qty): #for(i=0;i<qty;i++)
					issuedetails_obj = stkIssueDetails(issueid_id=issue_obj.issueid, itemdetailsid_id=itemdetails_obj[i].itemdetailsid)
					issuedetails_obj.save()
					tempitemdetails = stkItemDetails.objects.filter(itemdetailsid=itemdetails_obj[i].itemdetailsid).update(issuedornot='Y', deptid_id=todept, locationid_id=tolocation, issueid_id=issue_obj.issueid)
				new_qty = itemmaster_obj[0].qtyavailable - qty
				itemmaster_obj.update(qtyavailable=new_qty)
				modelmaster_obj = stkModelMaster.objects.defer('modelid','qtyavailable').filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				dict_single_row['status'] = "success"
				dict_single_row['issueid'] = issue_obj.issueid
				dict_single_row['issuedate'] = datetime.now().date()
				dict_single_row['issuedqty'] = qty
				dict_single_row['issuedbyid'] = request.session['session_empid']
				dict_single_row['issueddeptid'] = todept
				dict_single_row['unitid'] = unitid
				dict_single_row['maincatid'] = maincatid
				#get EMP code corresponding to EMPid
				query = "SELECT * FROM \"hrmBasicInfo\" WHERE personalid='"+str(request.session['session_empid'])+"'"
				result_data = dictFetchAll(cursorHelp(query))
				dict_single_row['issuedbyempcode'] = result_data[0]['empcode']
				#get DEPT name from deptid
				query = "SELECT * FROM \"hrmDepartment\" WHERE did='"+str(todept)+"'"
				result_data = dictFetchAll(cursorHelp(query))
				dict_single_row['issueddeptname'] = result_data[0]['department']
				issuedetail_obj = stkIssueDetails.objects.filter(issueid_id=issue_obj.issueid).select_related()
				#get item name...
				item_obj = stkItemMaster.objects.filter(itemid=issuedetail_obj[0].itemdetailsid.itemid_id).select_related()
				dict_single_row['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname		
				dict_single_row['itemid'] = item_obj[0].itemid
				dict_single_row['locationid'] = issuedetail_obj[0].itemdetailsid.locationid_id
				
				list_of_rows.append(dict_single_row.copy())
				response = JsonResponse(list_of_rows,safe=False)
				return HttpResponse(response.content)
				#return HttpResponse("success")
		except IndexError: #no need just to indicate a mistake
			dict_single_row['status'] = "failed"
			dict_single_row['data'] = "No such item existing. [NO Item details items]"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
		except Exception as e:#ObjectDoesNotExist
			dict_single_row['status'] = "failed"
			dict_single_row['data'] = "failed"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def issueTableView(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		issue_obj = stkIssue.objects.all()
		for issue in issue_obj:
			dict_single_row['issueid'] = issue.issueid
			if issue.issuedate != None: #can be null in case of existing item.
				dict_single_row['issuedate'] = str(issue.issuedate)
			else:
				dict_single_row['issuedate'] = ""
			dict_single_row['issuedqty'] = issue.issuedqty
			dict_single_row['issuedbyid'] = str(issue.issuedbyid)
			dict_single_row['issueddeptid'] = issue.issueddeptid_id
			dict_single_row['unitid'] = issue.unitid_id
			dict_single_row['maincatid'] = issue.maincatid_id
			#get EMP code corresponding to EMPid
			if issue.issuedbyid != None: #can be null in case of existing item.
				query = "SELECT * FROM \"hrmBasicInfo\" WHERE personalid='"+issue.issuedbyid+"'"
				result_data = dictFetchAll(cursorHelp(query))
				dict_single_row['issuedbyempcode'] = result_data[0]['empcode']
			else:
				dict_single_row['issuedbyempcode'] = "" #null
			#get DEPT name from deptid
			query = "SELECT * FROM \"hrmDepartment\" WHERE did='"+str(issue.issueddeptid_id)+"'"
			result_data = dictFetchAll(cursorHelp(query))
			dict_single_row['issueddeptname'] = result_data[0]['department']

			#details of items associated with the issue...
			dict_single_subrow={} #reinitialize
			list_of_subrows=[]
			issuedetail_obj = stkIssueDetails.objects.filter(issueid_id=issue.issueid).select_related()
			
			#for issuedetail in issuedetail_obj:
			#	dict_single_subrow['itemdetailsid'] = issuedetail.itemdetailsid_id
			#	dict_single_subrow['itemid'] = issuedetail.itemdetailsid.itemid_id
			#	dict_single_subrow['fisatid'] = issuedetail.itemdetailsid.fisatid
			#	list_of_subrows.append(dict_single_subrow.copy())
			#dict_single_row['issueDetails'] = list_of_subrows
			
			#get item name...
			try: #if purchase records of issued items deleted here comes the exception. solved in purchasedelete with dependent entries
				item_obj = stkItemMaster.objects.filter(itemid=issuedetail_obj[0].itemdetailsid.itemid_id).select_related()
				dict_single_row['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname		
				dict_single_row['itemid'] = item_obj[0].itemid
				dict_single_row['locationid'] = issuedetail_obj[0].itemdetailsid.locationid_id
				list_of_rows.append(dict_single_row.copy())
			except Exception as e:
				print "exception occured"
			
		dict_full_content['stkIssue']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def issueUpdate(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		issue_id = params['issueid']
		todept = params['todept']
		tolocation = params['tolocation']
		item_id = params['itemid']
		qty = params['qty']
		unitid = params['unitid']
		maincatid = params['maincatid']
		try:
			with transaction.atomic():
				issue_obj = stkIssue.objects.filter(issueid=issue_id)
				qty_difference = qty - issue_obj[0].issuedqty #if +ve then generate if -ve then delete, 0 no change
				issue_obj.update(issuedqty=qty, issueddeptid_id=todept, unitid_id=unitid, maincatid_id=maincatid)
				itemmaster_obj = stkItemMaster.objects.filter(itemid=item_id)
				if qty_difference == 0:
					print "no change"
				elif qty_difference > 0: #then generate the extra ones...
					print "greater then generated"
					if itemmaster_obj[0].qtyavailable < qty_difference:
						return HttpResponse("No sufficient quantity available.")
					itemdetails_obj = stkItemDetails.objects.filter(itemid_id=item_id, issuedornot='N', healthid_id=1).order_by('itemdetailsid')
					for i in range(0, qty_difference): #[i=0;i<(qty_difference);i++]
						issuedetails_obj = stkIssueDetails(issueid_id=issue_id, itemdetailsid_id=itemdetails_obj[i].itemdetailsid)
						issuedetails_obj.save()
						tempitemdetails = stkItemDetails.objects.filter(itemdetailsid=itemdetails_obj[i].itemdetailsid).update(issuedornot='Y', deptid_id=todept, locationid_id=tolocation, issueid_id=issue_id)
					new_qty = itemmaster_obj[0].qtyavailable - qty_difference #more are generated so reduce available ones
						
				else: #then delete the unwanted
					print "del extra"
					print abs(qty_difference)
					itemdetails_obj = stkItemDetails.objects.filter(issueid_id=issue_id).order_by('itemdetailsid')
					for i in range(0, abs(qty_difference)): #[i=0;i<(qty_difference);i++]
						issuedetails_obj = stkIssueDetails.objects.filter(itemdetailsid_id=itemdetails_obj[i].itemdetailsid).delete()
						tempitemdetails = stkItemDetails.objects.filter(itemdetailsid=itemdetails_obj[i].itemdetailsid).update(issuedornot='N', deptid_id='', locationid_id='', issueid_id='')
						print "del:"+str(itemdetails_obj[i].itemdetailsid)

					new_qty = itemmaster_obj[0].qtyavailable + abs(qty_difference) #more are freed so add
				#update quantity...
				if qty_difference != 0: #in case of first if case their is no change.
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.defer('modelid','qtyavailable').filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				return HttpResponse("success")

		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def issueDelete(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		issue_id = params['issue_id']
		try:
			with transaction.atomic():
				issuedetails_obj = stkIssueDetails.objects.filter(issueid_id=issue_id).select_related()
				item_id = issuedetails_obj[0].itemdetailsid.itemid_id
				for issuedetail in issuedetails_obj:
					itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=issuedetail.itemdetailsid_id).update(issuedornot='N', deptid_id='', locationid_id='', issueid_id='')
				issuedetails_obj.delete()
				issue_obj = stkIssue.objects.filter(issueid=issue_id)
				qty_freed = issue_obj[0].issuedqty
				issue_obj.delete()
				#update freed qty...
				itemmaster_obj = stkItemMaster.objects.filter(itemid=item_id).select_related()
				available_qty = itemmaster_obj[0].qtyavailable
				new_qty = available_qty + qty_freed
				model_id = itemmaster_obj[0].modelid_id
				itemmaster_obj.update(qtyavailable=new_qty)
				modelmaster_obj = stkModelMaster.objects.filter(modelid=model_id).update(qtyavailable=new_qty)
				return HttpResponse("success")
		except Exception as e:#ObjectDoesNotExist
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def existParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		dept_obj = stkDept.objects.defer('deptid')
		deptid_list = [single_dept.deptid for single_dept in dept_obj]
		query = "select * from \"hrmDepartment\" where displayinstock=1"
		dept_data = dictFetchAll(cursorHelp(query))
		for dept in dept_data:
			if dept['did'] not in deptid_list: #take only the registered depts
				continue
			dict_single_row['did'] = dept['did']
			dict_single_row['department_name'] = dept['department']
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkDept']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		unit_obj = stkUnits.objects.all()
		for unit in unit_obj:
			dict_single_row['unit_id'] = unit.unitid
			dict_single_row['unit_name'] = unit.unitname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkUnits']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		subcat_obj = stkSubCategory.objects.defer('subcatid','subcatname')
		for subcat in subcat_obj:
			dict_single_row['subcat_id'] = subcat.subcatid
			dict_single_row['subcat_name'] = subcat.subcatname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSubCategory']=list_of_rows

		dict_single_row={}
		list_of_rows=[]
		itemdetails_obj = stkItemDetails.objects.defer('fisatid')
		for detail in itemdetails_obj:
			dict_single_row['fisatid'] = detail.fisatid
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkFisatIds']=list_of_rows

		'''
		dict_single_row={}
		list_of_rows=[]
		item_obj = stkItemMaster.objects.all().select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['unit_id'] = item.unitid_id
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			dict_single_row['qty_available'] = item.modelid.qtyavailable
			item_detail_total_count=stkItemDetails.objects.filter(itemid_id=item.itemid).count()
			item_detail_purch_count=stkItemDetails.objects.filter(itemid_id=item.itemid,purchaseid__isnull=False).count()
			item_purch_return_count=stkItemDetails.objects.filter(itemid_id=item.itemid,purchasereturnid_id__isnull=False).count()#new..
			item_detail_exist_issued_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='Y',issueid__isnull=False).count()
			item_detail_exist_notissued_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='Y',issueid__isnull=True).count()
			item_detail_returndept_good_nonexist_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='N',issueid__isnull=True,health='G').exclude(returnedfromdept=0).count()
			item_detail_returndept_bad_nonexist_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='N',issueid__isnull=True).exclude(returnedfromdept=0,health='G').count()
			dict_single_row['qty_remaining_toadd'] = (item.modelid.qtyavailable + item_detail_total_count) - (item_detail_purch_count*2-item_purch_return_count) - (item_detail_exist_notissued_count*2)-item_detail_exist_issued_count - item_detail_returndept_good_nonexist_count + item_detail_returndept_bad_nonexist_count#(reduce all unwanted items from total. reduce purchase count twice because, it is already added twice ie, increase qty_available and add items to stlItemDetails. Existing non issued item also twice ie, already included in qty_available and added item in stkItemDetails. Also remove existing issued item count,purchase return count already reflected in the qtyavailable but present in stkItemDetails. So reduce it from purchase count only once. After return from dept if health is good then qtyavailable is increased by 1, thus item_detail_returndept_good_nonexist_count used to balance the remain count.)
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows
		'''

		dict_single_row={}
		list_of_rows=[]
		item_obj = stkItemMaster.objects.all().select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['unit_id'] = item.unitid_id
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			itemdetailscount=stkItemDetails.objects.filter(itemid_id=item.itemid,existing="Y").count()
			dict_single_row['qty_remaining_toadd'] = int(item.existingqty) - int(itemdetailscount)
			#print int(item.existingqty) - int(itemdetailscount)
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadRemainingToAddItemsForSubcatId(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		params = json.loads(request.body)
		subcat_id = params['subcatid']
		item_obj = stkItemMaster.objects.filter(subcatid_id=subcat_id).select_related()
		for item in item_obj:
			dict_single_row['item_id'] = item.itemid
			dict_single_row['unit_id'] = item.unitid_id
			dict_single_row['item_name'] = item.brandid.brandname +" " +item.modelid.modelname
			dict_single_row['model_code'] = item.modelid.modelcode
			'''
			dict_single_row['qty_available'] = item.modelid.qtyavailable
			item_detail_total_count=stkItemDetails.objects.filter(itemid_id=item.itemid).count()
			item_detail_purch_count=stkItemDetails.objects.filter(itemid_id=item.itemid,purchaseid__isnull=False).count()
			item_detail_exist_issued_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='Y',issueid__isnull=False).count()
			item_detail_exist_notissued_count=stkItemDetails.objects.filter(itemid_id=item.itemid,existing='Y',issueid__isnull=True).count()
			dict_single_row['qty_remaining_toadd'] = (item.modelid.qtyavailable + item_detail_total_count) - (item_detail_purch_count*2) - (item_detail_exist_notissued_count*2)-item_detail_exist_issued_count #(reduce all unwanted items from total. reduce purchase count twice because, it is already added twice ie, increase qty_available and add items to stlItemDetails. Existing non issued item also twice ie, already included in qty_available and added item in stkItemDetails. Also remove existing issued item count)
			'''
			itemdetailscount=stkItemDetails.objects.filter(itemid_id=item.itemid,existing="Y").count()
			dict_single_row['qty_remaining_toadd'] = int(item.existingqty) - int(itemdetailscount)
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemMaster']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def existSubmit(request):
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		print request.body
		item_id = params['itemid']
		qty = params['qty']
		unit_id = params['unitid']
		#fitid = params['fitid']
		isissued = params['issuedornot']
		todept = params['todept']
		tolocation = params['tolocation']
		issue_date = params['issuedate']
		json_fitids = json.loads(params['jsonids'])
		try:
			with transaction.atomic():
				if isissued == False: #existing non issued item. qty_available already entered at item registration time.
					print "Non issued item"
					#insert to stkItemDetails [generate quantity number of items]...
					for i in range(0, int(qty)): #[i=0;i<(qty);i++]
						itemdetails_obj = stkItemDetails(fisatid=json_fitids[i]['fitid'], itemid_id=item_id, existing='Y', firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'], manualentered='Y')
						itemdetails_obj.save()
						if json_fitids[i]['warrantyto'] !="":
							warranty_obj = stkWarrantyOrAmc(warrantyfrom=datetime.now().date(),warrantyto=json_fitids[i]['warrantyto'],itemdetailsid_id=itemdetails_obj.itemdetailsid) #woramc is default 'W'
							warranty_obj.save()
							stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetails_obj.itemdetailsid).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);
						print "item:"+str(i)
						############################
						dict_single_row['itemdetailsid'] = itemdetails_obj.itemdetailsid
						dict_single_row['fisatid'] = itemdetails_obj.fisatid
						dict_single_row['issuedornot'] = itemdetails_obj.issuedornot
						dict_single_row['itemid'] = itemdetails_obj.itemid_id
						item_obj = stkItemMaster.objects.filter(itemid=itemdetails_obj.itemid_id).select_related()		
						dict_single_row['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname
						dict_single_row['deptid'] = ""
						dict_single_row['todeptname'] = ""
						dict_single_row['tolocationid'] = ""
						dict_single_row['tolocationname'] = ""
						dict_single_row['issueid'] = ""
						dict_single_row['issuedate'] = ""
						if json_fitids[i]['warrantyto'] == "":
							dict_single_row['warrantyto'] = ""
						else:
							dict_single_row['warrantyto'] = json_fitids[i]['warrantyto']
						dict_single_row['status'] = "success"
						list_of_rows.append(dict_single_row.copy())
					#update qty_available...
					itemmaster_obj = stkItemMaster.objects.filter(itemid=item_id)
					new_qty_available = itemmaster_obj[0].qtyavailable + qty
					itemmaster_obj.update(qtyavailable=new_qty_available)
					modelmaster_obj = stkModelMaster.objects.defer('modelid','qtyavailable').filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty_available)
						############################				

				else: #exist an already issued item. qty_available must be decreased after issue.
					print "Already issued item"
					itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable').filter(itemid=item_id)
					issue_obj = stkIssue(issuedate=issue_date, issuedqty=qty, issueddeptid_id=todept, unitid_id=unit_id, maincatid_id=itemmaster_obj[0].maincatid_id)
					issue_obj.save()
					for i in range(0 , int(qty)): #for(i=0;i<qty;i++)
						itemdetails_obj = stkItemDetails(fisatid=json_fitids[i]['fitid'], itemid_id=item_id, existing='Y', firmid_id=request.session['session_firmid'], storeid_id=request.session['selected_store_id'], issuedornot='Y', deptid_id=todept, locationid_id=tolocation, issueid_id=issue_obj.issueid, manualentered='Y')
						itemdetails_obj.save()
						issuedetails_obj = stkIssueDetails(issueid_id=issue_obj.issueid, itemdetailsid_id=itemdetails_obj.itemdetailsid)
						issuedetails_obj.save()
						if json_fitids[i]['warrantyto'] !="":
							warranty_obj = stkWarrantyOrAmc(warrantyfrom=datetime.now().date(),warrantyto=json_fitids[i]['warrantyto'],itemdetailsid_id=itemdetails_obj.itemdetailsid) #woramc is default 'W'
							warranty_obj.save()
							stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetails_obj.itemdetailsid).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);

						############################
						dict_single_row['itemdetailsid'] = itemdetails_obj.itemdetailsid
						dict_single_row['fisatid'] = itemdetails_obj.fisatid
						dict_single_row['issuedornot'] = itemdetails_obj.issuedornot
						dict_single_row['itemid'] = itemdetails_obj.itemid_id
						item_obj = stkItemMaster.objects.filter(itemid=itemdetails_obj.itemid_id).select_related()		
						dict_single_row['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname

						#get DEPT name from deptid
						if itemdetails_obj.deptid_id != None: #can be null in case of unissued item.
							dict_single_row['deptid'] = itemdetails_obj.deptid_id
							query = "SELECT * FROM \"hrmDepartment\" WHERE did='"+str(itemdetails_obj.deptid_id)+"'"
							result_data = dictFetchAll(cursorHelp(query))
							dict_single_row['todeptname'] = result_data[0]['department']
						else:
							dict_single_row['deptid'] = ""
							dict_single_row['todeptname'] = ""
						#get LOCATION name from locationid...
						if itemdetails_obj.locationid_id != None:
							dict_single_row['tolocationid'] = itemdetails_obj.locationid_id
							location_obj = stkLocation.objects.defer('locationname').filter(locationid=itemdetails_obj.locationid_id)
							dict_single_row['tolocationname'] = location_obj[0].locationname
						else:
							dict_single_row['tolocationid'] = ""
							dict_single_row['tolocationname'] = ""

						#get issue date...
						if issue_obj.issueid != None:
							dict_single_row['issueid'] = issue_obj.issueid
							#issue_obj = stkIssue.objects.defer('issuedate').filter(issueid=issue_obj.issueid)
							if issue_obj.issuedate != None:
								dict_single_row['issuedate'] = issue_obj.issuedate
							else:
								dict_single_row['issuedate'] = ""
						else:
							dict_single_row['issueid'] = ""
							dict_single_row['issuedate'] = ""

						#warranty to date...
						if json_fitids[i]['warrantyto'] == "":
							dict_single_row['warrantyto'] = ""
						else:
							dict_single_row['warrantyto'] = json_fitids[i]['warrantyto']
						dict_single_row['status'] = "success"
						list_of_rows.append(dict_single_row.copy())
						############################

						#tempitemdetails = stkItemDetails.objects.filter(itemdetailsid=itemdetails_obj[i].itemdetailsid).update(issuedornot='Y', deptid_id=todept, locationid_id=tolocation, issueid_id=issue_obj.issueid)
					'''new_qty = itemmaster_obj[0].qtyavailable - qty
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.defer('modelid','qtyavailable').filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)'''

				response = JsonResponse(list_of_rows,safe=False)
				return HttpResponse(response.content)
				#return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			dict_single_row['status'] = "failed"
			list_of_rows.append(dict_single_row.copy())
			response = JsonResponse(list_of_rows,safe=False)
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def existingTableView(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		itemdetails_obj = stkItemDetails.objects.filter(existing='Y',healthid_id=1).select_related()
		for detail in itemdetails_obj:
			dict_single_row['itemdetailsid'] = detail.itemdetailsid
			dict_single_row['fisatid'] = detail.fisatid
			dict_single_row['issuedornot'] = detail.issuedornot
			dict_single_row['itemid'] = detail.itemid_id
			item_obj = stkItemMaster.objects.filter(itemid=detail.itemid_id).select_related()		
			dict_single_row['itemname'] = item_obj[0].brandid.brandname +" " +item_obj[0].modelid.modelname

			#get DEPT name from deptid
			if detail.deptid_id != None: #can be null in case of unissued item.
				dict_single_row['deptid'] = detail.deptid_id
				query = "SELECT * FROM \"hrmDepartment\" WHERE did='"+str(detail.deptid_id)+"'"
				result_data = dictFetchAll(cursorHelp(query))
				dict_single_row['todeptname'] = result_data[0]['department']
			else:
				dict_single_row['deptid'] = ""
				dict_single_row['todeptname'] = ""
			#get LOCATION name from locationid...
			if detail.locationid_id != None:
				dict_single_row['tolocationid'] = detail.locationid_id
				location_obj = stkLocation.objects.defer('locationname').filter(locationid=detail.locationid_id)
				dict_single_row['tolocationname'] = location_obj[0].locationname
			else:
				dict_single_row['tolocationid'] = ""
				dict_single_row['tolocationname'] = ""

			#get issue date...
			if detail.issueid_id != None:
				dict_single_row['issueid'] = detail.issueid_id
				issue_obj = stkIssue.objects.defer('issuedate').filter(issueid=detail.issueid_id)
				if issue_obj[0].issuedate != None:
					dict_single_row['issuedate'] = issue_obj[0].issuedate
				else:
					dict_single_row['issuedate'] = ""
			else:
				dict_single_row['issueid'] = ""
				dict_single_row['issuedate'] = ""

			#find warranty to date...
			if detail.warrantyoramcid_id != None:
				dict_single_row['warrantyto'] = detail.warrantyoramcid.warrantyto	
			else:
				dict_single_row['warrantyto'] = ""		
			list_of_rows.append(dict_single_row.copy())
		#list_of_rows = []	
		dict_full_content['stkItemDetails']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def existUpdate(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print request.body
		itemdetails_id = params['itemdetailsid']
		issue_id = params['issueid']
		issued_date = params['issueddate']
		fit_id = params['fitid']
		is_issued = params['isissued']
		war_todate = params['warrantyto']
		try:
			with transaction.atomic():
				itemdetails_obj = stkItemDetails.objects.defer('itemdetailsid','fisatid').filter(itemdetailsid=itemdetails_id).update(fisatid=fit_id)
				if is_issued == True:
					issue_obj = stkIssue.objects.defer('issueid','issuedate').filter(issueid=issue_id).update(issuedate=issued_date)

				#update warrenty information...
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id).select_related()
				if itemdetails_obj[0].warrantyoramcid_id != None: #already in database [in itemdetails table]
					if war_todate != "": #also in params list [so update]
						stkWarrantyOrAmc.objects.filter(itemdetailsid_id=itemdetails_id).update(warrantyto=war_todate)
						print "updated"
					else: #currently have a warrenty in database but not in the params so delete warranty entry...
						stkItemDetails.objects.filter(itemdetailsid=itemdetails_id).update(warrantyoramcid="")
						warranty_obj = stkWarrantyOrAmc.objects.filter(itemdetailsid_id=itemdetails_id).delete()
				else: #not already in database [in itemdetails table]
					if war_todate != "": #also present in params list
						warranty_obj = stkWarrantyOrAmc(warrantyfrom=datetime.now().date(), warrantyto=war_todate, itemdetailsid_id=itemdetails_id) #woramc is default 'W'
						warranty_obj.save()
						stkItemDetails.objects.defer('itemdetailsid','warrantyoramcid_id').filter(itemdetailsid=itemdetails_id).update(warrantyoramcid_id=warranty_obj.warrantyoramcid);
						print "created"
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def existDelete(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print request.body
		itemdetails_id = params['itemdetailsid']
		issue_id = params['issueid']
		is_issued = params['isissued']
		try:
			with transaction.atomic():
				if is_issued == False:
					print "Non issued item"
					itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id).delete() #no need to update qty available. Its already specified in item registration.
				else:
					print "Issued item"
					issuedetails_obj = stkIssueDetails.objects.filter(itemdetailsid_id=itemdetails_id).delete()
					itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id)
					item_id = itemdetails_obj[0].itemid_id
					itemdetails_obj.delete()
					issue_obj = stkIssue.objects.filter(issueid=issue_id)
					new_issue_qty = issue_obj[0].issuedqty - 1 #reduce issued qty by 1
					issue_obj.update(issuedqty=new_issue_qty)
					if stkIssueDetails.objects.filter(issueid_id=issue_id).exists():
						print "No change"
					else: #if no issueDetails entry for stkIssue record, then delete the stkIssue record.
						issue_obj = stkIssue.objects.filter(issueid=issue_id).delete()
					#update qty_available...
					itemmaster_obj = stkItemMaster.objects.filter(itemid=item_id)
					new_qty_available = itemmaster_obj[0].qtyavailable + 1
					itemmaster_obj.update(qtyavailable=new_qty_available)
					modelmaster_obj = stkModelMaster.objects.defer('modelid','qtyavailable').filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty_available)
				return HttpResponse("success")
		except Exception as e:#ObjectDoesNotExist
			return HttpResponse("This item can't be deleted.")
	else:
		return HttpResponse("Only post request is possible")

#just to load supplier details...
@csrf_protect
def purchaseReturnParams(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		supplier_obj = stkSupplier.objects.defer('supplierid','suppliername')
		for supplier in supplier_obj:
			dict_single_row['supplierid'] = supplier.supplierid
			dict_single_row['suppliername'] = supplier.suppliername
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSupplier']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#load itemnames from stkItemMaster (to load autocomplete)
@csrf_protect
def loadItemsForPurReturnAutocomplete(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method=='POST':
		params = json.loads(request.body)
		print request.body
		supplier_id = params['supplierid']
		invoice_no = params['invoiceno']
		try:
			purchasemaster_obj = stkPurchaseMaster.objects.defer('supplierid_id','invoiceno','purchaseid').filter(supplierid_id=supplier_id,invoiceno=invoice_no)
			purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid=purchasemaster_obj[0].purchaseid).select_related()
			for info in purchaseinfo_obj:
				dict_single_row['itemid'] = info.itemid_id
				dict_single_row['itemcode'] = info.itemid.itemcode
				itemmaster_obj = stkItemMaster.objects.filter(itemid=info.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
				dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
				list_of_rows.append(dict_single_row.copy())
			dict_full_content['itemMasterData']=list_of_rows
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
		except Exception as e:
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#load data from stkItemMaster (corresponds to invoiceno and supplierid)
@csrf_protect
def loadItemsForInvoice(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method=='POST':
		params = json.loads(request.body)
		print request.body
		invoice_no = params['invoiceno']
		try:
			purchasemaster_obj = stkPurchaseMaster.objects.defer('supplierid_id','invoiceno','purchaseid').filter(invoiceno=invoice_no)
			purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid).select_related()
			for info in purchaseinfo_obj:
				dict_single_row['itemid'] = info.itemid_id
				dict_single_row['itemcode'] = info.itemid.itemcode
				itemmaster_obj = stkItemMaster.objects.filter(itemid=info.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
				dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
				#get fitids of individual items...
				itemdetails_obj = stkItemDetails.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid, itemid=info.itemid_id, itemoutgoingstatus='N', issuedornot='N', installedornot='N', purchasereturnid_id__isnull=True)
				dict_single_subrow = {}
				list_of_subrows = []
				for item in itemdetails_obj:
					dict_single_subrow['fitid'] = item.fisatid
					dict_single_subrow['itemdetailsid'] = item.itemdetailsid
					dict_single_subrow['val'] = None
					list_of_subrows.append(dict_single_subrow.copy())
				dict_single_row['stkItemDetails'] = list_of_subrows
				list_of_rows.append(dict_single_row.copy())
			#dict_full_content['stkItemDetails']=list_of_subrows
			dict_full_content['stkItemMaster']=list_of_rows
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
		except Exception as e:
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadSupplierForInvoice(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		invoice_no = params['invoiceno']
		purchasemaster_obj = stkPurchaseMaster.objects.defer('supplierid_id','invoiceno','purchaseid').filter(invoiceno=invoice_no).select_related()
		for purchase in purchasemaster_obj:
			dict_single_row['supplierid'] = purchase.supplierid_id
			dict_single_row['suppliername'] = purchase.supplierid.suppliername
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkSupplier']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#load data from stkItemMaster (corresponds to invoiceno and supplierid)
@csrf_protect
def loadItemsForSupplierAndInvoice(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method=='POST':
		params = json.loads(request.body)
		print request.body
		supplier_id = params['supplierid']
		invoice_no = params['invoiceno']
		try:
			purchasemaster_obj = stkPurchaseMaster.objects.defer('supplierid_id','invoiceno','purchaseid').filter(supplierid_id=supplier_id,invoiceno=invoice_no)
			purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid).select_related()
			for info in purchaseinfo_obj:
				dict_single_row['itemid'] = info.itemid_id
				dict_single_row['itemcode'] = info.itemid.itemcode
				itemmaster_obj = stkItemMaster.objects.filter(itemid=info.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
				dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
				#get fitids of individual items...
				itemdetails_obj = stkItemDetails.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid, itemid=info.itemid_id, itemoutgoingstatus='N', issuedornot='N', installedornot='N', purchasereturnid_id__isnull=True)
				dict_single_subrow = {}
				list_of_subrows = []
				for item in itemdetails_obj:
					dict_single_subrow['fitid'] = item.fisatid
					dict_single_subrow['itemdetailsid'] = item.itemdetailsid
					dict_single_subrow['val'] = None
					list_of_subrows.append(dict_single_subrow.copy())
				dict_single_row['stkItemDetails'] = list_of_subrows
				list_of_rows.append(dict_single_row.copy())
			#dict_full_content['stkItemDetails']=list_of_subrows
			dict_full_content['stkItemMaster']=list_of_rows
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
		except Exception as e:
			response = JsonResponse(dict_full_content,safe=False)
			#print response.content
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#load data from stkItemMaster (corresponds to invoiceno , supplierid and itemid)
@csrf_protect
def loadItemsForSupplierInvoiceAndItem(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	dict_single_subrow={}
	list_of_subrows=[]
	if request.method=='POST':
		params = json.loads(request.body)
		#print request.body
		supplier_id = params['supplierid']
		invoice_no = params['invoiceno']
		item_id = params['itemid']
		try:
			purchasemaster_obj = stkPurchaseMaster.objects.defer('supplierid','invoiceno','purchaseid').filter(supplierid_id=supplier_id,invoiceno=invoice_no)
			purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid, itemid_id=item_id).select_related()
			for info in purchaseinfo_obj:
				dict_single_row['itemid'] = info.itemid_id
				dict_single_row['itemcode'] = info.itemid.itemcode
				itemmaster_obj = stkItemMaster.objects.filter(itemid=info.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
				dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
				#get fitids of individual items...
				itemdetails_obj = stkItemDetails.objects.filter(purchaseid_id=purchasemaster_obj[0].purchaseid, itemid=info.itemid_id, itemoutgoingstatus='N', issuedornot='N', installedornot='N', purchasereturnid_id__isnull=True)
				dict_single_subrow = {}
				list_of_subrows = []
				for item in itemdetails_obj:
					dict_single_subrow['fitid'] = item.fisatid
					dict_single_subrow['itemdetailsid'] = item.itemdetailsid
					dict_single_subrow['val'] = None
					list_of_subrows.append(dict_single_subrow.copy())
				dict_single_row['stkItemDetails'] = list_of_subrows
				list_of_rows.append(dict_single_row.copy())
			#dict_full_content['stkItemDetails']=list_of_subrows
			dict_full_content['stkItemMaster']=list_of_rows
			response = JsonResponse(dict_full_content,safe=False)
			print "invoice and itemmmm"
			print response.content
			return HttpResponse(response.content)
		except ObjectDoesNotExist:#Exception as e
			response = JsonResponse(dict_full_content,safe=False)
			print response.content
			return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

#submit purchase return...
@csrf_protect
def purchaseReturnSubmit(request):
	if request.method=='POST':
		#print request.body
		params = json.loads(request.body)
		returned_by = params['returnedby']
		descriptionvalue = params['description']
		jsonAllSelected = json.loads(params['jsonAllSelected'])
		try:
			with transaction.atomic():
				itemdetails_obj=stkItemDetails.objects.filter(itemdetailsid=jsonAllSelected[0]['itemdetailsid'])#all these blng to same purchase
				purchase_id = itemdetails_obj[0].purchaseid_id
				for returneditem in jsonAllSelected:
					itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=returneditem['itemid'])#to get maincatid [remaining use at the end of this for loop]
					purchasereturn_obj = stkPurchaseReturn(returneddate=datetime.now().date(), returnedbyid=returned_by, enteredbyid=request.session['session_empcode'], maincatid_id=itemmaster_obj[0].maincatid_id, purchaseid_id=purchase_id, itemdetailsid_id=returneditem['itemdetailsid'], description=descriptionvalue)
					purchasereturn_obj.save()
					#update stkItemDetails
					itemdetails_obj = stkItemDetails.objects.defer('itemdetailsid','purchasereturnid_id').filter(itemdetailsid=returneditem['itemdetailsid']).update(purchasereturnid_id=purchasereturn_obj.purchasereturnid)
					#update stkPurchaseInfo
					purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchase_id, itemid_id=returneditem['itemid'])
					new_prqty = purchaseinfo_obj[0].purchasereturnqty + 1 #update purchase return quantity
					purchaseinfo_obj.update(purchasereturnstatus='Y', purchasereturnqty=new_prqty) #purchasereturnid_id =purchasereturn_obj.purchasereturnid, is moved to stkPurchaseReturnDetails table.
					#connect stkPurchaseInfo and stkPurchaseReturnDetails
					purchasereturndetails_obj = stkPurchaseReturnDetails(recordid_id=purchaseinfo_obj[0].recordid, purchasereturnid_id=purchasereturn_obj.purchasereturnid)
					purchasereturndetails_obj.save()
					#update qty available in stkItemMaster and in stkModelMaster
					new_qty = itemmaster_obj[0].qtyavailable - 1 #reduce 1
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseReturnTableView(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		purchasereturn_obj = stkPurchaseReturn.objects.all().select_related()
		for preturn in purchasereturn_obj:
			dict_single_row['returneddate'] = preturn.returneddate
			dict_single_row['purchasereturnid'] = preturn.purchasereturnid
			dict_single_row['returnedby'] = preturn.returnedbyid
			dict_single_row['purchaseid'] = preturn.purchaseid_id
			dict_single_row['invoiceno'] = preturn.purchaseid.invoiceno
			dict_single_row['supplierid'] = preturn.purchaseid.supplierid_id
			dict_single_row['suppliername'] = stkSupplier.objects.defer('supplierid','suppliername').filter(supplierid=preturn.purchaseid.supplierid_id)[0].suppliername
			dict_single_row['itemdetailsid'] = preturn.itemdetailsid_id
			dict_single_row['itemid'] = preturn.itemdetailsid.itemid_id
			itemmaster_obj = stkItemMaster.objects.filter(itemid=preturn.itemdetailsid.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
			dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
			dict_single_row['fitid'] = preturn.itemdetailsid.fisatid
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkPurchaseReturn']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def purchaseReturnDelete(request):
	if request.method == 'POST':
		#print request.body
		params = json.loads(request.body)
		purchasereturn_id = params['purchasereturnid']
		purchase_id = params['purchaseid']
		itemdetails_id = params['itemdetailsid']
		item_id = params['itemid']
		try:
			with transaction.atomic():
				purchasereturndetails_obj = stkPurchaseReturnDetails.objects.filter(purchasereturnid_id=purchasereturn_id).delete()
				#update stkPurchaseInfo
				purchaseinfo_obj = stkPurchaseInfo.objects.filter(purchaseid_id=purchase_id, itemid_id=item_id)
				new_prqty = purchaseinfo_obj[0].purchasereturnqty - 1 #update purchase return quantity
				purchasereturndetails_obj=stkPurchaseReturnDetails.objects.filter(recordid_id=purchaseinfo_obj[0].recordid).exists()
				if purchasereturndetails_obj: #if atleast one of returns associated with this purchase info
					purchaseinfo_obj.update(purchasereturnstatus='Y', purchasereturnqty=new_prqty)
				else:
					purchaseinfo_obj.update(purchasereturnstatus='N', purchasereturnqty=new_prqty)
				#update stkItemDetails
				itemdetails_obj = stkItemDetails.objects.defer('itemdetailsid','purchasereturnid_id').filter(itemdetailsid=itemdetails_id).update(purchasereturnid_id=None)
				#delete purchase return entry of this item from stkPurchaseReturn
				purchasereturn_obj = stkPurchaseReturn.objects.filter(purchasereturnid=purchasereturn_id).delete()
				#update qty available
				itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=item_id)
				new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
				itemmaster_obj.update(qtyavailable=new_qty)
				modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				return HttpResponse("success")
		except Exception as e:#ObjectDoesNotExist
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadItemDetails(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		#print request.body
		params = json.loads(request.body)
		did = params['did']
		itemdetails_obj = stkItemDetails.objects.filter(deptid_id=did,issuedornot="Y")
		for item in itemdetails_obj:
			dict_single_row['fisatid'] = item.fisatid
			dict_single_row['itemdetailsid'] = item.itemdetailsid
			itemmaster_obj = stkItemMaster.objects.filter(itemid=item.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
			dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemDetails']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadRegisteredEmpCodes(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		firmaccess_obj = stkFirmAccess.objects.all()
		for detail in firmaccess_obj:
			dict_single_row['empcode'] = detail.empcode
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['allEmpCodes']=list_of_rows

		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def returnDeptSubmit(request):
	if request.method == 'POST':
		#print request.body
		params = json.loads(request.body)
		did = params['did']
		itemdetails_id = params['itemdetailsid']
		remark = params['remark']
		returnedby = params['returnedby'] #EMPcode
		status = params['status']
		#print str(did)+str(itemdetails_id)+remark+returnedby+status
		try:
			with transaction.atomic():
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id)
				issuedetails_obj = stkIssueDetails.objects.defer('itemdetailsid_id','latestissue').filter(itemdetailsid_id=itemdetails_id,latestissue=1)
				returnfromdept_obj = stkReturnFromDept(returndate=datetime.now().date(), remarks=remark, fromdeptid_id=did, issuedetailsid_id=issuedetails_obj[0].issuedetailsid, returnedbyid_id=returnedby, enteredbyid_id=request.session['session_empcode'], itemdetailsid_id=itemdetails_id, fromlocationid_id=itemdetails_obj[0].locationid_id)
				returnfromdept_obj.save()
				issuedetails_obj.update(latestissue=0) #mark as old issue entry
				newreturnfromdept = itemdetails_obj[0].returnedfromdept + 1
				itemdetails_obj.update(healthid_id=status, currentstatusid_id=3, issuedornot="N", returnedfromdept=newreturnfromdept, deptid_id=None, locationid_id=None, issueid_id=None)
				#update qty available
				if status == "G":
					itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
					new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def returnDeptTableView(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		returndept_obj = stkReturnFromDept.objects.all().select_related()
		for singlereturn in returndept_obj:
			dict_single_row['returnid'] = singlereturn.returnid
			dict_single_row['returndate'] = singlereturn.returndate
			dict_single_row['remarks'] = singlereturn.remarks
			dict_single_row['fromdeptid'] = singlereturn.fromdeptid_id
			#dict_single_row['fromdeptname'] = singlereturn.deptid.deptname
			query = "select * from \"hrmDepartment\" where did="+str(singlereturn.fromdeptid_id)
			dept_data = dictFetchAll(cursorHelp(query))
			dict_single_row['fromdeptname'] = dept_data[0]['department']
			dict_single_row['fromlocationid'] = singlereturn.fromlocationid_id
			dict_single_row['fromlocationname'] = stkLocation.objects.filter(locationid=singlereturn.fromlocationid_id)[0].locationname
			dict_single_row['issuedetailsid'] = singlereturn.issuedetailsid_id
			dict_single_row['enteredbyid'] = singlereturn.enteredbyid_id
			dict_single_row['returnedbyid'] = singlereturn.returnedbyid_id
			query = "SELECT * FROM \"hrmBasicInfo\" WHERE empcode='"+singlereturn.returnedbyid_id+"'"
			result_data = dictFetchAll(cursorHelp(query))
			dict_single_row['returnedbyname'] = result_data[0]['fullname']
			dict_single_row['itemdetailsid'] = singlereturn.itemdetailsid_id
			itemmaster_obj = stkItemMaster.objects.filter(itemid=singlereturn.itemdetailsid.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
			dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
			dict_single_row['fisatid'] = singlereturn.itemdetailsid.fisatid
			dict_single_row['health'] = singlereturn.itemdetailsid.healthid_id
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkReturnFromDept']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def returnDeptUpdate(request):
	if request.method == 'POST':
		print request.body
		params = json.loads(request.body)
		return_id = params['returnid']
		did = params['did']
		itemdetails_id = params['itemdetailsid']
		remark = params['remark']
		returnedby = params['returnedby'] #EMPcode
		status = params['status']
		flag = False
		print str(did)+str(itemdetails_id)+remark+returnedby+status
		try:
			with transaction.atomic():
				returndept_obj = stkReturnFromDept.objects.filter(returnid=return_id)
				#restoring the old item if new item is different
				if int(returndept_obj[0].itemdetailsid_id) != int(itemdetails_id): #if new and old items are different then issue the old item to where it is previously issued.
					flag = True
					print "NEW IS DIFFERENT::::::"
					oldissuedetails_obj = stkIssueDetails.objects.filter(issuedetailsid=returndept_obj[0].issuedetailsid_id)
					oldissuedetails_obj.update(latestissue=1)
					olditemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=returndept_obj[0].itemdetailsid_id)
					#update qty available
					if olditemdetails_obj[0].healthid_id == 1:
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=olditemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1 [because, increased 1 when returning good items]
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					newreturnfromdept = olditemdetails_obj[0].returnedfromdept - 1 #reduce its return from dept count by 1
					olditemdetails_obj.update(healthid_id=1, currentstatusid_id=2, issuedornot="Y", issueid_id=oldissuedetails_obj[0].issueid_id,  returnedfromdept=newreturnfromdept, deptid_id=returndept_obj[0].fromdeptid_id, locationid_id=returndept_obj[0].fromlocationid_id)

				#return the specified item from dept...
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id)
				fromlocation=0
				issuedetails_obj = None
				if flag == True:
					issuedetails_obj = stkIssueDetails.objects.defer('issuedetailsid','latestissue','itemdetailsid_id').filter(itemdetailsid_id=itemdetails_id, latestissue=1)
					fromlocation = itemdetails_obj[0].locationid_id
				else:
					issuedetails_obj = stkIssueDetails.objects.defer('issuedetailsid','latestissue','itemdetailsid_id').filter(issuedetailsid=returndept_obj[0].issuedetailsid_id)
					fromlocation = returndept_obj[0].fromlocationid_id
					if itemdetails_obj[0].healthid_id==1 and status!=1: #already returned as good but, now change to damaged.
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					if itemdetails_obj[0].healthid_id==2 and status==1: #already returned as bad but, now change to good.
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable + 1 #decrese 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				returndept_obj.update(remarks=remark, fromdeptid_id=did, issuedetailsid_id=issuedetails_obj[0].issuedetailsid, returnedbyid_id=returnedby, itemdetailsid_id=itemdetails_id, fromlocationid_id=fromlocation)
				issuedetails_obj.update(latestissue=0) #mark as old issue entry
				newreturnfromdept = itemdetails_obj[0].returnedfromdept + 1
				itemdetails_obj.update(healthid_id=status, currentstatusid_id=3, issuedornot="N", deptid_id=None, locationid_id=None, issueid_id=None)
				if flag == True: #if new item then change returnedfromdept too..
					itemdetails_obj.update(returnedfromdept=newreturnfromdept)

				#update qty available
				if status == "G" and flag == True: #if status is good and a new item
					itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
					new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("Failed.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def returnDeptDelete(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		return_id = params['returnid']
		try:
			with transaction.atomic():
				returndept_obj = stkReturnFromDept.objects.filter(returnid=return_id)
				issuedetails_obj = stkIssueDetails.objects.filter(issuedetailsid=returndept_obj[0].issuedetailsid_id)
				issuedetails_obj.update(latestissue=1) #again make it as newly issued 
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=returndept_obj[0].itemdetailsid_id)
				#update qty available
				if itemdetails_obj[0].healthid_id == 1:
					itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
					new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1 [because, increased 1 when returning good items]
					itemmaster_obj.update(qtyavailable=new_qty)
					modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				newreturnfromdept = itemdetails_obj[0].returnedfromdept - 1 #reduce its return from dept count by 1
				itemdetails_obj.update(healthid_id=1, currentstatusid_id=2, issuedornot="Y", issueid_id=issuedetails_obj[0].issueid_id,  returnedfromdept=newreturnfromdept, deptid_id=returndept_obj[0].fromdeptid_id, locationid_id=returndept_obj[0].fromlocationid_id)
				returndept_obj.delete()
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("This item can't be deleted.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadAllNonOutgoingItems(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		itemdetails_obj = stkItemDetails.objects.filter(itemoutgoingstatus="N", issuedornot="N")
		for item in itemdetails_obj:
			dict_single_row['fisatid'] = item.fisatid
			dict_single_row['itemdetailsid'] = item.itemdetailsid
			itemmaster_obj = stkItemMaster.objects.filter(itemid=item.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
			dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkItemDetails']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def loadServiceCompanies(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		company_obj = stkServiceCompany.objects.all()
		for company in company_obj:
			dict_single_row['companyid'] = company.companyid
			dict_single_row['companyname'] = company.companyname
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkServiceCompany']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def outgoingSubmit(request):
	if request.method == 'POST':
		print request.body
		params = json.loads(request.body)
		healthstatus = params['healthstatus']
		itemdetails_id = params['itemdetailsid']
		remark = params['remark']
		company_id = params['companyid']
		isnewcompany = params['isnewcompany']
		company_name = params['companyname']
		mail_id = params['mailid']
		phoneno = params['phone']
		addr = params['address']
		technician = params['technician']
		complaint = params['complaint']
		#returneddate = params['returneddate']
		#receivercode = params['receivercode']
		try:
			with transaction.atomic():
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id)
				if isnewcompany == True: #if it is a new company then register it
					if stkServiceCompany.objects.filter(companyname__iexact=company_name).exists() == True:
						return HttpResponse("companyexists")
					servicecompany_obj = stkServiceCompany(companyname=company_name, mailid=mail_id, phone=phoneno, address=addr)
					servicecompany_obj.save()
					companyidvalue = servicecompany_obj.companyid #if new company then store the new companyid
				else:
					companyidvalue = company_id #if company already there then store the companyid
				#perform outgoing process
				outgoing_obj = stkOutgoing(datedispatch=datetime.now().date(), remarks=remark, itemsenderid=request.session['session_empcode'], itemdetailsid_id=itemdetails_id, companyid_id=companyidvalue, oldhealthstatusid_id=itemdetails_obj[0].healthid_id, currentstatusid_id=healthstatus, oldoriginalstatusid_id=itemdetails_obj[0].currentstatusid_id)
				outgoing_obj.save()
				breakdown_obj = stkBreakdown(technicianname=technician, complaints=complaint, itemdetailsid_id=itemdetails_id, companyid_id=companyidvalue, itemoutgoingid_id=outgoing_obj.itemoutgoingid)
				breakdown_obj.save()
				#update in stkItemDetails and qty
				if healthstatus != 1: #if changing good item to bad
					if itemdetails_obj[0].healthid_id==1 and itemdetails_obj[0].issuedornot=='N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)

				if healthstatus == 1: #if changing bad item to good
					if itemdetails_obj[0].healthid_id!=1 and itemdetails_obj[0].issuedornot=='N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				itemdetails_obj.update(healthid_id=healthstatus, currentstatusid_id=4, itemoutgoingstatus='Y', itemoutgoingid_id=outgoing_obj.itemoutgoingid)
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("failed")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def outgoingTableView(request):
	if request.method == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		outgoing_obj = stkOutgoing.objects.all().select_related()
		for outgoing in outgoing_obj:
			dict_single_row['itemoutgoingid'] = outgoing.itemoutgoingid
			dict_single_row['datedispatch'] = outgoing.datedispatch
			dict_single_row['currentstatus'] = outgoing.currentstatusid_id
			dict_single_row['datereturn'] = "" if outgoing.datereturn==None else outgoing.datereturn
			dict_single_row['receivedstatus'] = "Not received" if outgoing.datereturn==None else ""
			dict_single_row['itemsenderid'] = outgoing.itemsenderid
			query = "SELECT * FROM \"hrmBasicInfo\" WHERE empcode='"+str(outgoing.itemsenderid)+"'"
			result_data = dictFetchAll(cursorHelp(query))
			dict_single_row['itemsendername'] = result_data[0]['fullname']
			dict_single_row['itemreceiverid'] = "" if outgoing.itemreceiverid==None else outgoing.itemreceiverid
			dict_single_row['itemdetailsid'] = outgoing.itemdetailsid_id
			dict_single_row['remarks'] = outgoing.remarks
			dict_single_row['fisatid'] = outgoing.itemdetailsid.fisatid
			dict_single_row['itemid'] = outgoing.itemdetailsid.itemid_id
			itemmaster_obj = stkItemMaster.objects.filter(itemid=outgoing.itemdetailsid.itemid_id).defer('itemid','brandid_id','modelid_id').select_related()
			dict_single_row['itemname'] = itemmaster_obj[0].brandid.brandname +" " +itemmaster_obj[0].modelid.modelname
			dict_single_row['companyid'] = outgoing.companyid_id
			dict_single_row['companyname'] = outgoing.companyid.companyname
			breakdown_obj = stkBreakdown.objects.filter(itemoutgoingid_id = outgoing.itemoutgoingid)
			dict_single_row['breakdownid'] = breakdown_obj[0].breakdownid
			dict_single_row['maintenancedetails'] = "" if breakdown_obj[0].maintenancedetails==None else breakdown_obj[0].maintenancedetails
			dict_single_row['rdam'] = "" if breakdown_obj[0].rdam==None else breakdown_obj[0].rdam
			dict_single_row['technicianname'] = breakdown_obj[0].technicianname
			dict_single_row['complaints'] = breakdown_obj[0].complaints
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkOutgoing']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def outgoingUpdate(request): #itemdetails , service company updates pending........
	if request.method == 'POST':
		print request.body
		params = json.loads(request.body)
		outgoingid = params['outgoingid']
		healthstatus = params['healthstatus']
		itemdetails_id = params['itemdetailsid']
		remark = params['remark']
		company_id = params['companyid']
		returneddate = params['returneddate']
		receivercode = params['receivercode']
		breakdown_id = params['breakdownid']
		maintenance_details = params['maintenancedetails']
		technician = params['technician']
		complaint = params['complaint']
		#return HttpResponse("success")
		try:
			with transaction.atomic():
				itemchangedflag = False
				outgoing_obj = stkOutgoing.objects.filter(itemoutgoingid=outgoingid).select_related()
				if outgoing_obj[0].itemdetailsid_id != itemdetails_id: #if different then undo the old item and enter the new item
					print "different items"
					itemchangedflag = True
					itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=outgoing_obj[0].itemdetailsid_id)#details of item to replace
					#reload the old item's qty
					currentstatusvalue = itemdetails_obj[0].healthid_id
					oldstatusvalue = outgoing_obj[0].oldhealthstatusid_id
					if oldstatusvalue != 1: #if changing good item to bad
						if currentstatusvalue==1 and itemdetails_obj[0].issuedornot=='N':
							itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
							new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1
							itemmaster_obj.update(qtyavailable=new_qty)
							modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)

					if oldstatusvalue == 1: #if changing bad item to good
						if currentstatusvalue!=1 and itemdetails_obj[0].issuedornot=='N':
							itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
							new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
							itemmaster_obj.update(qtyavailable=new_qty)
							modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
					#undo item to its old state
					itemdetails_obj.update(healthid_id=outgoing_obj[0].oldhealthstatusid_id, currentstatusid_id=outgoing_obj[0].oldoriginalstatusid_id, itemoutgoingstatus='N', itemoutgoingid_id=None) #updating the details of item to be replaced
					
				#perform outgoing update, also record new item as outgoing if their is item change happen...
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id) #details of new item
				if itemchangedflag == True:
					outgoing_obj.update(remarks=remark, itemdetailsid_id=itemdetails_id, companyid_id=company_id, oldhealthstatusid_id=itemdetails_obj[0].healthid_id, currentstatusid_id=healthstatus, oldoriginalstatusid_id=itemdetails_obj[0].currentstatusid_id, datereturn=returneddate, itemreceiverid=receivercode)
				else:
					outgoing_obj.update(remarks=remark, itemdetailsid_id=itemdetails_id, companyid_id=company_id,  currentstatusid_id=healthstatus, datereturn=returneddate, itemreceiverid=receivercode)

				#update qty
				if healthstatus != 1: #if changing good item to bad
					if itemdetails_obj[0].healthid_id==1 and itemdetails_obj[0].issuedornot=='N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				if healthstatus == 1:
					if outgoing_obj[0].itemdetailsid.healthid_id != 1 and outgoing_obj[0].itemdetailsid.issuedornot == 'N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				itemdetails_obj.update(healthid_id=healthstatus, currentstatusid_id=4, itemoutgoingstatus='Y', itemoutgoingid_id=outgoing_obj[0].itemoutgoingid)
				#update breakdown maintenance data...
				breakdown_obj = stkBreakdown.objects.filter(breakdownid=breakdown_id)
				breakdown_obj.update(maintenancedetails=maintenance_details, rdam=returneddate, technicianname=technician, complaints=complaint, itemdetailsid_id=itemdetails_id, companyid_id=company_id)

				#check whether item is received after maintenence or not
				if returneddate!=None or receivercode!= "": #if least one is present then item received
					print "received after maintenance"
					itemdetails_obj.update(currentstatusid_id=5, itemoutgoingstatus='N')
				else:
					print "not received after maintenance"
					itemdetails_obj.update(currentstatusid_id=4, itemoutgoingstatus='Y')
				
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("failed")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def outgoingDelete(request): #breakdown data will be auto deleted because of foreign key constraint.
	if request.method == 'POST':
		params = json.loads(request.body)
		print request.body
		outgoingid = params['outgoingid']
		itemdetails_id = params['itemdetailsid']
		try:
			with transaction.atomic():
				outgoing_obj = stkOutgoing.objects.filter(itemoutgoingid=outgoingid).select_related()
				itemdetails_obj = stkItemDetails.objects.filter(itemdetailsid=itemdetails_id)
				#reload the item's old parameters, ie, status, qty etc...
				presentstatusvalue = itemdetails_obj[0].healthid_id
				oldstatusvalue = outgoing_obj[0].oldhealthstatusid_id
				if oldstatusvalue != 1: #if changing good item to bad
					if presentstatusvalue==1 and itemdetails_obj[0].issuedornot=='N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable - 1 #decrese 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)

				if oldstatusvalue == 1: #if changing bad item to good
					if presentstatusvalue!=1 and itemdetails_obj[0].issuedornot=='N':
						itemmaster_obj = stkItemMaster.objects.defer('maincatid_id','qtyavailable','modelid_id').filter(itemid=itemdetails_obj[0].itemid_id)
						new_qty = itemmaster_obj[0].qtyavailable + 1 #increase 1
						itemmaster_obj.update(qtyavailable=new_qty)
						modelmaster_obj = stkModelMaster.objects.filter(modelid=itemmaster_obj[0].modelid_id).update(qtyavailable=new_qty)
				#undo item to its old state
				itemdetails_obj.update(healthid_id=outgoing_obj[0].oldhealthstatusid_id, currentstatusid_id=outgoing_obj[0].oldoriginalstatusid_id, itemoutgoingstatus='N', itemoutgoingid_id=None) #updating the details of item to be replaced
				outgoing_obj.delete() #delete the outgoing record
				return HttpResponse("success")
		except ObjectDoesNotExist:#Exception as e
			return HttpResponse("This item can't be deleted.")
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def getHealthStatus(request):
	if 'POST' == 'POST':
		dict_full_content={}
		dict_single_row={}
		list_of_rows=[]
		healthstatus_obj = stkHealthStatus.objects.all()
		for healthstat in healthstatus_obj:
			dict_single_row['healthstatusid'] = healthstat.healthstatusid
			dict_single_row['healthstatusvalue'] = healthstat.healthstatusvalue
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkHealthStatus']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)
	else:
		return HttpResponse("Only post request is possible")

@csrf_protect
def serviceCompanyTableView(request):
	dict_full_content={}
	dict_single_row={}
	list_of_rows=[]
	if request.method == 'POST':
		company_obj = stkServiceCompany.objects.all()
		for company in company_obj:
			dict_single_row['companyid'] = company.companyid
			dict_single_row['companyname'] = company.companyname
			dict_single_row['mailid'] = company.mailid
			dict_single_row['phone'] = company.phone
			dict_single_row['address'] = company.address
			if stkOutgoing.objects.defer('companyid_id').filter(companyid_id=company.companyid).exists():
				dict_single_row['editable'] = False
			else:
				dict_single_row['editable'] = True
			list_of_rows.append(dict_single_row.copy())
		dict_full_content['stkServiceCompany']=list_of_rows
		response = JsonResponse(dict_full_content,safe=False)
		return HttpResponse(response.content)

@csrf_protect
def companySubmit(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		company_name = params['companyname']
		mail_id = params['mailid']
		phone_no = params['phone']
		addr = params['address']
		try:
			with transaction.atomic():
				company_obj = stkServiceCompany(companyname=company_name, mailid=mail_id, phone=phone_no, address=addr)
				company_obj.save()
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse("Mainstore Registration Failed.")
	else:
		return HttpResponse("Only post request is possible.")

@csrf_protect
def companyUpdate(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		company_id = params['companyid']
		company_name = params['companyname']
		mail_id = params['mailid']
		phone_no = params['phone']
		addr = params['address']
		try:
			with transaction.atomic():
				company_obj = stkServiceCompany.objects.filter(companyid=company_id).update(companyname=company_name, mailid=mail_id, phone=phone_no, address=addr)
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse("Mainstore Registration Failed.")
	else:
		return HttpResponse("Only post request is possible.")

@csrf_protect
def companyDelete(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		#print request.body
		company_id = params['companyid']
		try:
			with transaction.atomic():
				stkServiceCompany.objects.filter(companyid=company_id).delete()
				return HttpResponse("success")
		except Exception as e:
			return HttpResponse("Mainstore Registration Failed.")
	else:
		return HttpResponse("Only post request is possible.")

#reading excel sheets sample...
def readXls(request):
	try:
		excelfile = request.FILES['file']
		book = xlrd.open_workbook(file_contents=excelfile.read())
		for sheet_index in range(0, book.nsheets):
			sheet_obj = book.sheet_by_index(sheet_index)
			for row_id in range(1, sheet_obj.nrows):    # Iterate through rows
				#print ('-'*40)
				#print ('Row: %s' % row_idx)   # Print row number
				print(sheet_obj.row(row_id)[1].value)
				row_object_obj = stkSampleUpload(name=sheet_obj.row(row_id)[0].value, age=sheet_obj.row(row_id)[1].value, mark=sheet_obj.row(row_id)[2].value)
				row_object_obj.save()

				#for col_id in range(0, sheet_obj.ncols):  # Iterate through columns
				#	cell_obj = sheet_obj.cell(row_id, col_id)  # Get cell object by row, col
				#	print (cell_obj.value)
		student_obj = stkSampleUpload.objects.all()
		#json_students=json.loads(student_obj)
		#print json_items
		return render(request, 'stk/uploadResponse.html',{'headingdata':"ALL STUDENT DETAILS", 'json_students':student_obj})
		#return HttpResponse("success")
	except Exception as e:
		return render(request, 'stk/uploadResponseFailed.html',{'errordata':"UPLOAD FAILED"})

#show pdf in the category order
def itemRegistrationPreview2(request):
	dict_maincat_content={}
	dict_single_maincat_row={}
	list_of_maincat_rows=[]
	dict_subcat_content={}
	dict_single_subcat_row={}
	list_of_subcat_rows=[]
	dict_full_content={}
	json_items_var = request.GET.get('jsondata')
	headingdata = request.GET.get('headingdata')
	json_items=json.loads(json_items_var)
	itemid_arr = []
	for singleitem in json_items:
		itemid_arr.append(int(singleitem['item_id']))
	maincat_obj = stkMainCategory.objects.all()
	for maincat in maincat_obj:
		dict_single_maincat_row = {}
		list_of_maincat_rows = []
		subcat_obj = stkSubCategory.objects.filter(maincatid_id=maincat.maincatid)
		dict_subcat_content = {}
		for subcat in subcat_obj:
			dict_single_subcat_row = {}
			list_of_subcat_rows = []
			for item_id in itemid_arr:
				itemmaster_obj = stkItemMaster.objects.filter(maincatid_id=maincat.maincatid, itemid=item_id, subcatid_id=subcat.subcatid).select_related()
				if itemmaster_obj is None:
					break
				for item in itemmaster_obj:
					dict_single_subcat_row['itemid'] = item_id
					dict_single_subcat_row['brand_name'] = item.brandid.brandname
					dict_single_subcat_row['model_name'] = item.modelid.modelname
					#dict_single_subcat_row['maincat_name'] = item.maincatid.maincatname
					#dict_single_subcat_row['subcat_name'] = item.subcatid.subcatname
					dict_single_subcat_row['qty_available'] = item.qtyavailable
					dict_single_subcat_row['no_of_contents'] = item.totalnoofcontents
					dict_single_subcat_row['unit_name'] = item.unitid.unitname
					list_of_subcat_rows.append(dict_single_subcat_row.copy())
			if len(list_of_subcat_rows) == 0: #skip if no items for this subcategory
				continue
			#list_of_subcat_rows.append("subcatname":subcat.subcatname)
			dict_subcat_content[subcat.subcatname]=list_of_subcat_rows
			dict_subcat_content["subcatname"]=subcat.subcatname
		if len(dict_subcat_content) == 0:
			continue
		list_of_maincat_rows.append(dict_subcat_content.copy())
		#if len(list_of_maincat_rows) == 0:
		#	continue
		dict_maincat_content[maincat.maincatname]=list_of_maincat_rows
		dict_maincat_content["maincatname"]=maincat.maincatname
	response = JsonResponse(dict_maincat_content,safe=False)
	#return HttpResponse(response.content)
	return render(request, 'stk/itemRegistrationPreview2.html',{'headingdata':headingdata, 'json_items':response.content})

def itemRegistrationPreview3(request):
	json_items_var = request.GET.get('jsondata')
	headingdata = request.GET.get('headingdata')
	json_items=json.loads(json_items_var)
	#print json_items
	return render(request, 'stk/itemRegistrationPreview3.html',{'headingdata':headingdata, 'json_items':json_items})

#item Details generate pdf module...
def itemDetailsPdf(request):
	json_items_var = request.GET.get('json_items')
	json_items=json.loads(json_items_var)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Item Details '+ str(datetime.now().date()) + '.pdf"'
	doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
	doc.pagesize = landscape(A4)
	doc.font = ('Helvetica', 30)
	#doc.line = (480,747,580,747)	
	elements = []

	data = []
	data_row = []
	data_head_row = ["BRAND NAME","MODEL NAME","MAINCATEGORY","SUBCATEGORY","QTY","CONTENTS","UNIT"]
	data.append(data_head_row)

	for single_item in json_items:
		data_row.append(single_item["brand_name"])
		data_row.append(single_item["model_name"])
		data_row.append(single_item["maincat_name"])
		data_row.append(single_item["subcat_name"])
		data_row.append(single_item["qty_available"])
		data_row.append(single_item["no_of_contents"])
		data_row.append(single_item["unit_name"])

		data.append(data_row)
		data_row = [] #reinitialize after each iteration
		#print str(data)
				 
	#TODO: Get this line right instead of just copying it from the docs
	style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
		                   ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
		                   ('VALIGN',(0,0),(0,-1),'TOP'),
		                   ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
		                   ('ALIGN',(0,-1),(-1,-1),'CENTER'),
		                   ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
		                   ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
		                   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
		                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
		                   ])
	 
	#Configure style and word wrap
	s = getSampleStyleSheet()
	s = s["BodyText"]
	s.wordWrap = 'CJK'
	data2 = [[Paragraph(str(cell), s) for cell in row] for row in data]
	t=Table(data2)
	t.setStyle(style)
	 
	#Send the data and build the file
	centered = PS(name = 'centered',
    fontSize = 20,
    leading = 16,
    alignment = 1,
    spaceAfter = 20)

	elements.append(Paragraph('<h3>ALL REGISTERED ITEMS</h3>', centered))
	elements.append(t)
	doc.build(elements)
	return response












































from django.conf.urls import url
from . import views
import os
site_media = os.path.join(
    os.path.dirname(__file__), "../", "myApp", "static", 'site_media'
)
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
	url(r'^firmForLogin$', views.firmForLogin, name='firmForLogin'),
	url(r'^sampleurl$', views.sampleurl, name='sampleurl'),
	url(r'^adminHome$', views.adminHome, name='adminHome'),
	url(r'^selectStore$', views.selectStore, name='selectStore'),
	url(r'^confirmSelectedStore$', views.confirmSelectedStore, name='confirmSelectedStore'),
	url(r'^checkStoreSelected$', views.checkStoreSelected, name='checkStoreSelected'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^checkSession$', views.checkSession, name='checkSession'),

#firm registration...
	url(r'^firmReg$', views.firmReg, name='firmReg'),
	url(r'^firmRegistration$', views.firmRegistration, name='firmRegistration'),
	url(r'^firmUpdate$', views.firmUpdate, name='firmUpdate'),
	url(r'^firmDelete$', views.firmDelete, name='firmDelete'),

#mainstoreRegistration...
	url(r'^mainstoreRegistration$', views.mainstoreRegistration, name='mainstoreRegistration'),
	url(r'^loadFirm$', views.loadFirm, name='loadFirm'),
	url(r'^loadMainstores$', views.loadMainstores, name='loadMainstores'),
	url(r'^mainstoreSubmit$', views.mainstoreSubmit, name='mainstoreSubmit'),
	url(r'^mainstoreTableView$', views.mainstoreTableView, name='mainstoreTableView'),
	url(r'^storeUpdateParams$', views.storeUpdateParams, name='storeUpdateParams'),
	url(r'^updateMainstore$', views.updateMainstore, name='updateMainstore'),
	url(r'^deleteMainstore$', views.deleteMainstore, name='deleteMainstore'),

#connect Dept and store...
	url(r'^connectStoreDept$', views.connectStoreDept, name='connectStoreDept'),
	url(r'^connectStoreDeptSubmit$', views.connectStoreDeptSubmit, name='connectStoreDeptSubmit'),
	url(r'^connectStoreDeptTableView$', views.connectStoreDeptTableView, name='connectStoreDeptTableView'),
	url(r'^storeDeptUpdateParams$', views.storeDeptUpdateParams, name='storeDeptUpdateParams'),
	url(r'^updateStoreDeptConnection$', views.updateStoreDeptConnection, name='updateStoreDeptConnection'),
	url(r'^deleteStoreDeptConnection$', views.deleteStoreDeptConnection, name='deleteStoreDeptConnection'),


#location registration...
	url(r'^locationRegistration$', views.locationRegistration, name='locationRegistration'),
	url(r'^loadDeptInfo$', views.loadDeptInfo, name='loadDeptInfo'),
	url(r'^locationSubmit$', views.locationSubmit, name='locationSubmit'),
	url(r'^loadRegisteredDeptInfo$', views.loadRegisteredDeptInfo, name='loadRegisteredDeptInfo'),
	url(r'^locationTableView$', views.locationTableView, name='locationTableView'),
	url(r'^updateLocation$', views.updateLocation, name='updateLocation'),

#unit registration...
	url(r'^unitRegistration$', views.unitRegistration, name='unitRegistration'),
	url(r'^unitSubmit$', views.unitSubmit, name='unitSubmit'),
	url(r'^unitTableView$', views.unitTableView, name='unitTableView'),
	url(r'^updateUnit$', views.updateUnit, name='updateUnit'),

#sub category registration...
	url(r'^subCategoryRegistration$', views.subCategoryRegistration, name='subCategoryRegistration'),
	url(r'^loadMaincatInfo$', views.loadMaincatInfo, name='loadMaincatInfo'),
	url(r'^subCategorySubmit$', views.subCategorySubmit, name='subCategorySubmit'),
	url(r'^subcatTableView$', views.subcatTableView, name='subcatTableView'),
	url(r'^updateSubcat$', views.updateSubcat, name='updateSubcat'),

#item registration...
	url(r'^itemRegistration$', views.itemRegistration, name='itemRegistration'),
	url(r'^itemRegistrationParams$', views.itemRegistrationParams, name='itemRegistrationParams'),
	url(r'^itemModelForBrand$', views.itemModelForBrand, name='itemModelForBrand'),
	url(r'^itemSubmit$', views.itemSubmit, name='itemSubmit'),
	url(r'^brandsForMaincatId$', views.brandsForMaincatId, name='brandsForMaincatId'),
	url(r'^itemTableView$', views.itemTableView, name='itemTableView'),
	url(r'^itemUpdate$', views.itemUpdate, name='itemUpdate'),
	url(r'^itemDelete$', views.itemDelete, name='itemDelete'),

#supplier Registration...
	url(r'^supplierRegistration$', views.supplierRegistration, name='supplierRegistration'),
	url(r'^supplierSubmit$', views.supplierSubmit, name='supplierSubmit'),
	url(r'^supplierTableView$', views.supplierTableView, name='supplierTableView'),
	url(r'^supplierUpdate$', views.supplierUpdate, name='supplierUpdate'),
	url(r'^supplierDelete$', views.supplierDelete, name='supplierDelete'),
	url(r'^supplierParams$', views.supplierParams, name='supplierParams'),

#purchase...
	url(r'^purchase$', views.purchase, name='purchase'),
	url(r'^purchaseParams$', views.purchaseParams, name='purchaseParams'),
	url(r'^purchaseSubmit$', views.purchaseSubmit, name='purchaseSubmit'),
	url(r'^purchaseTableView$', views.purchaseTableView, name='purchaseTableView'),
	url(r'^purchaseUpdate$', views.purchaseUpdate, name='purchaseUpdate'),
	url(r'^purchaseDelete$', views.purchaseDelete, name='purchaseDelete'),

#issue...
	url(r'^issueItem$', views.issueItem, name='issueItem'),
	url(r'^issueParams$', views.issueParams, name='issueParams'),
	url(r'^loadLocations$', views.loadLocations, name='loadLocations'),
	url(r'^loadItemsForSubcatId$', views.loadItemsForSubcatId, name='loadItemsForSubcatId'),
	url(r'^issueSubmit$', views.issueSubmit, name='issueSubmit'),
	url(r'^issueTableView$', views.issueTableView, name='issueTableView'),
	url(r'^issueUpdate$', views.issueUpdate, name='issueUpdate'),
	url(r'^issueDelete$', views.issueDelete, name='issueDelete'),

#existing item registration...
	url(r'^existing$', views.existing, name='existing'),
	url(r'^existParams$', views.existParams, name='existParams'),
	url(r'^loadRemainingToAddItemsForSubcatId$', views.loadRemainingToAddItemsForSubcatId, name='loadRemainingToAddItemsForSubcatId'),
	url(r'^existSubmit$', views.existSubmit, name='existSubmit'),
	url(r'^existingTableView$', views.existingTableView, name='existingTableView'),
	url(r'^existUpdate$', views.existUpdate, name='existUpdate'),
	url(r'^existDelete$', views.existDelete, name='existDelete'),
	url(r'^itemRegistrationPreview$', views.itemRegistrationPreview, name='itemRegistrationPreview'),
	url(r'^itemRegistrationPreview2$', views.itemRegistrationPreview2, name='itemRegistrationPreview2'),
	url(r'^itemRegistrationPreview3$', views.itemRegistrationPreview3, name='itemRegistrationPreview3'),
	url(r'^itemDetailsPdf$', views.itemDetailsPdf, name='itemDetailsPdf'),

#purchase return...
	url(r'^purchaseReturn$', views.purchaseReturn, name='purchaseReturn'),
	url(r'^purchaseReturnParams$', views.purchaseReturnParams, name='purchaseReturnParams'),
	url(r'^loadItemsForPurReturnAutocomplete$', views.loadItemsForPurReturnAutocomplete, name='loadItemsForPurReturnAutocomplete'),
	url(r'^loadItemsForInvoice$', views.loadItemsForInvoice, name='loadItemsForInvoice'),
	url(r'^loadItemsForSupplierAndInvoice$', views.loadItemsForSupplierAndInvoice, name='loadItemsForSupplierAndInvoice'),
	url(r'^loadItemsForSupplierInvoiceAndItem$', views.loadItemsForSupplierInvoiceAndItem, name='loadItemsForSupplierInvoiceAndItem'),
	url(r'^purchaseReturnSubmit$', views.purchaseReturnSubmit, name='purchaseReturnSubmit'),
	url(r'^purchaseReturnTableView$', views.purchaseReturnTableView, name='purchaseReturnTableView'),
	url(r'^purchaseReturnDelete$', views.purchaseReturnDelete, name='purchaseReturnDelete'),
	url(r'^loadSupplierForInvoice$', views.loadSupplierForInvoice, name='loadSupplierForInvoice'),

#return from dept...
	url(r'^returnFromDept$', views.returnFromDept, name='returnFromDept'),
	url(r'^loadItemDetails$', views.loadItemDetails, name='loadItemDetails'),
	url(r'^loadRegisteredEmpCodes$', views.loadRegisteredEmpCodes, name='loadRegisteredEmpCodes'),
	url(r'^returnDeptSubmit$', views.returnDeptSubmit, name='returnDeptSubmit'),
	url(r'^returnDeptTableView$', views.returnDeptTableView, name='returnDeptTableView'),
	url(r'^returnDeptUpdate$', views.returnDeptUpdate, name='returnDeptUpdate'),
	url(r'^returnDeptDelete$', views.returnDeptDelete, name='returnDeptDelete'),

#outgoing items...
	url(r'^outgoing$', views.outgoing, name='outgoing'),
	url(r'^loadAllNonOutgoingItems$', views.loadAllNonOutgoingItems, name='loadAllNonOutgoingItems'),
	url(r'^loadServiceCompanies$', views.loadServiceCompanies, name='loadServiceCompanies'),
	url(r'^outgoingSubmit$', views.outgoingSubmit, name='outgoingSubmit'),
	url(r'^outgoingTableView$', views.outgoingTableView, name='outgoingTableView'),
	url(r'^outgoingUpdate$', views.outgoingUpdate, name='outgoingUpdate'),
	url(r'^outgoingDelete$', views.outgoingDelete, name='outgoingDelete'),
	url(r'^getHealthStatus$', views.getHealthStatus, name='getHealthStatus'),

#miscellaneous
	url(r'^miscellaneous$', views.miscellaneous, name='miscellaneous'),
	url(r'^serviceCompanyTableView$', views.serviceCompanyTableView, name='serviceCompanyTableView'),
	url(r'^companySubmit$', views.companySubmit, name='companySubmit'),
	url(r'^companyUpdate$', views.companyUpdate, name='companyUpdate'),
	url(r'^companyDelete$', views.companyDelete, name='companyDelete'),

	url(r'^test$', views.test, name='test'),
	url(r'^searchsample$', views.searchsample, name='searchsample'),
	url(r'^samplepurchase$', views.samplepurchase, name='samplepurchase'),
	url(r'^readXls$', views.readXls, name='readXls'),

]













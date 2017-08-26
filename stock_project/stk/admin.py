from django.contrib import admin
from stk.models import stkCompanyMaster,stkStoreMaster,stkDept,stkLocation,stkPrivilegeGroup,stkLogintab,stkPrivilegeDescription,stkUnits,stkMainCategory,stkSubCategory, stkBrandMaster,stkModelMaster,stkItemMaster, stkFirmAccess, stkSupplier, stkPurchaseMaster, stkPurchaseInfo, stkPurchaseOrder, stkServiceCompany, stkOutgoing, stkAssembled, stkIssue, stkIssueDetails,  stkItemDetails, stkWarrantyOrAmc, stkPurchaseReturn, stkPurchaseReturnDetails, stkReturnFromDept, stkHealthStatus, stkCurrentStatus, stkSampleUpload, stkBreakdown

# Register your models here.
admin.site.register(stkItemDetails)
admin.site.register(stkOutgoing)
admin.site.register(stkBreakdown)

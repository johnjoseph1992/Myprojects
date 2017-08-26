//outgoing items ctrl begin...
app.controller("outgoingCtrl", function($scope, $http, $rootScope, $window) {

	//$scope.statusarray = [{"value":"G","status":"GOOD"},{"value":"B","status":"DAMAGED"},{"value":"C","status":"COMPLAINT"}];
	$scope.healthstatusarray = [];
	$scope.all_emps = [];
	$scope.all_items = [];
	$scope.companies = [];
	$scope.all_outgoings = [];
	$scope.selectedOID = null;
	$scope.selectedoutgoing_obj = null;
	$scope.delButton = false;
	$scope.btnTxt = "Save";
	$scope.loadingPart = true;
	$scope.nodataPart = false;
	$scope.itemFetching = false;

	//checking whether store is selected...
	$http({
			method : "POST",
			url : "checkStoreSelected"
		}).then(function mySucces(response) {
			if(response.data[0].status == "success"){ //store already selected
				$rootScope.currentStore = response.data[0].storename; //show after refresh
			}
		}, function myError(response) {
		});//checking end...

	//detect ng-repeat finish...
	$scope.$on('ngRepeatFinished', function(ngRepeatFinishedEvent) { //worked when ng-repeat finished.(on-finish-render="ngRepeatFinished")
		$scope.loadingPart = false;
	});

	$scope.checkReturnDate = function(returndate){
		if(returndate=="")
			return "Not received"; //also a field sentstatus in tableview
		else
			return returndate;
	}

	//function load the table view...
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "outgoingTableView"
			}).then(function mySucces(response) {
				$scope.all_outgoings = response.data.stkOutgoing;
				if($scope.all_outgoings.length == 0){
					$scope.nodataPart = true;
					$scope.loadingPart = false;
					$scope.errorMsg = "No Records";
				}
			}, function myError(response) {
				$scope.nodataPart = true;
				$scope.loadingPart = false;
				$scope.errorMsg = "Something went wrong! "+response.status +" "+ response.statusText+" error occured";
		});
	}//loading table end...
	var start = performance.now();
	$scope.loadtabledata();
	var end = performance.now();
	console.log("Outgoing Loadtime :" + (end-start) + " milliseconds");

	$scope.clearClicked = function(){
		$scope.selectedItem=$scope.remarks_model=$scope.selectedCompany=$scope.new_servicecompanycheck=$scope.name_model=$scope.mail_model=$scope.phone_model=$scope.addr_model=$scope.returned_date_model=$scope.selectedEmp=$scope.technician_model=$scope.complaints_model=$scope.maintenance_details_model="";
		$scope.delButton = $scope.noCompanies = false;
		$scope.selectedOID=$scope.selectedoutgoing_obj = null;
		$scope.btnTxt = "Save";
		if(angular.isDefined($scope.status_model)){ //clearing the selection of current status select box
			delete $scope.status_model;
		}
	}

	//load dept data...
	$scope.loadInitParams = function(){
		$scope.itemFetching = true;
		$http({
				method : "POST",
				url : "loadAllNonOutgoingItems"
			}).then(function mySucces(response) {
				$scope.all_items = response.data.stkItemDetails;
				$scope.itemFetching = false;
				//$scope.companies = response.data.stkServiceCompany;
			}, function myError(response) {

		});

		$http({
				method : "POST",
				url : "loadRegisteredEmpCodes"
			}).then(function mySucces(response) {
				$scope.all_emps = response.data.allEmpCodes;
			}, function myError(response) {

		});

		$http({
				method : "POST",
				url : "loadServiceCompanies"
			}).then(function mySucces(response) {
				$scope.companies = response.data.stkServiceCompany;
			}, function myError(response) {

		});

		$http({
				method : "POST",
				url : "getHealthStatus"
			}).then(function mySucces(response) {
				$scope.healthstatusarray = response.data.stkHealthStatus;
			}, function myError(response) {

		});
	}
	$scope.loadInitParams();

	$scope.itemLostFocus = function(){
		$scope.noItems = false;
	}

	$scope.empLostFocus = function(){
		$scope.noEmps = false;
	}

	$scope.checkChanged = function(){
		$scope.name_model=$scope.mail_model=$scope.phone_model=$scope.addr_model="";
	}

	//submit function start...
	$scope.outgoingSubmit = function(){
		if($scope.delButton == false){ //if condition for submit...
			if($scope.new_servicecompanycheck == true){
				$scope.selectedCompany = {"companyname":"", "companyid":""};
			}
			else{
				if(typeof($scope.selectedCompany) != 'object' || $scope.selectedCompany.companyname=="" || $scope.selectedCompany.companyid==""){
					notifyMessage('fa fa-exclamation-triangle',"<b>Company required</b><br>Service company must be required.",'warning');
					return;
				}
				$scope.name_model=$scope.mail_model=$scope.phone_model=$scope.addr_model="";
			}

			$http({ //http submit start...
						method : "POST",
						url : "outgoingSubmit",
						data: {healthstatus:$scope.status_model, itemdetailsid:$scope.selectedItem.itemdetailsid, remark:$scope.remarks_model, companyid:$scope.selectedCompany.companyid, isnewcompany:$scope.new_servicecompanycheck, companyname:$scope.name_model, mailid:$scope.mail_model, phone:$scope.phone_model, address:$scope.addr_model, technician:$scope.technician_model, complaint:$scope.complaints_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.clearClicked();
							$scope.loadtabledata();
							$scope.loadInitParams();
						}
						else if(response.data == "companyexists"){
							notifyMessage('fa fa-exclamation-triangle',"<b>Company exists</b><br>Service company already existing.",'warning');
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
						}
					}, function myError(response) {

			}); //http submit end...
		} //if condition end
		else{ //condition for update...
			if($scope.returned_date_model=="" || $scope.returned_date_model==null || !angular.isDefined($scope.returned_date_model))
				$scope.returned_date_model = null;
			if(typeof($scope.selectedEmp) != 'object' || !angular.isDefined($scope.selectedEmp) || $scope.selectedEmp == null){
				//$scope.selectedEmp.empcode = "";
				$scope.receiverempcode = "";
			}
			else
				$scope.receiverempcode = $scope.selectedEmp.empcode;

			//if either returned date or receiver code is their then both of them must be present
			if($scope.returned_date_model == null && $scope.receiverempcode =="")
				console.log("Both null no problem");
			else if($scope.returned_date_model != null && $scope.receiverempcode !="")
				console.log("Both filled no problem");
			else{ //one is null and the other is filled
				notifyMessage('fa fa-exclamation-triangle',"<b>Fields Required</b><br>Received item must have received date and receiver.",'warning');
				return;
			}

			$http({ //http update start...
						method : "POST",
						url : "outgoingUpdate",
						data: {outgoingid:$scope.selectedoutgoing_obj.itemoutgoingid, healthstatus:$scope.status_model, itemdetailsid:$scope.selectedItem.itemdetailsid, remark:$scope.remarks_model, companyid:$scope.selectedCompany.companyid, returneddate:$scope.returned_date_model, receivercode:$scope.receiverempcode, breakdownid:$scope.selectedoutgoing_obj.breakdownid, maintenancedetails:$scope.maintenance_details_model, technician:$scope.technician_model, complaint:$scope.complaints_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
							$scope.clearClicked();
							$scope.loadtabledata();
							$scope.loadInitParams();
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
						}
					}, function myError(response) {

			}); //http update end...
		} //else end...
	} //submit function ends...

	$scope.outgoingTableRowClicked = function(outgoingobj){
		$scope.delButton = true;
		$scope.btnTxt = "Update";
		$scope.selectedoutgoing_obj = outgoingobj;
		$scope.selectedOID = outgoingobj.itemoutgoingid;
		$scope.selectedItem = {"itemdetailsid":outgoingobj.itemdetailsid,"itemname":outgoingobj.itemname,"fisatid":outgoingobj.fisatid};
		$scope.remarks_model = outgoingobj.remarks;
		$scope.status_model = outgoingobj.currentstatus //it is currentstatusid.
		$scope.selectedCompany = {"companyid":outgoingobj.companyid,"companyname":outgoingobj.companyname};
		$scope.returned_date_model = outgoingobj.datereturn;
		$scope.selectedEmp = {"empcode":outgoingobj.itemreceiverid};
		$scope.technician_model = outgoingobj.technicianname;
		$scope.complaints_model = outgoingobj.complaints;
		$scope.maintenance_details_model = outgoingobj.maintenancedetails;
	}

	$scope.outgoingDelete = function(){
		//notify user that you are deleting the record.
		if (confirm("You are going to cancel the entry.") == true) {
			console.log("pressed ok so execute delete.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}

		$http({
					method : "POST",
					url : "outgoingDelete",
					data: {outgoingid:$scope.selectedoutgoing_obj.itemoutgoingid, itemdetailsid:$scope.selectedoutgoing_obj.itemdetailsid}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Deleted Successfully.",'info');
						$scope.index = $scope.all_outgoings.indexOf($scope.selectedoutgoing_obj);
  						$scope.all_outgoings.splice($scope.index, 1);
						$scope.clearClicked();

					}
					else{
						notifyMessage('',"<b>Failed</b><br>Failed to delete data."+response.data,'danger');
					}
				}, function myError(response) {

		});
	}

	//custom filter start...
	$scope.customFilterForOutgoing = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['datedispatch','datereturn','itemsendername','itemname','companyname','fisatid','receivedstatus'];
		
	  return function (item) {
		if (!searchText) {
		  return true; // no filter
		}

		for (var i = 0; i < lookInKeys.length; i++) {
		  var key = lookInKeys[i];
		  if (comparator(item[key], searchText)) {
			return true; // if any key is match, return true
		  }
		}

		return false; // none of keys are match
	  };
	};
	//custom filter end...

});//supplier reg ctrl end...

























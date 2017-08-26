//return from dept ctrl begin...
app.controller("returnFromDeptCtrl", function($scope, $http, $rootScope, $window) {

	//$scope.statusarray = [{"value":"G","status":"GOOD"},{"value":"B","status":"DAMAGED"},{"value":"C","status":"COMPLAINT"}];
	$scope.healthstatusarray = [];
	$scope.depts = [];
	$scope.all_issueditems = [];
	$scope.selectedRID = null;
	$scope.selectedreturn_obj = null;
	$scope.delButton = false;
	$scope.btnTxt = "Return";
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

	//function load the table view...
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "returnDeptTableView"
			}).then(function mySucces(response) {
				$scope.all_returns = response.data.stkReturnFromDept;
				if($scope.all_returns.length == 0){
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
	console.log("ReturnFromDept Loadtime :" + (end-start) + " milliseconds");

	$scope.clearClicked = function(){
		$scope.selectedDept=$scope.selectedItem=$scope.remarks_model=$scope.selectedEmp=""
		$scope.selectedRID=$scope.selectedreturn_obj= null;
		$scope.delButton=false;
		$scope.btnTxt = "Return";
		if(angular.isDefined($scope.status_model)){ //clearing the selection of current status select box
			delete $scope.status_model;
		}
	}

	$scope.loadHealthStatus = function(){
		$http({
				method : "POST",
				url : "getHealthStatus"
			}).then(function mySucces(response) {
				$scope.healthstatusarray = response.data.stkHealthStatus;
			}, function myError(response) {

		});
	}
	$scope.loadHealthStatus();

	//load dept data...
	$scope.loadDepts = function(){
		$http({
					method : "POST",
					url : "loadRegisteredDeptInfo"
				}).then(function mySucces(response) {
					$scope.depts = response.data.hrmDepartment;
				}, function myError(response) {

			});
	}
	$scope.loadDepts();

	//load empcode data...
	$scope.loadEmps = function(){
		$http({
					method : "POST",
					url : "loadRegisteredEmpCodes"
				}).then(function mySucces(response) {
					$scope.all_emps = response.data.allEmpCodes;
				}, function myError(response) {

			});
	}
	$scope.loadEmps();



	//load issued items details when dept selection changed...
	$scope.deptSelectChanged = function(){
		$scope.selectedItem = "";
		$scope.itemFetching = true; //variable to show spinner when data is fetching
		$http({
					method : "POST",
					url : "loadItemDetails",
					data: {did:$scope.selectedDept.did}
				}).then(function mySucces(response) {
					$scope.all_issueditems = response.data.stkItemDetails;
					$scope.itemFetching = false;
				}, function myError(response) {

			});
	}

	$scope.deptLostFocus = function(){
		$scope.noDepts = false;
	}

	$scope.itemLostFocus = function(){
		$scope.noItems = false;
	}

	$scope.empLostFocus = function(){
		$scope.noEmps = false;
	}

	$scope.returnDeptSubmit = function(){
		if(!angular.isDefined($scope.remarks_model) || $scope.remarks_model==null || $scope.remarks_model=="")
			$scope.remarkvalue = "";
		else
			$scope.remarkvalue = $scope.remarks_model;
		if($scope.delButton == false){ //condition for returnDeptSubmit..if-else start...
			$http({ //http submit start...
						method : "POST",
						url : "returnDeptSubmit",
						data: {did:$scope.selectedDept.did, itemdetailsid:$scope.selectedItem.itemdetailsid, remark:$scope.remarkvalue, returnedby:$scope.selectedEmp.empcode, status:$scope.status_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							/*$scope.delButton = false;
							for (var i = 0; i < response.data.length; i++){ //multiple rows are returned from django
								$scope.list_row_to_push = {
								  	'itemdetailsid': response.data[i].itemdetailsid,
								  	'warrantyto': response.data[i].warrantyto,		  
								};
								$scope.all_existing.push($scope.list_row_to_push);
							}
							$scope.loadInitParams();*/
							$scope.clearClicked();
							$scope.loadtabledata();
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data[0].data,'danger');
						}
					}, function myError(response) {

			}); //http submit end...
		}else{ //condition for update..
			alert();
			$http({ //http start...
						method : "POST",
						url : "returnDeptUpdate",
						data: {returnid:$scope.selectedreturn_obj.returnid, did:$scope.selectedDept.did, itemdetailsid:$scope.selectedItem.itemdetailsid, remark:$scope.remarkvalue, returnedby:$scope.selectedEmp.empcode, status:$scope.status_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
							$scope.clearClicked();
							$scope.loadtabledata();
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data[0].data,'danger');
						}
					}, function myError(response) {

			}); //http end...
		} //if-else end...
	}

	$scope.returnDeptTableRowClicked = function(return_obj){
		$scope.delButton = true;
		$scope.btnTxt = "Update";
		$scope.selectedRID = return_obj.returnid;
		$scope.selectedreturn_obj = return_obj;
		$scope.remarks_model = return_obj.remarks;
		$scope.status_model = return_obj.health;
		for (var i = 0; i < $scope.depts.length; i++) { //the object corresponds to the did is assigned to typeahead
  			if($scope.depts[i].did == return_obj.fromdeptid){
				$scope.selectedDept = $scope.depts[i];
				break;
			}
		}

		for (var i = 0; i < $scope.all_emps.length; i++) { //the object corresponds to the did is assigned to typeahead
  			if($scope.all_emps[i].empcode == return_obj.returnedbyid){
				$scope.selectedEmp = $scope.all_emps[i];
				break;
			}
		}
		
		//to load issued items corresponding to the dept
		$scope.itemFetching = true; //variable to show spinner when data is fetching
		$http({
					method : "POST",
					url : "loadItemDetails",
					data: {did:return_obj.fromdeptid/*$scope.selectedDept.did*/}
				}).then(function mySucces(response) {
					$scope.all_issueditems = response.data.stkItemDetails;
					$scope.itemFetching = false;
					$scope.selectedItem = {"fisatid":return_obj.fisatid,"itemname":return_obj.itemname,"itemdetailsid":return_obj.itemdetailsid};
					//$scope.selectedItem = return_obj.fisatid+" ("+return_obj.itemname+")"; //returned items not in the autocompletebox so just typed it
				}, function myError(response) {

			});
		
	}

	$scope.returnDeptDelete = function(){
		//notify user that you are deleting the record.
		if (confirm("You are going to cancel the return entry.") == true) {
			console.log("pressed ok so execute delete.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}

		$http({
					method : "POST",
					url : "returnDeptDelete",
					data: {returnid:$scope.selectedreturn_obj.returnid}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Deleted Successfully.",'info');
						$scope.index = $scope.all_returns.indexOf($scope.selectedreturn_obj);
  						$scope.all_returns.splice($scope.index, 1);
						$scope.clearClicked();

					}
					else{
						notifyMessage('',"<b>Failed</b><br>Failed to delete data."+response.data,'danger');
					}
				}, function myError(response) {

		});
	}

	//custom filter start...
	$scope.customFilterForReturnDept = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['returndate','itemname','fromdeptname','fromlocationname','returnedbyname','fisatid'];
		
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

























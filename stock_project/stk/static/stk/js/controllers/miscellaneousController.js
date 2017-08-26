//existing item reg ctrl begin...
app.controller("miscellaneousCtrl", function($scope, $http, $rootScope, $window) {

	$scope.alloptions = [{"optionid":1, "optionname":"Service company"}, {"optionid":"2", "optionname":"Item details"}, {"optionid":"3", "optionname":"Sample option"}, {"optionid":4, "optionname":"Service company"}, {"optionid":"5", "optionname":"Item details"}, {"optionid":"6", "optionname":"Sample option"}];
	$scope.clickedOptionid = 1;
	$scope.fadeintrial = false;
	$scope.companies = [];
	$scope.selectedCID = null;
	$scope.companyDelButton = false;
	$scope.companyBtnTxt = "Save";
	$scope.selectedcompany_obj = null;

	$scope.tabClicked = function(optionobj){
		$scope.clickedOptionid = optionobj.optionid;
	}

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
	$scope.$on('preturnNgRepeatFinished', function(ngRepeatFinishedEvent) { //worked when ng-repeat finished.(on-finish-render="..ngRepeatFinished")
		$scope.loadingPart = false;
	});

	//function load the table view...
	$scope.loadservicecompanytabledata = function(){
		$http({
				method : "POST",
				url : "serviceCompanyTableView"
			}).then(function mySucces(response) {
				$scope.companies = response.data.stkServiceCompany;
				/*if($scope.all_preturns.length == 0){
					$scope.nodataPart = true;
					$scope.loadingPart = false;
					$scope.errorMsg = "No Records";
				}*/
			}, function myError(response) {
				/*$scope.nodataPart = true;
				$scope.loadingPart = false;*/
				$scope.errorMsg = "Something went wrong! "+response.status +" "+ response.statusText+" error occured";
		});
	}//loading table end...
	$scope.loadservicecompanytabledata();

	$scope.companyClearClicked = function(){
		$scope.name_model=$scope.mail_model=$scope.phone_model=$scope.addr_model="";
		$scope.selectedCID = null;
		$scope.companyDelButton = false;
		$scope.companyBtnTxt = "Save";
		$scope.selectedcompany_obj = null;
	}

	//submit function...
	$scope.companySubmit = function(){
		if($scope.companyDelButton == false){ //if for submit start
			$http({
						method : "POST",
						url : "companySubmit",
						data: {companyname:$scope.name_model, mailid:$scope.mail_model, phone:$scope.phone_model, address:$scope.addr_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.loadservicecompanytabledata();
							$scope.companyClearClicked();
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
						}
					}, function myError(response) {

			});
		} //if for submit end
		else{ //else for update condition start
			$http({
						method : "POST",
						url : "companyUpdate",
						data: {companyid:$scope.selectedcompany_obj.companyid, companyname:$scope.name_model, mailid:$scope.mail_model, phone:$scope.phone_model, address:$scope.addr_model}
					}).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.loadservicecompanytabledata();
							$scope.companyClearClicked();
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
						}
					}, function myError(response) {

			});
		} //else for update condition start
	}

	$scope.companyTableRowClicked = function(company_obj){
		//$scope.selectedCID = company_obj.companyid;
	}

	$scope.editCompanyClicked = function(company_obj){
		$scope.selectedCID = company_obj.companyid;
		$scope.companyDelButton = true;
		$scope.companyBtnTxt = "Update";
		$scope.selectedcompany_obj = company_obj;
		$scope.name_model = company_obj.companyname;
		$scope.mail_model = company_obj.mailid;
		$scope.phone_model = parseInt(company_obj.phone);
		$scope.addr_model = company_obj.address;
	}

	$scope.companyDelete = function(preturn_obj){

		$http({ //http start
					method : "POST",
					url : "companyDelete",
					data: {companyid:$scope.selectedcompany_obj.companyid}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Deleted Successfully.",'info');
						$scope.index = $scope.companies.indexOf($scope.selectedcompany_obj);
						$scope.companies.splice($scope.index, 1);
						$scope.companyClearClicked();
					}
					else{
						notifyMessage('',"<b>Failed</b><br>Failed to delete data."+response.data,'danger');
					}
				}, function myError(response) {

		}); //http end
	} //purchase return delete function end
	
	//custom filter start...
	$scope.customFilterForCompany = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['companyname','mailid','phone','address'];
		
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

























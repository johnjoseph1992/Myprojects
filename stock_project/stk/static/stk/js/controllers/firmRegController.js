//firm reg ctrl begin...
		app.controller("firmRegCtrl", function($scope, $http) {
			$scope.all_firms = [];
			$scope.edit_data = [];
			$scope.temp_firm_name = "";

			//function load the table with firm names...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "loadFirm"
					}).then(function mySucces(response) {
						$scope.all_firms = response.data.stkCompanyMaster;
						for (var i = 0; i < $scope.all_firms.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_firms[i].firmid] = false;
						}
					}, function myError(response) {

					});
			}//loading table end...
			$scope.loadtabledata(); //call for initial loading	
	
			$scope.checkeditable = function(firm_obj){
				if(firm_obj.editable == 'false')
					return true;
			}

			$scope.modifyfirm = function(firm_obj){                             //for edit options
				$scope.temp_firm_name = firm_obj.firmname;
				if(firm_obj.editable == 'true')
					$scope.edit_data[firm_obj.firmid] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}
			}

			$scope.stopmodifyfirm = function(firm_obj){                         //for edit options
				firm_obj.firmname = $scope.temp_firm_name;
				$scope.edit_data[firm_obj.firmid] = false; //visibility
			}

			$scope.firmupdate = function(firm_obj){                             //for edit options
				$http({
					method : "POST",
					url : "firmUpdate",
					params: {firm_name: firm_obj.firmname, firm_id: firm_obj.firmid}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Firm Updated Successfully.",'info');
							$scope.edit_data[firm_obj.firmid] = false; //visibility
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to update.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}

			$scope.firmdelete = function(firm_obj){
				$http({
					method : "POST",
					url : "firmDelete",
					params: {firm_id: firm_obj.firmid}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Firm Deleted Successfully.",'info');
							$scope.stopmodifyfirm(firm_obj);
							$scope.index = $scope.all_firms.indexOf(firm_obj);
  							$scope.all_firms.splice($scope.index, 1);
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to delete.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}

			//submiting a new firm...
			$scope.firmSubmit = function(){
				$http({
					method : "POST",
					url : "firmRegistration",
					params: {firm_name: $scope.firm_submit_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.loadtabledata(); //reload table after submit a new row
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}


		});//firm reg ctrl end...

























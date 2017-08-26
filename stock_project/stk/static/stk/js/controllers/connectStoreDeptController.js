//connect dept store ctrl begin...
		app.controller("connectStoreDeptCtrl", function($scope, $http) {
	
			$scope.edit_data = [];
			$scope.depts = [];
			$scope.temp_store_name = "";

			//load the selectbox with department names...
			$http({
					method : "POST",
					url : "loadDeptInfo"
				}).then(function mySucces(response) {
					$scope.depts = response.data.hrmDepartment;
				}, function myError(response) {

				});//loading selectbox end...	

			//load the selectbox store names...
			$http({
					method : "POST",
					url : "loadMainstores"
				}).then(function mySucces(response) {
					$scope.all_stores = response.data.stkStoreMaster;
					//dont want independent store with storeid 0 here. so removing it...
					for(var i=0 ; i<$scope.all_stores.length; i++){
						if($scope.all_stores[i].storeid== "0")
							$scope.all_stores.splice(i);
					}
				}, function myError(response) {

				});//loading selectbox end...

			//function load data to table...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "connectStoreDeptTableView"
					}).then(function mySucces(response) {
						$scope.all_store_dept_data = response.data.stkStoreDeptData;
						for (var i = 0; i < $scope.all_store_dept_data.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_store_dept_data[i].dept_id] = false;
						}
					}, function myError(response) {

					});
			}//function loading table end...
			$scope.loadtabledata();	 //call for initial loading

			$scope.checkeditable = function(connect_store_dept_obj){
				if(connect_store_dept_obj.editable == 'false')
					return true;
			}

			//edit rows...
			$scope.modifyrecord = function(connect_store_dept_obj){                             //for edit options
				$scope.temp_store_name = connect_store_dept_obj.mainstore_name;
				//$scope.edit_data[connect_store_dept_obj.dept_id] = true;
				if(connect_store_dept_obj.editable == 'true')
					$scope.edit_data[connect_store_dept_obj.dept_id] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}
			}

			$scope.stopmodifyrecord = function(connect_store_dept_obj){                         //for edit options
				connect_store_dept_obj.mainstore_name = $scope.temp_store_name;
				$scope.edit_data[connect_store_dept_obj.dept_id] = false;  //visibility
			}

			//update store dept connection...
			$scope.recordupdate = function(connect_store_dept_obj){
				$http({
					method : "POST",
					url : "storeDeptUpdateParams",
					params: {store_id:connect_store_dept_obj.store_id}

				  }).then(function mySucces(response) {
						connect_store_dept_obj.mainstore_name = response.data;
						//if its a success then perform update...
						$http({
							method : "POST",
							url : "updateStoreDeptConnection",
							params: {dept_id:connect_store_dept_obj.dept_id, store_id:connect_store_dept_obj.store_id}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Dept and Store Connection Updated Successfully.",'info');
									$scope.edit_data[connect_store_dept_obj.dept_id] = false;//change visibility
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to update.",'danger');
								}
							}, function myError(response) {
							 // $scope.myResponse = response.statusText;
						});
					}, function myError(response) {
				});
			}

			$scope.recorddelete = function(connect_store_dept_obj){
				$http({
							method : "POST",
							url : "deleteStoreDeptConnection",
							params: {dept_id:connect_store_dept_obj.dept_id}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Store - Department Connection Deleted Successfully.",'info');
									$scope.stopmodifyrecord(connect_store_dept_obj);
									$scope.index = $scope.all_store_dept_data.indexOf(connect_store_dept_obj); //delete item from table view
  									$scope.all_store_dept_data.splice($scope.index, 1);
									//add deleted item back to dept selectbox...
									$scope.list_row_to_push = {
									  'did': connect_store_dept_obj.dept_id,
									  'department_name': connect_store_dept_obj.department_name,
									};
									$scope.depts.push($scope.list_row_to_push);
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to delete.",'danger');
								}
							}, function myError(response) {
							 // $scope.myResponse = response.statusText;
					});
			}

			
			//custom filter start...
			$scope.customFilter = function (searchText) {
			  function comparator(a, b) {
				return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
			  }

			  var lookInKeys = ['department_name', 'mainstore_name'];

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


			//connecting store and dept...
			$scope.connectDeptStoreSubmit = function(){
				$http({
					method : "POST",
					url : "connectStoreDeptSubmit",
					params: {dept_id: $scope.dept_select_model, store_id:$scope.store_select_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.loadtabledata(); //load after adding new row
						}
						else{
							notifyMessage('',"<b>Failed</b><br>"+response.data+"Failed to save data.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}


		});//connect dept store ctrl end...

























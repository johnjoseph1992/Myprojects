//location reg ctrl begin...
		app.controller("locationRegCtrl", function($scope, $http) {

			$scope.edit_data = [];
			$scope.temp_loc_name = "";
			$scope.temp_dept_name = "";

			//load the selectbox with dependent firm names...
			$http({
					method : "POST",
					url : "loadRegisteredDeptInfo"
				}).then(function mySucces(response) {
					$scope.depts = response.data.hrmDepartment;
				}, function myError(response) {

				});//loading selectbox end...	

			//function load data to table...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "locationTableView"
					}).then(function mySucces(response) {
						$scope.all_locations = response.data.stkLocation;
						for (var i = 0; i < $scope.all_locations.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_locations[i].location_id] = false;
						}
					}, function myError(response) {

					});
			}//function loading table end...
			$scope.loadtabledata();	 //call for initial loading

			
			//edit rows...
			$scope.modifyrecord = function(location_obj){                             //for edit options
				$scope.temp_loc_name = location_obj.location_name;
				$scope.temp_dept_name = location_obj.department_name;
				$scope.edit_data[location_obj.location_id] = true;
				/*if(connect_store_dept_obj.editable == 'true')
					$scope.edit_data[connect_store_dept_obj.dept_id] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}*/
			}

			$scope.stopmodifyrecord = function(location_obj){                         //for edit options
				location_obj.location_name = $scope.temp_loc_name;
				location_obj.department_name = $scope.temp_dept_name;
				$scope.edit_data[location_obj.location_id] = false;
			}

			//update store dept connection...
			$scope.updaterecord = function(location_obj){
				$http({
					method : "POST",
					url : "updateLocation",
					params: {location_id:location_obj.location_id, location_name:location_obj.location_name, dept_id:location_obj.dept_id}

				  }).then(function mySucces(response) {
						if(response.data[0].status == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Location Updated Successfully.",'info');
							location_obj.department_name = response.data[0].department_name;
							$scope.edit_data[location_obj.location_id] = false;
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to update.",'danger');
						}
					}, function myError(response) {
				});
			}

			//custom filter start...
			$scope.customFilter = function (searchText) {
			  function comparator(a, b) {
				return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
			  }

			  var lookInKeys = ['department_name', 'location_name'];

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

			//submiting a new location...
			$scope.locationSubmit = function(){
				$http({
					method : "POST",
					url : "locationSubmit",
					params: {location_name: $scope.location_name_model, dept_id:$scope.dept_select_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Location Added Successfully.",'info');
							$scope.loadtabledata(); //load after adding new row
						}
						else{
							notifyMessage('',"<b>Failed</b><br>"+response.data+"Failed to save data.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}


		});//location reg ctrl end...

























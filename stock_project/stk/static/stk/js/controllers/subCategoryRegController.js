//ctrl begin...
		app.controller("subCategoryRegCtrl", function($scope, $http) {

			$scope.edit_data = [];
			$scope.temp_subcat_name = "";
			$scope.temp_maincat_name = "";

			//load the selectbox with dependent firm names...
			$http({
					method : "POST",
					url : "loadMaincatInfo"
				}).then(function mySucces(response) {
					$scope.maincats = response.data.stkMainCategory;
				}, function myError(response) {

				});//loading selectbox end...	

			//function load data to table...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "subcatTableView"
					}).then(function mySucces(response) {
						$scope.all_subcat = response.data.stkSubCategory;
						for (var i = 0; i < $scope.all_subcat.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_subcat[i].subcat_id] = false;
						}
					}, function myError(response) {

					});
			}//function loading table end...
			$scope.loadtabledata();	 //call for initial loading

			//edit rows...
			$scope.modifyrecord = function(subcat_obj){                             //for edit options
				$scope.temp_subcat_name = subcat_obj.subcat_name;
				$scope.temp_maincat_name = subcat_obj.maincat_name;
				$scope.edit_data[subcat_obj.subcat_id] = true;
				/*if(connect_store_dept_obj.editable == 'true')
					$scope.edit_data[connect_store_dept_obj.dept_id] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}*/
			}

			$scope.stopmodifyrecord = function(subcat_obj){                         //for edit options
				subcat_obj.subcat_name = $scope.temp_subcat_name;
				subcat_obj.maincat_name = $scope.temp_maincat_name;
				$scope.edit_data[subcat_obj.subcat_id] = false; //visibility
			}

			//update store dept connection...
			$scope.updaterecord = function(subcat_obj){
				$http({
					method : "POST",
					url : "updateSubcat",
					params: {subcat_id:subcat_obj.subcat_id, subcat_name:subcat_obj.subcat_name, maincat_id:subcat_obj.maincat_id}

				  }).then(function mySucces(response) {
						if(response.data[0].status == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Subcategory Updated Successfully.",'info');
							subcat_obj.maincat_name = response.data[0].maincat_name;
							$scope.edit_data[subcat_obj.subcat_id] = false;
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

			  var lookInKeys = ['subcat_name', 'maincat_name'];

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
			$scope.subCategorySubmit = function(){
				$http({
					method : "POST",
					url : "subCategorySubmit",
					params: {subcat_name: $scope.subcat_name_model, maincat_id:$scope.maincat_select_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
							$scope.loadtabledata(); //reload table view
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}

			//clear button clicked...
			$scope.clearClicked = function(){
				$scope.subcat_name_model="";
				$scope.frmSubcat.$setPristine();
				$scope.frmSubcat.$setUntouched();
				if(angular.isDefined($scope.maincat_select_model)){ //clearing the selection of maincat select box
				    delete $scope.maincat_select_model;
				}
			}


		});//ctrl end...

























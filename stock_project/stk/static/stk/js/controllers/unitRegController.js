//unit reg ctrl begin...
		app.controller("unitRegCtrl", function($scope, $http) {

			$scope.edit_data = [];
			$scope.temp_unit_name = "";
			$scope.temp_nos_contents = 0;

			//function load data to table...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "unitTableView"
					}).then(function mySucces(response) {
						$scope.all_units = response.data.stkUnits;
						for (var i = 0; i < $scope.all_units.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_units[i].unit_id] = false;
						}
					}, function myError(response) {

					});
			}//function loading table end...
			$scope.loadtabledata();	 //call for initial loading

			$scope.checkContents = function(content_value){
				if(content_value == (0 || null))
					return "NA";
				else
					return content_value;
			}

			//edit rows...
			$scope.modifyrecord = function(unit_obj){                             //for edit options
				//temporarly storing the data before making changes...
				$scope.temp_unit_name = unit_obj.unit_name;
				$scope.temp_nos_contents = unit_obj.no_of_contents;
				$scope.edit_data[unit_obj.unit_id] = true;//change visibility
				/*if(unit_obj.editable == 'true')
					$scope.edit_data[unit_obj.unit_id] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}*/
			}

			$scope.stopmodifyrecord = function(unit_obj){                         //for edit options
				//restoring the temporary stored data...
				unit_obj.unit_name = $scope.temp_unit_name;
				unit_obj.no_of_contents = $scope.temp_nos_contents;
				$scope.edit_data[unit_obj.unit_id] = false;//change visibility
			}

			//update unit...
			$scope.updaterecord = function(unit_obj){
				$http({
					method : "POST",
					url : "updateUnit",
					params: {unit_id:unit_obj.unit_id, unit_name:unit_obj.unit_name, nos_contents:unit_obj.no_of_contents}

				  }).then(function mySucces(response) {
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Unit Updated Successfully.",'info');
							$scope.edit_data[unit_obj.unit_id] = false;//change visibility
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to update.",'danger');
						}
					}, function myError(response) {
				});
			}

			//clear button clicked...
			$scope.clearClicked = function(){
				$scope.frmUnit.$setPristine();
				$scope.frmUnit.$setUntouched(); //Angularjs function set error states to default
				$scope.unit_name_model=$scope.no_of_contents_model="";
			}

			//custom filter start...
			$scope.customFilter = function (searchText) {
			  function comparator(a, b) {
				return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
			  }

			  var lookInKeys = ['unit_name', 'no_of_contents'];

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

			//submiting a new unit...
			$scope.unitSubmit = function(){
				$http({
					method : "POST",
					url : "unitSubmit",
					params: {unit_name: $scope.unit_name_model, no_of_contents:$scope.no_of_contents_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Unit Added Successfully.",'info');
							$scope.loadtabledata(); //load after adding new row
						}
						else{
							notifyMessage('',"<b>Failed</b><br>"+response.data+"Failed to save data.",'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}


		});//unit reg ctrl end...

























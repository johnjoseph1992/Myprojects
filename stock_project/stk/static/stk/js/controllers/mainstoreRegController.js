//mainstore reg ctrl begin...
		app.controller("mainstoreRegCtrl", function($scope, $http) {

			$scope.edit_data = [];
			$scope.temp_store_name = "";
			$scope.temp_firm_name = "";
			$scope.temp_understore_name = "";

			//load the selectbox with dependent firm names...
			$http({
					method : "POST",
					url : "loadFirm"
				}).then(function mySucces(response) {
					$scope.firms = response.data.stkCompanyMaster;
				}, function myError(response) {

				});//loading selectbox end...	

			//load the selectbox store names...
			$http({
					method : "POST",
					url : "loadMainstores"
				}).then(function mySucces(response) {
					$scope.under_stores = response.data.stkStoreMaster;
				}, function myError(response) {

				});//loading selectbox end...	

			//function load data to table...
			$scope.loadtabledata = function(){
				$http({
						method : "POST",
						url : "mainstoreTableView"
					}).then(function mySucces(response) {
						$scope.all_storedata = response.data.stkStoreMaster;
						for (var i = 0; i < $scope.all_storedata.length; i++) {         //for edit options
				  			$scope.edit_data[$scope.all_storedata[i].storeid] = false;
						}
					}, function myError(response) {

					});
			}//function loading table end...	
			$scope.loadtabledata(); //call for initial loading

			$scope.checkeditable = function(store_obj){
				if(store_obj.editable == 'false')
					return true;
			}

			//edit rows...
			$scope.modifystore = function(store_obj){                             //for edit options
				$scope.temp_store_name = store_obj.mainstorename;
				$scope.temp_firm_name = store_obj.firmname;
				$scope.temp_understore_name = store_obj.understorename;
				//$scope.edit_data[store_obj.storeid] = true;
				if(store_obj.editable == 'true')
					$scope.edit_data[store_obj.storeid] = true;
				else{
					notifyMessage('fa fa-exclamation-triangle',"<b>Locked Record</b><br>This record have dependent entries. It cannot be edited.",'warning');
				}
			}

			$scope.stopmodifystore = function(store_obj){                         //for edit options
				store_obj.mainstorename = $scope.temp_store_name;
				store_obj.firmname = $scope.temp_firm_name;
				store_obj.understorename = $scope.temp_understore_name;
				$scope.edit_data[store_obj.storeid] = false; //visibility
			}

			$scope.storeupdate = function(store_obj){
				$http({
					method : "POST",
					url : "storeUpdateParams",
					params: {firm_id: store_obj.firmid,understore_id:store_obj.understoreid}

				  }).then(function mySucces(response) {
					 	//set values back to table view
						store_obj.firmname = response.data[0].firm_name
						store_obj.understorename = response.data[0].understore_name
						//alert(store_obj.understorename);
						//if its a success then perform update...
						$http({
							method : "POST",
							url : "updateMainstore",
							params: {store_id:store_obj.storeid, mainstore_name:store_obj.mainstorename, firm_id:store_obj.firmid, understore_id:store_obj.understoreid}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Mainstore Updated Successfully.",'info');
									$scope.edit_data[store_obj.storeid] = false; //visibility
									for(var i=0 ; i<$scope.under_stores.length; i++){
										if($scope.under_stores[i].storeid == store_obj.storeid)
											$scope.under_stores[i].mainstorename = store_obj.mainstorename;
									}
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

			$scope.storedelete = function(store_obj){
				$http({
							method : "POST",
							url : "deleteMainstore",
							params: {store_id:store_obj.storeid}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Mainstore Deleted Successfully.",'info');
									$scope.stopmodifystore(store_obj);
									$scope.index = $scope.all_storedata.indexOf(store_obj);
  									$scope.all_storedata.splice($scope.index, 1);  //remove this entry from table view
									//remove deleted store from underwhichstore selectbox [registration phase also]...
									for(var i=0 ; i<$scope.under_stores.length; i++){
										if($scope.under_stores[i].storeid == store_obj.storeid)
											$scope.under_stores.splice(i);
									}
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

			  var lookInKeys = ['mainstorename', 'understorename'];

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


			//submiting a new mainstore...
			$scope.mainstoreSubmit = function(){
				$http({
					method : "POST",
					url : "mainstoreSubmit",
					params: {main_store_name: $scope.mainstore_name_model, firm_id:$scope.firm_select_model, under_which_store:$scope.under_store_select_model}

				  }).then(function mySucces(response) {
					 // $scope.myResponse = response.data;
						if(response.data == "success"){
							notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');

							//load the selectbox store names...
							$http({
									method : "POST",
									url : "loadMainstores"
								}).then(function mySucces(response) {
									$scope.under_stores = response.data.stkStoreMaster;
								}, function myError(response) {

								});//loading selectbox end...

							$scope.loadtabledata(); //refresh table after adding a row	
						}
						else{
							notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
						}
					}, function myError(response) {
					 // $scope.myResponse = response.statusText;
				});
			}


		});//mainstore reg ctrl end...

























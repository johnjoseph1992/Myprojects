//supplier reg ctrl begin...
app.controller("supplierRegCtrl", function($scope, $http, $rootScope, $window) {

	$scope.selectedID = null;
	$scope.delButton = false;
	$scope.btnTxt = "Save";
	$scope.all_suppliers = [];

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

	//load autocomplete data...
	$http({
				method : "POST",
				url : "supplierParams"
			}).then(function mySucces(response) {
				$scope.all_states = response.data.supplierStates;
				$scope.all_countries = response.data.supplierCountries;
				$scope.all_cities = response.data.supplierCities;
				$scope.all_districts = response.data.supplierDistricts;
			}, function myError(response) {

		});

	//function load the table view...
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "supplierTableView"
			}).then(function mySucces(response) {
				$scope.all_suppliers = response.data.stkSupplier;
			}, function myError(response) {

		});
	}//loading table end...
	var start = performance.now();
	$scope.loadtabledata();
	var end = performance.now();
	console.log("Supplier loadtime: " + (end-start) + " milliseconds");

	//function to clear all controls to default values...
	$scope.clearAll = function(){
		$scope.selected_supplier_id=$scope.sup_name_model=$scope.sup_addr_model=$scope.sup_city_model=$scope.sup_district_model=$scope.sup_state_model=$scope.sup_country_model=$scope.sup_mail_model=$scope.sup_phone_model=$scope.sup_vat_model="";
	}	

	//function for submitting the supplier...
	$scope.supplierSubmit = function(){
		if($scope.delButton == false){ //for supplier submit
			$http({
							method : "POST",
							url : "supplierSubmit",
							data: {supplier_name:$scope.sup_name_model, address:$scope.sup_addr_model, city:$scope.sup_city_model, district:$scope.sup_district_model, state:$scope.sup_state_model, country:$scope.sup_country_model, mail_id:$scope.sup_mail_model, phone:$scope.sup_phone_model, vat_no:$scope.sup_vat_model}
						}).then(function mySucces(response) {
							if(response.data[0].status == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
								$scope.delButton = false;
								//add inserted item to tableview...
								$scope.list_row_to_push = {
								  	'supplier_id': response.data[0].supplier_id,
									'supplier_name': response.data[0].supplier_name,
									'address': response.data[0].address,
									'city': response.data[0].city,
									'district': response.data[0].district,
									'country': response.data[0].country,
									'state': response.data[0].state,
									'mailid': response.data[0].mailid,
									'mobileorlandline': response.data[0].mobileorlandline,
									'vatno': response.data[0].vatno,
									'rating': response.data[0].rating,
								  
								};
								$scope.all_suppliers.push($scope.list_row_to_push);	
								//load autocomplete data...
								$http({
											method : "POST",
											url : "supplierParams"
										}).then(function mySucces(response) {
											$scope.all_states = response.data.supplierStates;
											$scope.all_countries = response.data.supplierCountries;
											$scope.all_cities = response.data.supplierCities;
											$scope.all_districts = response.data.supplierDistricts;
										}, function myError(response) {

									});						
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
							}
						}, function myError(response) {

			});
		} //end of if
		else{ //condition for supplier update
			$http({
							method : "POST",
							url : "supplierUpdate",
							data: {supplier_id:$scope.selected_supplier_id,supplier_name:$scope.sup_name_model, address:$scope.sup_addr_model, city:$scope.sup_city_model, district:$scope.sup_district_model, state:$scope.sup_state_model, country:$scope.sup_country_model, mail_id:$scope.sup_mail_model, phone:$scope.sup_phone_model, vat_no:$scope.sup_vat_model}
						}).then(function mySucces(response) {
							if(response.data == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
								//$scope.delButton = false;
								//$scope.btnTxt = "Save";	
								for (var j = 0; j < $scope.all_suppliers.length; j++) {
					  				if($scope.all_suppliers[j].supplier_id == $scope.selected_supplier_id){
										$scope.all_suppliers[j].supplier_name = $scope.sup_name_model;
										$scope.all_suppliers[j].address = $scope.sup_addr_model;
										$scope.all_suppliers[j].city = $scope.sup_city_model;
										$scope.all_suppliers[j].district = $scope.sup_district_model;
										$scope.all_suppliers[j].country = $scope.sup_country_model;
										$scope.all_suppliers[j].state = $scope.sup_state_model;
										$scope.all_suppliers[j].mailid = $scope.sup_mail_model;
										$scope.all_suppliers[j].mobileorlandline = $scope.sup_phone_model;
										$scope.all_suppliers[j].vatno = $scope.sup_vat_model;
										break;
									}
								}//for loop end	
								//load autocomplete data...
								$http({
											method : "POST",
											url : "supplierParams"
										}).then(function mySucces(response) {
											$scope.all_states = response.data.supplierStates;
											$scope.all_countries = response.data.supplierCountries;
											$scope.all_cities = response.data.supplierCities;
											$scope.all_districts = response.data.supplierDistricts;
										}, function myError(response) {

									});//http end					
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
							}
						}, function myError(response) {

			});
		}
	}

	//table row clicked...
	$scope.supplierTableRowClicked = function(supplier_obj){
		$scope.selectedID = supplier_obj.supplier_id; //to make table selection hilight
		$scope.delButton = true; //show delete button
		$scope.btnTxt = "Update";
		$scope.selected_supplier_obj = supplier_obj
		$scope.selected_supplier_id = supplier_obj.supplier_id;
		$scope.sup_name_model = supplier_obj.supplier_name;
		$scope.sup_addr_model = supplier_obj.address;
		$scope.sup_city_model = supplier_obj.city;
		$scope.sup_district_model = supplier_obj.district;
		$scope.sup_state_model = supplier_obj.state;
		$scope.sup_country_model = supplier_obj.country;
		$scope.sup_mail_model = supplier_obj.mailid;
		$scope.sup_phone_model = supplier_obj.mobileorlandline;
		$scope.sup_vat_model = supplier_obj.vatno;
	}

	$scope.cancelClicked = function(){
		$scope.delButton = false; //hide delete button
		$scope.btnTxt = "Save";
		$scope.selectedID = null; //remove table selection		
		$scope.clearAll(); //clear all controls to default values	
	}

	//when back button clicked...
	$scope.backToPrevous = function(){
		$rootScope.showSupplierBack = false;
		$window.history.back(); //back to previous page
	}

	//delete button click...
	$scope.supplierDelete = function(){
		$http({
				method : "POST",
				url : "supplierDelete",
				data: {supplier_id: $scope.selected_supplier_id}
			}).then(function mySucces(response) {
				if(response.data == "success"){
					notifyMessage('fa fa-check-circle',"<b>Success</b><br>Item Deleted Successfully.",'info');
					$scope.cancelClicked();
					/*for (var i = 0; i < $scope.all_suppliers.length; i++) { //delete it from table view
			  			if($scope.all_suppliers[i].supplier_id == $scope.selected_supplier_id){	alert();
							$scope.index = $scope.all_suppliers.indexOf($scope.all_suppliers[i]);
							$scope.all_suppliers.splice($scope.index, 1);
							break;
						}
					}*/
					$scope.index = $scope.all_suppliers.indexOf($scope.selected_supplier_obj);
  					$scope.all_suppliers.splice($scope.index, 1);
				}
				else{
					notifyMessage('',"<b>Failed</b><br>Item can't be deleted."+response.data,'danger');
				}
			}, function myError(response) {

		});
	}//delete click end

	//custom filter start...
		$scope.customFilterForSupplier = function (searchText) {
		  function comparator(a, b) {
			return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
		  }

		  var lookInKeys = ['supplier_name', 'address','mailid', 'mobileorlandline','vatno', 'rating'];

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

























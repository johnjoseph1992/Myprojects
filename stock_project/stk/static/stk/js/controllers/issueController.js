//issue ctrl begin...
app.controller("issueCtrl", function($scope, $http, $rootScope, $window) {

	$scope.locations = [];
	$scope.selectedLocation = "";
	$scope.selectedIID = null;
	$scope.delButton = false;
	$scope.btnTxt = "Issue";
	$scope.all_issues = [];
	$scope.selected_issue_obj = null;
	$scope.loadingPart = true;
	$scope.nodataPart = false;
	//$scope.availablestatus = false;

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
	$scope.$on('issueNgRepeatFinished', function(ngRepeatFinishedEvent) { //worked when ng-repeat finished.(on-finish-render="issueNgRepeatFinished")
		$scope.loadingPart = false;
	});

	//function load the table view...
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "issueTableView"
			}).then(function mySucces(response) {
				$scope.all_issues = response.data.stkIssue;
				if($scope.all_issues.length == 0){
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
	console.log("Issue Loadtime :" + (end-start) + " milliseconds");

	//load initial data...
	$http({
				method : "POST",
				url : "issueParams"
			}).then(function mySucces(response) {
				$scope.all_items = response.data.stkItemMaster;
				$scope.units = response.data.stkUnits;
				$scope.maincats = response.data.stkMainCategory;
				$scope.depts = response.data.stkDept;
				$scope.subcats = response.data.stkSubCategory;
			}, function myError(response) {

		});


	//load locations when dept selection changed...
	$scope.deptSelectChanged = function(){
		$http({
					method : "POST",
					url : "loadLocations",
					data: {did:$scope.selectedDept.did}
				}).then(function mySucces(response) {
					$scope.locations = response.data.stkLocation;
				}, function myError(response) {

			});
	}

	$scope.deptClicked = function(){
		if(typeof($scope.selectedDept) == 'object'){
			$http({
						method : "POST",
						url : "loadLocations",
						data: {did:$scope.selectedDept.did}
					}).then(function mySucces(response) {
						$scope.locations = response.data.stkLocation;
					}, function myError(response) {

				});
		}
		else{
			//clear location box
		}
	}

	//subcategory selection changed...
	$scope.subcatSelectChanged = function(){
		$http({
					method : "POST",
					url : "loadItemsForSubcatId",
					data: {subcatid:$scope.selectedSubcat.subcat_id}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
				}, function myError(response) {

			});
	}

	$scope.itemSelected = function(){
		if($scope.selectedItem.qty_available <= 0)
			notifyMessage('fa fa-exclamation-triangle',"<b>Unavailable</b><br>"+$scope.selectedItem.item_name+" not available for issue.",'warning');
	}

	$scope.qtyChanged = function(){
		if(typeof($scope.selectedItem) == 'object'){
			if(($scope.issue_qty_model-$scope.selectedItem.qty_available) > 0) //more qty required
				notifyMessage('fa fa-exclamation-triangle',"<b>Unavailable</b><br>"+$scope.selectedItem.item_name+" not available for issue. Only "+ $scope.selectedItem.qty_available + " is available.",'warning');
		}
	}

	$scope.checkAvailableStatus = function(){
		if(typeof($scope.selectedItem) == 'object')
			return true;
		else
			return false;
	}

	$scope.deptLostFocus = function(){
		$scope.noDepts = false;
	}

	$scope.locationLostFocus = function(){
		$scope.noLocations = false;
	}

	$scope.subcatLostFocus = function(){
		$scope.noSubcats = false;
	}

	$scope.itemLostFocus = function(){
		$scope.noItems = false;
	}

	$scope.issueSubmit = function(){
		if($scope.delButton == false){ //for supplier submit
			$http({
							method : "POST",
							url : "issueSubmit",
							data: {todept:$scope.selectedDept.did, tolocation:$scope.selectedLocation.location_id, itemid:$scope.selectedItem.item_id, qty:$scope.issue_qty_model, unitid:$scope.unit_select_model, maincatid:$scope.maincat_select_model}
						}).then(function mySucces(response) {
							if(response.data[0].status == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
								$scope.delButton = false;
								//add inserted issue to tableview...
								$scope.list_row_to_push = {
								  	'issueid': response.data[0].issueid,
								  	'issuedate': response.data[0].issuedate,
								  	'issuedqty': response.data[0].issuedqty,
								  	'issuedbyid': response.data[0].issuedbyid,
								  	'issueddeptid': response.data[0].issueddeptid,
								  	'unitid': response.data[0].unitid,
								  	'maincatid': response.data[0].maincatid,
								  	'issuedbyempcode': response.data[0].issuedbyempcode,
								  	'issueddeptname': response.data[0].issueddeptname,
								  	'itemname': response.data[0].itemname,
								  	'itemid': response.data[0].itemid,
								  	'locationid': response.data[0].locationid,								  
								};
								$scope.all_issues.push($scope.list_row_to_push);
								//Reload initial data...
								$http({
											method : "POST",
											url : "issueParams"
										}).then(function mySucces(response) {
											$scope.all_items = response.data.stkItemMaster;
											$scope.units = response.data.stkUnits;
											$scope.maincats = response.data.stkMainCategory;
											$scope.depts = response.data.stkDept;
											$scope.subcats = response.data.stkSubCategory;
										}, function myError(response) {

									});
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data[0].data,'danger');
							}
						}, function myError(response) {

				});
		}
		else{ //condition for update
			$http({
							method : "POST",
							url : "issueUpdate",
							data: {issueid:$scope.selected_issue_id, todept:$scope.selectedDept.did, tolocation:$scope.selectedLocation.location_id, itemid:$scope.selectedItem.item_id, qty:$scope.issue_qty_model, unitid:$scope.unit_select_model, maincatid:$scope.maincat_select_model}
						}).then(function mySucces(response) {
							if(response.data == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
								for (var j = 0; j < $scope.all_issues.length; j++) {
					  				if($scope.all_issues[j].issueid == $scope.selected_issue_id){
										$scope.all_issues[j].issueddeptid = $scope.selectedDept.did;
										$scope.all_issues[j].issueddeptname = $scope.selectedDept.department_name;
										$scope.all_issues[j].locationid = $scope.selectedLocation.location_id;
										$scope.all_issues[j].issuedqty = $scope.issue_qty_model;
										$scope.all_issues[j].unitid = $scope.unit_select_model;
										$scope.all_issues[j].maincatid = $scope.maincat_select_model;
										break;
									}
								}//for loop end	
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
							}
						}, function myError(response) {

				});
		}
	}

	//issue tablerow 
	$scope.issueTableRowClicked = function(issue){
		$scope.selectedIID = issue.issueid;
		$scope.delButton = true; //show delete button
		$scope.btnTxt = "Update";
		$scope.selected_issue_id = issue.issueid;
		$scope.selected_issue_obj = issue;
		$scope.issue_qty_model = issue.issuedqty;
		$scope.unit_select_model = issue.unitid;
		$scope.maincat_select_model = issue.maincatid;
		for (var i = 0; i < $scope.depts.length; i++) { //the object corresponds to the did is assigned to typeahead
  			if($scope.depts[i].did == issue.issueddeptid){
				$scope.selectedDept = $scope.depts[i];
				break;
			}
		}

		/*for (var i = 0; i < $scope.locations.length; i++) { //the object corresponds to the location_id is assigned to typeahead
  			if($scope.locations[i].location_id == issue.locationid){
				$scope.selectedLocation = $scope.locations[i];
				break;
			}
		}*/

		//assign to location typehead(http start)...
		$http({
					method : "POST",
					url : "loadLocations",
					data: {did:issue.issueddeptid}
				}).then(function mySucces(response) {
					$scope.locations = response.data.stkLocation;
					for (var i = 0; i < $scope.locations.length; i++) { //the object corresponds to the location_id is assigned to typeahead
			  			if($scope.locations[i].location_id == issue.locationid){
							$scope.selectedLocation = $scope.locations[i];
							break;
						}
					}
				}, function myError(response) {

		});	//http end
		for (var i = 0; i < $scope.all_items.length; i++) { //the object corresponds to the item_id is assigned to typeahead
  			if($scope.all_items[i].item_id == issue.itemid){
				$scope.selectedItem = $scope.all_items[i];
				break;
			}
		}
	}

	//issue cancel button clicked [work as issue delete]
	$scope.issueDelete = function(){
		//$scope.index = $scope.all_issues.indexOf($scope.selected_issue_obj);
  		//$scope.all_issues.splice($scope.index, 1);
		$http({
				method : "POST",
				url : "issueDelete",
				data: {issue_id: $scope.selected_issue_id}
			}).then(function mySucces(response) {
				if(response.data == "success"){
					notifyMessage('fa fa-check-circle',"<b>Success</b><br>Item Deleted Successfully.",'info');
					$scope.index = $scope.all_issues.indexOf($scope.selected_issue_obj);
  					$scope.all_issues.splice($scope.index, 1);
					$scope.delButton = false;
					$scope.btnTxt = "Issue";
					$scope.selectedIID = null;
					$scope.selected_issue_obj = null;
					$scope.selected_issue_id = null;
				}
				else{
					notifyMessage('',"<b>Failed</b><br>Issue can't be deleted."+response.data,'danger');
				}
			}, function myError(response) {

		});
	}//issue cancel end

	$scope.clearClicked = function(){
		$scope.selectedIID = null;
		$scope.btnTxt = "Issue";
		$scope.delButton = false;
		$scope.selected_issue_id=$scope.selected_issue_obj=null;
		$scope.selectedDept=$scope.selectedSubcat=$scope.selectedLocation=$scope.selectedItem=$scope.issue_qty_model="";
		/*if(angular.isDefined($scope.subcat_select_model)){ //clearing the selection of subcategory select box
			delete $scope.subcat_select_model;
		}*/
		if(angular.isDefined($scope.unit_select_model)){ //clearing the selection of unit select box
			delete $scope.unit_select_model;
		}
		if(angular.isDefined($scope.maincat_select_model)){ //clearing the selection of maincategory select box
			delete $scope.maincat_select_model;
		}
	}

	//custom filter start...
	$scope.customFilterForItem = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['item_name','model_code'];
		
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

	//custom filter start...
	$scope.customFilterForIssue = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['issuedate','itemname','issuedqty','issueddeptname','issuedbyempcode'];
		
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

























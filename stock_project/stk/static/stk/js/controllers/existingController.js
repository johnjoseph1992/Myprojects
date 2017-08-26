//existing item reg ctrl begin...
app.controller("existingCtrl", function($scope, $http, $rootScope, $window) {

	$scope.locations = [];
	$scope.all_items = [];
	$scope.units = [];
	$scope.depts = [];
	$scope.subcats = [];
	$scope.all_existing = [];
	$scope.all_shown = [];
	$scope.delButton = false;
	$scope.btnTxt = "Save";
	$scope.fitids = [];
	$scope.all_fisatids = [];
	$scope.fitidDisabled = false;
	$scope.exist_check_submit_model = false;
	$scope.selectedDID = null;
	$scope.selected_itemdetailobj = null;
	$scope.qty_remainingtoadd = 0;
	$scope.loadingPart = true;
	$scope.nodataPart = false;

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
				url : "existingTableView"
			}).then(function mySucces(response) {
				$scope.all_existing = response.data.stkItemDetails;
				if($scope.all_existing.length == 0){
					$scope.nodataPart = true;
					$scope.loadingPart = false;
					$scope.errorMsg = "No Records";
				}
				$scope.all_shown = [];
				for (var i = 0; i < $scope.all_existing.length; i++) { //initially show all unissued existing items from list of all.
					if($scope.all_existing[i].issueid == ""){
						$scope.all_shown.push($scope.all_existing[i]);
					}
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
	console.log("Existing Loadtime :" + (end-start) + " milliseconds");

	$scope.clearClicked = function(){
		$scope.selectedSubcat=$scope.selectedItem=$scope.exist_qty_model=$scope.selectedDept=$scope.selectedLocation=$scope.issued_date_model=$scope.fitid_txtbox_model=$scope.selected_itemdetailsid=$scope.selected_issueid=$scope.warranty_todate_model="";
		$scope.delButton = false;
		$scope.btnTxt = "Save";
		$scope.selectedDID = null;
		$scope.fitids = [];
		$scope.selected_itemdetailobj = null;
		if(angular.isDefined($scope.unit_select_model))
			delete $scope.unit_select_model;
	}

	$scope.showAllNonissued = function(){
		$scope.all_shown = [];
		for (var i = 0; i < $scope.all_existing.length; i++) { //show all unissued existing items from list of all.
			if($scope.all_existing[i].issueid == ""){
				$scope.all_shown.push($scope.all_existing[i]);
			}
		}
		if($scope.delButton == true)
			$scope.clearClicked();
	}

	$scope.showAllIssued = function(){
		$scope.all_shown = [];
		for (var i = 0; i < $scope.all_existing.length; i++) { //initially show all issued existing items from list of all.
			if($scope.all_existing[i].issueid != ""){
				$scope.all_shown.push($scope.all_existing[i]);
			}
		}
		if($scope.delButton == true)
			$scope.clearClicked();
	}

	$scope.checkAvailableStatus = function(){
		if(typeof($scope.selectedItem) == 'object')
			return true;
		else
			return false;
	}

	$scope.itemSelected = function(){
		$scope.unit_select_model = $scope.selectedItem.unit_id;
		if($scope.exist_qty_model > $scope.selectedItem.qty_remaining_toadd){ //exceed remaining to add limit
				notifyMessage('fa fa-exclamation-triangle',"<b>Limit Exceeded</b><br>Only "+$scope.selectedItem.qty_remaining_toadd+" need to be added.",'warning');
				$scope.exist_qty_model = "";
		}
	}

	//load initial data...
	$scope.loadInitParams = function(){
		$http({
					method : "POST",
					url : "existParams"
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					$scope.units = response.data.stkUnits;
					$scope.depts = response.data.stkDept;
					$scope.subcats = response.data.stkSubCategory;
					$scope.all_fisatids = response.data.stkFisatIds;
				}, function myError(response) {

			});
	}
	$scope.loadInitParams();


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
		$scope.selectedItem = "";
		$http({
					method : "POST",
					url : "loadRemainingToAddItemsForSubcatId",
					data: {subcatid:$scope.selectedSubcat.subcat_id}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
				}, function myError(response) {

			});
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

	$scope.qtyChanged = function(){
		if(typeof($scope.selectedItem) == 'object'){
			if($scope.exist_qty_model > $scope.selectedItem.qty_remaining_toadd){ //exceed remaining to add limit
				notifyMessage('fa fa-exclamation-triangle',"<b>Limit Exceeded</b><br>Only "+$scope.selectedItem.qty_remaining_toadd+" need to be added.",'warning');
				$scope.exist_qty_model = "";
			}
		}
	}

	$scope.removeFitId = function(fit){
		$scope.index = $scope.fitids.indexOf(fit);
  		$scope.fitids.splice($scope.index, 1);
	}

	$scope.enterKeyPressed = function(keyEvent){
		if (keyEvent.which == 13 && $scope.delButton == false){ //Enterkey is pressed inside fitid txtbox
			if(!angular.isDefined($scope.exist_qty_model)){
				$scope.fitidDisabled = true;
				$scope.fitid_txtbox_model = "";
				notifyMessage('fa fa-exclamation-triangle',"<b>Quantity Required</b><br> Proper quantity required.",'warning');
				return;
			}

			for (var i = 0; i < $scope.fitids.length; i++) { //check whether exist in the client side array.
					if($scope.fitids[i].fitid.toUpperCase() == $scope.fitid_txtbox_model.toUpperCase()){
						notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.fitid_txtbox_model+" is already entered.",'warning');
						return;
					}
			}

			for (var i = 0; i < $scope.all_fisatids.length; i++) { //check whether the fisat id is already existing in the table.
				if($scope.all_fisatids[i].fisatid.toUpperCase() == $scope.fitid_txtbox_model.toUpperCase()){
					notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.fitid_txtbox_model+" is already existing.",'warning');
					return;
				}
			}

			if(angular.isDefined($scope.fitid_txtbox_model)){
				if($scope.warranty_todate_model==null)
					$scope.warto = "";
				else
					$scope.warto = $scope.warranty_todate_model;
				$scope.fitidrow={
					'fitid':$scope.fitid_txtbox_model.toUpperCase(),
					'warrantyto':$scope.warto
				};
				$scope.fitids.push($scope.fitidrow);
				$scope.fitid_txtbox_model = "";
			}
		}
	}

	//submit existing item...
	$scope.existSubmit = function(){
		//enter fitid txtbox item to fisatids array start...
		if($scope.fitid_txtbox_model != "" && $scope.delButton == false && angular.isDefined($scope.fitid_txtbox_model)){
			for (var i = 0; i < $scope.fitids.length; i++) { //check whether exist in the client side array.
				if($scope.fitids[i].fitid.toUpperCase() == $scope.fitid_txtbox_model.toUpperCase()){
					notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.fitid_txtbox_model+" is already entered.",'warning');
					return;
				}
			}

			for (var i = 0; i < $scope.all_fisatids.length; i++) { //check whether the fisat id is already existing in the table.
				if($scope.all_fisatids[i].fisatid.toUpperCase() == $scope.fitid_txtbox_model.toUpperCase()){
					notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.fitid_txtbox_model+" is already existing.",'warning');
					return;
				}
			}

			if(angular.isDefined($scope.fitid_txtbox_model)){
				if($scope.warranty_todate_model==null)
					$scope.warto = "";
				else
					$scope.warto = $scope.warranty_todate_model;
				$scope.fitidrow={
					'fitid':$scope.fitid_txtbox_model.toUpperCase(),
					'warrantyto':$scope.warranty_todate_model
				};
				$scope.fitids.push($scope.fitidrow);
				$scope.fitid_txtbox_model = "";
			}
		}
		//enter fitid txtbox item to fisatids array end...

		//error check part start...
		if(typeof($scope.selectedItem) == 'object'){
			if($scope.exist_qty_model > $scope.selectedItem.qty_remaining_toadd){ //exceed remaining to add limit
				notifyMessage('fa fa-exclamation-triangle',"<b>Limit Exceeded</b><br>Only "+$scope.selectedItem.qty_remaining_toadd+" need to be added.",'warning');
				return;
			}
		}
		//error check part end...

		var jsonAllIds=angular.toJson($scope.fitids);
		if($scope.delButton == false){ //for existing item submit
			//error check before submit start...
			if($scope.fitids.length < 1 && $scope.delButton != true){
				notifyMessage('fa fa-exclamation-triangle',"<b>No Fisat IDS</b><br>No FisatIDs specified.",'warning');
				return;
			}
			if($scope.fitids.length != $scope.exist_qty_model && $scope.delButton != true){
				notifyMessage('fa fa-exclamation-triangle',"<b>Quantity Difference</b><br>"+$scope.exist_qty_model+" number of fisatids required.",'warning');
				return;
			}
			//error check before submit end...
			if(!angular.isDefined($scope.selectedDept) || $scope.selectedDept==null || typeof($scope.selectedDept) != 'object') //if department is undefined or null,it can be null sometimes.
				$scope.did = "";
			else
				$scope.did = $scope.selectedDept.did;
			if(!angular.isDefined($scope.selectedLocation) || $scope.selectedLocation==null || typeof($scope.selectedLocation) != 'object') //if location is undefined or null,it can be null sometimes.
				$scope.lid = "";
			else
				$scope.lid = $scope.selectedLocation.location_id;
			if($scope.issued_date_model == null) //this field also can be null.
				$scope.isudate = null;
			else
				$scope.isudate = $scope.issued_date_model;
			$http({
							method : "POST",
							url : "existSubmit",
							data: {itemid:$scope.selectedItem.item_id, qty:$scope.exist_qty_model, unitid:$scope.unit_select_model,jsonids:jsonAllIds,issuedornot:$scope.exist_check_submit_model, todept:$scope.did, tolocation:$scope.lid, issuedate:$scope.isudate}
						}).then(function mySucces(response) {
							if(response.data[0].status == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
								$scope.delButton = false;
								for (var i = 0; i < response.data.length; i++){ //multiple rows are returned from django
									$scope.list_row_to_push = {
									  	'itemdetailsid': response.data[i].itemdetailsid,
									  	'fisatid': response.data[i].fisatid,
									  	'issuedornot': response.data[i].issuedornot,
									  	'itemid': response.data[i].itemid,
									  	'itemname': response.data[i].itemname,
									  	'deptid': response.data[i].deptid,
									  	'todeptname': response.data[i].todeptname,
									  	'tolocationid': response.data[i].tolocationid,
									  	'tolocationname': response.data[i].tolocationname,
									  	'issueid': response.data[i].issueid,
									  	'issuedate': response.data[i].issuedate,
									  	'warrantyto': response.data[i].warrantyto,		  
									};
									$scope.all_existing.push($scope.list_row_to_push);
									$scope.all_shown.push($scope.list_row_to_push);
								}
								$scope.clearClicked();
								$scope.loadInitParams();
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data[0].data,'danger');
							}
						}, function myError(response) {

				});
		}
		else{ //condition for update
			//error check for already existing start...
			for (var i = 0; i < $scope.all_fisatids.length; i++) { //check whether the fisat id is already existing in the table.
				if(($scope.all_fisatids[i].fisatid.toUpperCase() == $scope.fitid_txtbox_model.toUpperCase()) && ($scope.all_fisatids[i].fisatid.toUpperCase() != $scope.selected_itemdetailobj.fisatid.toUpperCase())){
					notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.fitid_txtbox_model+" is already existing.",'warning');
					return;
				}
			}
			//error check for already existing end...
			
			//notify user that you are updating the fitid and issued date.
			if (confirm("You are going to update the Fisatid.") == true) {
				console.log("pressed ok so execute update.");
			} else {
				console.log("pressed cancel so return.");
				return;
			}
			if($scope.issued_date_model == null) //this field also can be null.
				$scope.isudate = null;
			else
				$scope.isudate = $scope.issued_date_model;

			if($scope.warranty_todate_model==null)
				$scope.warto = "";
			else
				$scope.warto = $scope.warranty_todate_model;

			$http({
							method : "POST",
							url : "existUpdate",
							data: {itemdetailsid:$scope.selected_itemdetailsid, issueid:$scope.selected_issueid, issueddate:$scope.isudate, fitid:$scope.fitid_txtbox_model, isissued:$scope.exist_check_submit_model, warrantyto:$scope.warto}
						}).then(function mySucces(response) {
							if(response.data == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
								$scope.delButton = false;
								for (var i = 0; i < $scope.all_existing.length; i++){
									if($scope.all_existing[i].itemdetailsid == $scope.selected_itemdetailsid){
										$scope.all_existing[i].fisatid = $scope.fitid_txtbox_model;
										$scope.all_existing[i].issuedate = $scope.isudate;
										$scope.all_existing[i].warrantyto = $scope.warto;
									}
								}
								if($scope.exist_check_submit_model){ //if-else start...
									$scope.all_shown = [];
									for (var i = 0; i < $scope.all_existing.length; i++) { //show all issued existing items from list of all.
										if($scope.all_existing[i].issueid != ""){
											$scope.all_shown.push($scope.all_existing[i]);
										}
									}
								}
								else{
									$scope.all_shown = [];
									for (var i = 0; i < $scope.all_existing.length; i++) { //show all issued existing items from list of all.
										if($scope.all_existing[i].issueid == ""){
											$scope.all_shown.push($scope.all_existing[i]);
										}
									}
								} //if-else end...
								$scope.clearClicked();
								$scope.loadInitParams();
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
							}
						}, function myError(response) {

				});
		}//if-else end
	}//submit function end...

	$scope.itemDetailTableRowClicked = function(detail_obj){
		$scope.delButton = true;
		$scope.btnTxt = "Update";
		$scope.fitids = [];
		$scope.selected_itemdetailsid = detail_obj.itemdetailsid;
		$scope.selected_issueid = detail_obj.issueid;
		$scope.selected_itemdetailobj = detail_obj;
		$scope.selectedDID = detail_obj.itemdetailsid;
		$scope.exist_qty_model = 1;//just for updating fisatid
		$scope.fitid_txtbox_model = detail_obj.fisatid;
		if(detail_obj.warrantyto == "")
			$scope.warranty_todate_model = "";
		else
			$scope.warranty_todate_model = detail_obj.warrantyto;
		$scope.issued_date_model = detail_obj.issuedate;
		for (var i = 0; i < $scope.all_items.length; i++) { //the object corresponds to the item_id is assigned to typeahead
	  		if($scope.all_items[i].item_id == detail_obj.itemid){
				$scope.selectedItem = $scope.all_items[i];
				break;
			}
		}
		if(detail_obj.deptid !=""){ //if for deptid check start...
			for (var i = 0; i < $scope.depts.length; i++) { //the object corresponds to the dept_id is assigned to typeahead
		  		if($scope.depts[i].did == detail_obj.deptid){
					$scope.selectedDept = $scope.depts[i];
					break;
				}
			}
			//load location name properly...
			$http({
							method : "POST",
							url : "loadLocations",
							data: {did:$scope.selectedDept.did}
						}).then(function mySucces(response) {
							$scope.locations = response.data.stkLocation;
							for (var i = 0; i < $scope.locations.length; i++) { //the object corresponds to the location_id is assigned to typeahead
						  		if($scope.locations[i].location_id == detail_obj.tolocationid){
									$scope.selectedLocation = $scope.locations[i];
									break;
								}
							}
						}, function myError(response) {

				}); //load location end...
		} //if for deptid check end...

		
	}

	$scope.existDelete = function(){
		//notify user that you are deleting the record.
		if (confirm("You are going to delete the item.") == true) {
			console.log("pressed ok so execute delete.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}

		$http({
							method : "POST",
							url : "existDelete",
							data: {itemdetailsid:$scope.selected_itemdetailsid, isissued:$scope.exist_check_submit_model, issueid:$scope.selected_issueid}
						}).then(function mySucces(response) {
							if(response.data == "success"){
								notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Deleted Successfully.",'info');
								$scope.index = $scope.all_existing.indexOf($scope.selected_itemdetailobj);
  								$scope.all_existing.splice($scope.index, 1);
								$scope.index = $scope.all_shown.indexOf($scope.selected_itemdetailobj);
  								$scope.all_shown.splice($scope.index, 1);
								$scope.clearClicked();
								$scope.loadInitParams();
							}
							else{
								notifyMessage('',"<b>Failed</b><br>Failed to delete data."+response.data,'danger');
							}
						}, function myError(response) {

				});
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
	$scope.customFilterForDetails = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['itemname','todeptname','tolocationname','issuedate','fisatid'];
		
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

























//existing item reg ctrl begin...
app.controller("purchaseReturnCtrl", function($scope, $http, $rootScope, $window) {

	$scope.all_items = [];
	$scope.full_items = [];
	$scope.selected_items = [];
	$scope.all_preturns = [];
	//$scope.selectedDID = null;
	//$scope.delButton = false;
	$scope.loadingPart = true;
	$scope.nodataPart = false;
	$scope.supplierdependents = [];
	$scope.norecords = null;
	$scope.clickedSupplierid = null;

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
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "purchaseReturnTableView"
			}).then(function mySucces(response) {
				$scope.all_preturns = response.data.stkPurchaseReturn;
				if($scope.all_preturns.length == 0){
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
	console.log("PurchaseReturn Loadtime :" + (end-start) + " milliseconds");

	//load initial data...
	$scope.loadInitParams = function(){
		$http({
					method : "POST",
					url : "purchaseReturnParams"
				}).then(function mySucces(response) {
					$scope.all_suppliers = response.data.stkSupplier;
				}, function myError(response) {

			});
	}
	$scope.loadInitParams();

	$scope.clearClicked = function(){
		$scope.invoiceno_model=$scope.selectedSupplier=$scope.selectedItem=$scope.returnedby_model=$scope.desc_model="";
		$scope.selected_items=$scope.full_items=$scope.all_items=[];
		//$scope.selectedDID = null;
		//$scope.delButton = false;
		$scope.selected_purchasereturn_obj = null;
		$scope.clickedSupplierid = null;
	}

	//when invoice no typed and enter key pressed...
	$scope.enterKeyPressed = function(keyEvent){
		$scope.selectedItem = "";
		$scope.selectedSupplier = "";
		$scope.selected_items = [];//clear when supplier changed
		if (keyEvent.which == 13){ //Enterkey is pressed inside invoiceno txtbox
			$http({
					method : "POST",
					url : "loadItemsForInvoice",
					data: {invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					if((angular.isDefined($scope.all_items) && $scope.all_items.length == 0) || (!angular.isDefined($scope.all_items)))
						$scope.norecords = true;
					else
						$scope.norecords = false;
				}, function myError(response) {

			});

			$scope.supplierdependents = [];
			$http({
					method : "POST",
					url : "loadSupplierForInvoice",
					data: {invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.supplierdependents = response.data.stkSupplier;
					$scope.clickedSupplierid = $scope.supplierdependents[0].supplierid;
					$scope.selectedSupplier = $scope.supplierdependents[0];
					//load items in the autocomplete according to selected supplier
					$http({
								method : "POST",
								url : "loadItemsForPurReturnAutocomplete",
								data: {supplierid:$scope.selectedSupplier.supplierid, invoiceno:$scope.invoiceno_model}
							}).then(function mySucces(response) {
								$scope.full_items = response.data.itemMasterData;
							}, function myError(response) {

						});
				}, function myError(response) {

			});
		}
	}

	//when invoice no re typed then clear some fields...
	$scope.invoiceChanged = function(){
		$scope.selectedSupplier=$scope.selectedItem="";
		$scope.selected_items=$scope.full_items=$scope.all_items=[];
		$scope.selected_purchasereturn_obj = null;
		$scope.clickedSupplierid = null;
	}

	$scope.supplierListClicked = function(supplier){
		$scope.clickedSupplierid = supplier.supplierid;
		$scope.selectedSupplier = supplier;
		$scope.selectedItem = "";
		$scope.selected_items = [];//clear when supplier changed
		$http({
					method : "POST",
					url : "loadItemsForSupplierAndInvoice",
					data: {supplierid:supplier.supplierid, invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					if((angular.isDefined($scope.all_items) && $scope.all_items.length == 0) || (!angular.isDefined($scope.all_items)))
						$scope.norecords = true;
					else
						$scope.norecords = false;
				}, function myError(response) {

			});

		//load item autocompletebox
		$http({
					method : "POST",
					url : "loadItemsForPurReturnAutocomplete",
					data: {supplierid:supplier.supplierid, invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.full_items = response.data.itemMasterData;
				}, function myError(response) {

			});
	}
	
	//supplier selection changed...
	$scope.supplierSelectChanged = function(){
		$scope.selectedItem = "";
		$scope.selected_items = [];//clear when supplier changed
		$http({
					method : "POST",
					url : "loadItemsForSupplierAndInvoice",
					data: {supplierid:$scope.selectedSupplier.supplierid, invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					if((angular.isDefined($scope.all_items) && $scope.all_items.length == 0) || (!angular.isDefined($scope.all_items)))
						$scope.norecords = true;
					else
						$scope.norecords = false;
					$scope.supplierdependents = [];
					$scope.supplierdependents.push({"supplierid":$scope.selectedSupplier.supplierid,"suppliername":$scope.selectedSupplier.suppliername});
					$scope.clickedSupplierid = $scope.selectedSupplier.supplierid;
				}, function myError(response) {

			});

		//load item autocompletebox
		$http({
					method : "POST",
					url : "loadItemsForPurReturnAutocomplete",
					data: {supplierid:$scope.selectedSupplier.supplierid, invoiceno:$scope.invoiceno_model}
				}).then(function mySucces(response) {
					$scope.full_items = response.data.itemMasterData;
				}, function myError(response) {

			});
	}

	//item select changed...
	$scope.itemSelectChanged = function(){
		$scope.selected_items = [];//clear when item changed
		//$scope.all_items = [];
		$http({
					method : "POST",
					url : "loadItemsForSupplierInvoiceAndItem",
					data: {supplierid:$scope.selectedSupplier.supplierid, invoiceno:$scope.invoiceno_model, itemid:$scope.selectedItem.itemid}
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					if((angular.isDefined($scope.all_items) && $scope.all_items.length == 0) || (!angular.isDefined($scope.all_items)))
						$scope.norecords = true;
					else
						$scope.norecords = false;
				}, function myError(response) {

			});
	}

	$scope.checkedItemSelected = function(fitid,checkedvalue,itemname,itemid,itemdetailsid){
		//alert(fitid+checkedvalue+itemname+itemdetailsid);
		if(checkedvalue==true){//if start
			$scope.selecteditemrow={
				'fitid':fitid,
				'itemdetailsid':itemdetailsid,
				'itemid':itemid,
				'itemname':itemname,
				'checkedvalue':checkedvalue,
				'suppliername':$scope.selectedSupplier.suppliername,
				'supplierid':$scope.selectedSupplier.supplierid,
				'invoiceno':$scope.invoiceno_model,
				'returnedby':$scope.returnedby_model,
			};
			$scope.selected_items.push($scope.selecteditemrow);
		}//if end
		else{//else start
			for(var i=0;i<$scope.selected_items.length;i++){
				if($scope.selected_items[i].itemdetailsid == itemdetailsid){
					$scope.index = $scope.selected_items.indexOf($scope.selected_items[i]);
  					$scope.selected_items.splice($scope.index, 1);
				}
			}
		}//else end
	}

	//submit function...
	$scope.purchaseReturnSubmit = function(){
		if($scope.returnedby_model == null || !angular.isDefined($scope.returnedby_model) || $scope.returnedby_model == ""){
			notifyMessage('fa fa-check-circle',"<b>Required</b><br>Return suggested by field is required.",'warning');
			return;
		}
		if($scope.selected_items.length < 1){
			notifyMessage('fa fa-check-circle',"<b>No Items Selected</b><br>No items selected for return.",'warning');
			return;
		}		

		//notify user that you are returning the item.
		if (confirm("You are going to return the item.") == true) {
			console.log("pressed ok so execute return.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}
 
		if($scope.desc_model == null || $scope.desc_model == "" || !angular.isDefined($scope.desc_model))
			$scope.descriptionfield = "";
		else
			$scope.descriptionfield = $scope.desc_model;
		var jsonFullSelected=angular.toJson($scope.selected_items);
		$http({
					method : "POST",
					url : "purchaseReturnSubmit",
					data: {returnedby:$scope.returnedby_model, description:$scope.descriptionfield, jsonAllSelected:jsonFullSelected}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
						$scope.loadtabledata();
						$scope.clearClicked();
						/*for (var i = 0; i < response.data.length; i++){ //multiple rows are returned from django
							$scope.list_row_to_push = {
							  	'itemdetailsid': response.data[i].itemdetailsid,
							  	'fisatid': response.data[i].fisatid,	  
							};
							$scope.all_existing.push($scope.list_row_to_push);
						}
						$scope.clearClicked();
						$scope.loadInitParams();*/
					}
					else{
						notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data[0].data,'danger');
					}
				}, function myError(response) {

		});
	}

	/*//purchase return table row clicked...
	$scope.preturnTableRowClicked = function(preturn_obj){
		//$scope.selectedDID = preturn_obj.itemdetailsid;
		//$scope.delButton = true;
		//$scope.selected_purchasereturn_obj = preturn_obj;
	}*/

	//purchase return cancel entry...
	$scope.purchaseReturnDelete = function(preturn_obj){
		$scope.selected_purchasereturn_obj = preturn_obj;
		//notify user that you are deleting the record.
		if (confirm("You are going to cancel the purchase return entry.") == true) {
			console.log("pressed ok so execute cancel.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}

		$http({ //http start
					method : "POST",
					url : "purchaseReturnDelete",
					data: {purchasereturnid:$scope.selected_purchasereturn_obj.purchasereturnid, purchaseid:$scope.selected_purchasereturn_obj.purchaseid, itemdetailsid:$scope.selected_purchasereturn_obj.itemdetailsid, itemid:$scope.selected_purchasereturn_obj.itemid}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Deleted Successfully.",'info');
						$scope.index = $scope.all_preturns.indexOf($scope.selected_purchasereturn_obj);
						$scope.all_preturns.splice($scope.index, 1);
						$scope.clearClicked();
						$scope.loadInitParams();
					}
					else{
						notifyMessage('',"<b>Failed</b><br>Failed to delete data."+response.data,'danger');
					}
				}, function myError(response) {

		}); //http end
	} //purchase return delete function end

	$scope.supplierLostFocus = function(){
		$scope.noSupplier = false;
	}

	$scope.itemLostFocus = function(){
		$scope.noItems = false;
	}

	//custom filter start...
	$scope.customFilterForReturn = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['suppliername','invoiceno','itemname','fitid','returneddate'];
		
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
	$scope.customFilterForItem = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['itemname','itemcode'];
		
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

























/////////////////////////// The detail_id must be defined in terms of $index , to be donemainly in purchaseupdate////////////////////////


//rootScope.pdetails[] and $rootScope.navigateStartedFlag are defined in adminMain.html ==> sidebarCtrl controller
//purchase ctrl begin...
app.controller("purchaseCtrl", function($scope, $http, $rootScope) {

	$scope.details = [];
	$scope.detail_id = 0;
	//$scope.detailTablePart = false;	
	$scope.selectedRowID = null;
	$scope.all_suppliers = [];
	$scope.all_items = [];
	$scope.all_itemsbackup = [];
	$scope.maincats = [];
	$scope.units = [];
	$scope.insertedItems = [];
	$scope.detailBtnTxt = "Add";
	$scope.btnTxt = "Save";
	$scope.selected_detail_id_for_detail = null;
	$scope.item_total=0;
	$scope.grand_total=0;
	$scope.all_purchases = [];
	$scope.selectedPID = null;
	$scope.delButton = false;

	//$scope.tot_price_model = $rootScope.price;

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

	//function load the initial parameters...
	$http({
			method : "POST",
			url : "purchaseParams"
		}).then(function mySucces(response) {
			$scope.maincats = response.data.stkMainCategory;
			$scope.all_items = response.data.stkItemMaster;
			$scope.all_itemsbackup = response.data.stkItemMaster;
			$scope.all_suppliers = response.data.stkSupplier;
			$scope.units = response.data.stkUnits;
		}, function myError(response) {

	});//initial parameter loading end...

	//function load the table view...
	$scope.loadtabledata = function(){
		$http({
				method : "POST",
				url : "purchaseTableView"
			}).then(function mySucces(response) {
				$scope.all_purchases = response.data.stkPurchaseMaster;
			}, function myError(response) {

		});
	}//loading table end...
	$scope.loadtabledata();

	$scope.reloadRootScopeParams = function(){
		//main data values...
		$scope.invoice_no_model=$rootScope.pinvoice_no_model;
		$scope.invoice_date_model=$rootScope.pinvoice_date_model;
		$scope.purchase_date_model=$rootScope.ppurchase_date_model;
		$scope.tot_price_model=$rootScope.ptot_price_model;
		$scope.tot_tax_model=$rootScope.ptot_tax_model;
		$scope.net_amount_model=$rootScope.pnet_amount_model;
		$scope.tot_discount_model=$rootScope.ptot_discount_model;
		/*$scope.entered_date_model=$rootScope.pentered_date_model;*/
		$scope.selectedSupplier=$rootScope.pselectedSupplier;
		//details values...
		if($rootScope.pdetailBtnTxt == null)
			$scope.detailBtnTxt="Add";
		else
			$scope.detailBtnTxt=$rootScope.pdetailBtnTxt;
		$scope.selected_detail_id_for_detail=$rootScope.pselected_detail_id_for_detail;
		$scope.selectedRowID=$rootScope.pselectedRowID;
		$scope.details=$rootScope.pdetails.slice(0); //it will copy the array "pdetails" to details
		//$scope.item_total=$rootScope.pitem_total;
		$scope.grand_total=$rootScope.pgrand_total;
		$scope.detailTablePart = $rootScope.pdetailTablePart;
		$scope.maincat_select_model=$rootScope.pmaincat_select_model;
		$scope.qty_model=$rootScope.pqty_model;
		$scope.desc_model=$rootScope.pdesc_model;
		$scope.unit_price_model=$rootScope.punit_price_model;
		$scope.indivi_discount_model=$rootScope.pindivi_discount_model;
		$scope.tax_percent_model=$rootScope.ptax_percent_model;
		$scope.tax_amt_model=$rootScope.ptax_amt_model;
		$scope.stk_regtr_pageno_model=$rootScope.pstk_regtr_pageno_model;
		$scope.unit_select_model=$rootScope.punit_select_model;
		$scope.warranty_todate_model = $rootScope.pwarranty_todate_model;
		$scope.selectedItem=$rootScope.pselectedItem;
		$rootScope.navigateStartedFlag == false; //navigation ended after assignment
	}
	if($rootScope.navigateStartedFlag == true)
		$scope.reloadRootScopeParams();

	$scope.pushToAllItems = function(itemid){
		$scope.detail_row = {
				  'item_name': purchase_obj.purchaseInfo[i].itemname,
				  'item_id': purchase_obj.purchaseInfo[i].itemid,
		};
		$scope.all_items.push($scope.detail_row);
	}

	$scope.popFromAllItems = function(itemid){

	}

	$scope.addDetailClicked = function(){
		$scope.detailTablePart = true;
		if($scope.detailBtnTxt == "Add"){ //if adding new detail	
			//$scope.detail_id = $scope.detail_id + 1;
			if($scope.warranty_todate_model == null) //this field also can be null.
				$scope.warrantytodate = null;
			else
				$scope.warrantytodate = $scope.warranty_todate_model;
			$scope.detail_row = {
			  'detail_id': $scope.selected_detail_id_for_detail,
			  /*'maincat_name': $scope.maincat_select_model.maincatname,*/
			  'maincat_id': $scope.maincat_select_model,
			  'item_name': $scope.selectedItem.item_name,
			  'item_id': $scope.selectedItem.item_id,
			  'supplier_name': $scope.selectedSupplier.supplier_name,
			  'supplier_id': $scope.selectedSupplier.supplier_id,
			  'quantity': $scope.qty_model,
			  'description': $scope.desc_model,
			  'unit_price': $scope.unit_price_model,
			  'individual_discount': $scope.indivi_discount_model,
			  'individual_tax_percentage': $scope.tax_percent_model,
			  'individual_tax_amount': $scope.tax_amt_model,
			  'stk_regtr_pageno': $scope.stk_regtr_pageno_model,
			  /*'unit_name': $scope.unit_select_model.unit_name,*/
			  'unit_id': $scope.unit_select_model,
			  'item_total': $scope.item_total,
			  'warranty_todate': $scope.warrantytodate,
			};
			$scope.details.unshift($scope.detail_row); //it will insert at the begining of an array
			$scope.grand_total=$scope.grand_total+$scope.item_total;
			//clear all after add...
			$scope.detailBtnTxt = "Add";
			$scope.selected_detail_id_for_detail=$scope.maincat_select_model=$scope.qty_model=$scope.desc_model=$scope.unit_price_model=$scope.indivi_discount_model=$scope.tax_percent_model=$scope.tax_amt_model=$scope.stk_regtr_pageno_model=$scope.unit_select_model=$scope.selectedItem=$scope.warranty_todate_model="";
			$scope.index = $scope.all_items.indexOf($scope.selectedItem); //splice the item from all_items
  			$scope.all_items.splice($scope.index, 1);
			$scope.clearDetailClicked();
		} //add new detail end
		else{ //update detail
			if($scope.warranty_todate_model == null) //this field also can be null.
				$scope.warrantytodate = null;
			else
				$scope.warrantytodate = $scope.warranty_todate_model;
			for (var i = 0; i < $scope.details.length; i++) {
		  		if($scope.details[i].detail_id == $scope.selected_detail_id_for_detail){
					$scope.details[i].maincat_id = $scope.maincat_select_model;
					if(typeof($scope.selectedItem) == 'object'){
						if($scope.details[i].item_id != $scope.selectedItem.item_id){
							$scope.index = $scope.all_items.indexOf($scope.selectedItem); //splice the item from all_items
	  						$scope.all_items.splice($scope.index, 1);
							/*$scope.detail_row = {
									  'item_name': $scope.details[i].item_name,
									  'item_id': $scope.details[i].item_id,
									  'model_code': "",
							};
							$scope.all_items.push($scope.detail_row);*/
							//push the item to typehead...
							for(var j=0;j<$scope.all_itemsbackup.length;j++){
								if($scope.all_itemsbackup[j].item_id == $scope.details[i].item_id)
								  	$scope.all_items.push($scope.all_itemsbackup[j]);
							}
						}
						$scope.details[i].item_name = $scope.selectedItem.item_name;
						$scope.details[i].item_id = $scope.selectedItem.item_id;
					}
					/*$scope.details[i].supplier_name = $scope.selectedSupplier.supplier_name;
					$scope.details[i].supplier_id = $scope.selectedSupplier.supplier_id;*/
					$scope.details[i].quantity = $scope.qty_model;
					$scope.details[i].description = $scope.desc_model;
					$scope.details[i].unit_price = $scope.unit_price_model;
					$scope.details[i].individual_discount = $scope.indivi_discount_model;
					$scope.details[i].individual_tax_percentage = $scope.tax_percent_model;
					$scope.details[i].individual_tax_amount = $scope.tax_amt_model;
					$scope.details[i].stk_regtr_pageno = $scope.stk_regtr_pageno_model;
					$scope.details[i].unit_id = $scope.unit_select_model;
					$scope.details[i].item_total = $scope.item_total;
					$scope.details[i].warranty_todate = $scope.warrantytodate;//$scope.warranty_todate_model;
					break;
				}
			}
			$scope.clearDetailClicked();
		} //update detail end
	}

	//delete unwanted details...
	$scope.detailDeleteClicked = function(detail_obj){
		//notify user that you are deleting the record.
		if (confirm("You are going to delete the record.") == true) {
			console.log("pressed ok so execute delete.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}
		$scope.index = $scope.details.indexOf(detail_obj);
  		$scope.details.splice($scope.index, 1);
		if($scope.details.length == 0)
			$scope.detailTablePart = false;
		$scope.grand_total = $scope.grand_total - detail_obj.item_total;
		//$scope.grand_total=$scope.grand_total-((detail_obj.quantity * detail_obj.unit_price)-detail_obj.individual_discount+ detail_obj.individual_tax_amount);
		/*$scope.detail_row = {
				  'item_name': detail_obj.item_name,
				  'item_id': detail_obj.item_id,
				  'model_code': "",
		};
		$scope.all_items.push($scope.detail_row);*/
		//push the item to typehead...
		for(var j=0;j<$scope.all_itemsbackup.length;j++){
			if($scope.all_itemsbackup[j].item_id == detail_obj.item_id)
			  	$scope.all_items.push($scope.all_itemsbackup[j]);
		}
		$scope.clearDetailClicked();	
	}

	$scope.detailTableRowClicked = function(detail_obj,index_value){
		$scope.detailBtnTxt = "Update";
		$scope.selected_detail_id_for_detail = index_value;
		$scope.selectedRowID = index_value;
		$scope.maincat_select_model = detail_obj.maincat_id;
		$scope.qty_model = parseFloat(detail_obj.quantity);
		$scope.desc_model = detail_obj.description;
		$scope.unit_price_model = parseFloat(detail_obj.unit_price);
		$scope.indivi_discount_model = parseFloat(detail_obj.individual_discount);
		$scope.tax_percent_model = detail_obj.individual_tax_percentage;
		$scope.tax_amt_model = parseFloat(detail_obj.individual_tax_amount);
		$scope.stk_regtr_pageno_model = detail_obj.stk_regtr_pageno;
		$scope.unit_select_model = detail_obj.unit_id;
		$scope.warranty_todate_model = detail_obj.warranty_todate;
		//$scope.item_total=(convertToProper(parseFloat(detail_obj.quantity))*convertToProper(parseFloat(detail_obj.unit_price)))-convertToProper(parseFloat(detail_obj.individual_discount))+convertToProper(parseFloat(detail_obj.individual_tax_amount));

		/*for (var i = 0; i < $scope.all_suppliers.length; i++) { //the object corresponds to the supplier_id is assigned to typeahead
  			if($scope.all_suppliers[i].supplier_id == detail_obj.supplier_id){
				$scope.selectedSupplier = $scope.all_suppliers[i];
				break;
			}
		}*/
		for (var i = 0; i < $scope.all_items.length; i++) { //the object corresponds to the item_id is assigned to typeahead
  			if($scope.all_items[i].item_id == detail_obj.item_id){
				$scope.selectedItem = $scope.all_items[i];
				break;
			}
		}
		$scope.selectedItem = detail_obj.item_name;
	}

	$scope.clearDetailClicked = function(){
		$scope.detailBtnTxt = "Add";
		$scope.selectedRowID = null;
		$scope.selected_detail_id_for_detail=$scope.maincat_select_model=$scope.qty_model=$scope.desc_model=$scope.unit_price_model=$scope.indivi_discount_model=$scope.tax_percent_model=$scope.tax_amt_model=$scope.stk_regtr_pageno_model=$scope.unit_select_model=$scope.selectedItem=$scope.warranty_todate_model="";
	}

	//converting textbox values to proper eliminate NaN type null etc...
	$scope.convertToProper = function(source_value){
		if(isNaN(source_value) || (source_value=="") || (source_value==null)){ //check whether the value in the textbox is not a number
			source_value=0;
		}
		return source_value;
	}
	//converting end...

	//rounding to next int...
	$scope.roundToInt = function(source_value){
		return Math.round(source_value);
	}

	$scope.calTaxAmt = function(){
		$scope.tax_amt_model=($scope.convertToProper($scope.qty_model)*$scope.convertToProper($scope.unit_price_model))*$scope.convertToProper($scope.tax_percent_model)/100;
	}

	$scope.storeValuesTemporarily = function(){
		//main data values...
		$rootScope.pinvoice_no_model = $scope.invoice_no_model;
		$rootScope.pinvoice_date_model = $scope.invoice_date_model;
		$rootScope.ppurchase_date_model = $scope.purchase_date_model;
		$rootScope.ptot_price_model = $scope.tot_price_model;
		$rootScope.ptot_tax_model = $scope.tot_tax_model;
		$rootScope.pnet_amount_model = $scope.net_amount_model;
		$rootScope.ptot_discount_model = $scope.tot_discount_model;
		/*$rootScope.pentered_date_model = $scope.entered_date_model;*/
		$rootScope.pselectedSupplier = $scope.selectedSupplier;
		//details values...
		$rootScope.pdetailBtnTxt = $scope.detailBtnTxt;
		$rootScope.pselected_detail_id_for_detail = $scope.selected_detail_id_for_detail;
		$rootScope.pselectedRowID = $scope.selectedRowID;
		$rootScope.pdetails = $scope.details.slice(0); //it will copy the array "details" to pdetails
		//$rootScope.pitem_total = $scope.item_total;
		$rootScope.pgrand_total = $scope.grand_total;
		$rootScope.pdetailTablePart = $scope.detailTablePart;
		$rootScope.pmaincat_select_model = $scope.maincat_select_model;
		$rootScope.pqty_model = $scope.qty_model;
		$rootScope.pdesc_model = $scope.desc_model;
		$rootScope.punit_price_model = $scope.unit_price_model;
		$rootScope.pindivi_discount_model = $scope.indivi_discount_model;
		$rootScope.ptax_percent_model = $scope.tax_percent_model;
		$rootScope.ptax_amt_model = $scope.tax_amt_model;
		$rootScope.pstk_regtr_pageno_model = $scope.stk_regtr_pageno_model;
		$rootScope.punit_select_model = $scope.unit_select_model;
		$rootScope.pwarranty_todate_model = $scope.warranty_todate_model;
	}

	$scope.addNewSupplierClicked = function(){
		$rootScope.showSupplierBack = true; //show back button in item registration page
		$rootScope.navigateStartedFlag = true;
		$scope.storeValuesTemporarily();
		$rootScope.pselectedItem = $scope.selectedItem;
	}

	$scope.addNewItemClicked = function(){
		$rootScope.showItemBack = true; //show back button in item registration page
		$rootScope.navigateStartedFlag = true;
		$scope.storeValuesTemporarily();
		//$rootScope.pselectedSupplier = $scope.selectedSupplier;
	}

	//submit purchase start...
	$scope.purchaseSubmit = function(){
		if($scope.details.length < 1){
			notifyMessage('fa fa-exclamation-triangle',"<b>Detail Required</b><br>Atleast one purchase detail must be required.",'warning');
			return;
		}
		var jsonAllDetails=angular.toJson($scope.details);
		if($scope.delButton == false){ //for purchase submit
			$http({
								method : "POST",
								url : "purchaseSubmit",
								data: {invoice_no:$scope.invoice_no_model, invoice_date:$scope.invoice_date_model, purchase_date:$scope.purchase_date_model, total_price:$scope.tot_price_model, total_tax:$scope.tot_tax_model, net_amount:$scope.net_amount_model, total_discount:$scope.tot_discount_model, /*entered_date:$scope.entered_date_model,*/ supplier_id:$scope.selectedSupplier.supplier_id, jsonDetails:jsonAllDetails}
							}).then(function mySucces(response) {
								if(response.data[0].status == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
									$scope.delButton = false;
									$scope.all_purchases.push(response.data[0]);			
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
								}
							}, function myError(response) {

			});
			$scope.purchaseClearClicked();
			//load the initial parameters...
			$http({
					method : "POST",
					url : "purchaseParams"
				}).then(function mySucces(response) {
					$scope.maincats = response.data.stkMainCategory;
					$scope.all_items = response.data.stkItemMaster;
					$scope.all_suppliers = response.data.stkSupplier;
					$scope.units = response.data.stkUnits;
				}, function myError(response) {

			});//initial parameter loading end...
		}
		else{ //purchase update
			$http({
								method : "POST",
								url : "purchaseUpdate",
								data: {purchase_id:$scope.selected_purchaseid,invoice_no:$scope.invoice_no_model, invoice_date:$scope.invoice_date_model, purchase_date:$scope.purchase_date_model, total_price:$scope.tot_price_model, total_tax:$scope.tot_tax_model, net_amount:$scope.net_amount_model, total_discount:$scope.tot_discount_model, /*entered_date:$scope.entered_date_model,*/ supplier_id:$scope.selectedSupplier.supplier_id, jsonDetails:jsonAllDetails}
							}).then(function mySucces(response) {
								if(response.data[0].status == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
									//$scope.delButton = false;
									//$scope.btnTxt = "Save";
									//$scope.all_purchases.push(response.data[0]);
									$scope.loadtabledata();
									/*for (var j = 0; j < $scope.all_purchases.length; j++) {
						  				if($scope.all_purchases[j].purchaseid == $scope.selected_purchaseid){
											$scope.all_purchases[j].totprice = $scope.tot_price_model;
											$scope.all_purchases[j].tottax = $scope.tot_tax_model;
											$scope.all_purchases[j].netamount = $scope.net_amount_model;
											$scope.all_purchases[j].totdiscount = $scope.tot_discount_model;
											$scope.all_purchases[j].invoiceno = $scope.invoice_no_model;
											$scope.all_purchases[j].invoicedate = $scope.invoice_date_model;
											$scope.all_purchases[j].purchasedate = $scope.purchase_date_model;
											$scope.all_purchases[j].supplierid = $scope.selectedSupplier.supplier_id;
											$scope.all_purchases[j].suppliername = $scope.selectedSupplier.supplier_name;
											//$scope.det_id = 0;
											for(var i=0;i < $scope.all_purchases[j].purchaseInfo.length;i++){
												//$scope.all_purchases[j].purchaseInfo[i].recordid = $scope.det_id;
												//$scope.det_id = $scope.det_id + 1;
												$scope.all_purchases[j].purchaseInfo[i].description = $scope.details[i].description;
												$scope.all_purchases[j].purchaseInfo[i].quantity = $scope.details[i].quantity;
												$scope.all_purchases[j].purchaseInfo[i].unitprice = $scope.details[i].unit_price;
												$scope.all_purchases[j].purchaseInfo[i].individualdiscount = $scope.details[i].individual_discount;
												$scope.all_purchases[j].purchaseInfo[i].individualtaxpercentage = $scope.details[i].individual_tax_percentage;
												$scope.all_purchases[j].purchaseInfo[i].individualtaxamount = $scope.details[i].individual_tax_amount;
												$scope.all_purchases[j].purchaseInfo[i].stkregtrpageno = $scope.details[i].stk_regtr_pageno;
												$scope.all_purchases[j].purchaseInfo[i].unitid = $scope.details[i].unit_id;
												for(var k=0;k < $scope.units.length;k++){
													if($scope.units[k].unit_id == $scope.details[i].unit_id){
														$scope.all_purchases[j].purchaseInfo[i].unitname = $scope.units[k].unit_name;
													}
												}
												$scope.all_purchases[j].purchaseInfo[i].itemid = $scope.details[i].item_id;
												$scope.all_purchases[j].purchaseInfo[i].itemname = $scope.details[i].item_name;
												$scope.all_purchases[j].purchaseInfo[i].maincatid = $scope.details[i].maincat_id;
												for(var k=0;k < $scope.maincats.length;k++){
													if($scope.maincats[k].maincat_id == $scope.details[i].maincat_id){
														$scope.all_purchases[j].purchaseInfo[i].maincatname = $scope.maincats[k].maincat_name;
													}
												}
												$scope.all_purchases[j].purchaseInfo[i].itemtotal = $scope.details[i].item_total;
												$scope.all_purchases[j].purchaseInfo[i].warrantytodate = $scope.details[i].warranty_todate;
											}
											break;
										}
									}//for loop end		*/		
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
								}
							}, function myError(response) {

			});	
			$scope.purchaseClearClicked();
			//load the initial parameters...
			$http({
					method : "POST",
					url : "purchaseParams"
				}).then(function mySucces(response) {
					$scope.maincats = response.data.stkMainCategory;
					$scope.all_items = response.data.stkItemMaster;
					$scope.all_suppliers = response.data.stkSupplier;
					$scope.units = response.data.stkUnits;
				}, function myError(response) {

			});//initial parameter loading end...
		}
	}//purchase submit end...

	//table row clicked...
	$scope.purchaseTableRowClicked = function(purchase_obj){
		$scope.selectedPID = purchase_obj.purchaseid; //to make table selection hilight
		$scope.delButton = true; //show delete button
		$scope.btnTxt = "Update";
		$scope.selected_purchaseid = purchase_obj.purchaseid;
		$scope.clearDetailClicked(); //clear all controls in details part
		//$scope.details = purchase_obj.purchaseInfo.slice(0);
		$scope.invoice_no_model=purchase_obj.invoiceno;
		$scope.invoice_date_model=purchase_obj.invoicedate;
		$scope.purchase_date_model=purchase_obj.purchasedate;
		$scope.tot_price_model=parseFloat(purchase_obj.totprice);
		$scope.tot_tax_model=parseFloat(purchase_obj.tottax);
		$scope.net_amount_model=parseFloat(purchase_obj.netamount);
		$scope.tot_discount_model=parseFloat(purchase_obj.totdiscount);
		//$scope.selectedSupplier.supplier_id=purchase_obj.supplierid;
		for (var i = 0; i < $scope.all_suppliers.length; i++) { //the object corresponds to the model_id is assigned to typeahead
	  		if($scope.all_suppliers[i].supplier_id == purchase_obj.supplierid){
				$scope.selectedSupplier = $scope.all_suppliers[i];
				break;
			}
		}
		$scope.details = [];
		$scope.item_total = 0;
		$scope.grand_total = 0;
		$scope.all_items = $scope.all_itemsbackup.slice(0) //will copy all_itemsbackup to all_items
		$scope.det_id = 0;
		for(i=0;i < purchase_obj.purchaseInfo.length;i++){
			$scope.detail_row = {
				  'detail_id': $scope.det_id, //not using this field
				  'maincat_id': purchase_obj.purchaseInfo[i].maincatid,
				  'item_name': purchase_obj.purchaseInfo[i].itemname,
				  'item_id': purchase_obj.purchaseInfo[i].itemid,
				  'supplier_name': purchase_obj.suppliername,
				  'supplier_id': purchase_obj.supplierid,
				  'quantity': parseFloat(purchase_obj.purchaseInfo[i].quantity),
				  'description': purchase_obj.purchaseInfo[i].description,
				  'unit_price': parseFloat(purchase_obj.purchaseInfo[i].unitprice),
				  'individual_discount': parseFloat(purchase_obj.purchaseInfo[i].individualdiscount),
				  'individual_tax_percentage': purchase_obj.purchaseInfo[i].individualtaxpercentage,
				  'individual_tax_amount': purchase_obj.purchaseInfo[i].individualtaxamount,
				  'stk_regtr_pageno': purchase_obj.purchaseInfo[i].stkregtrpageno,
				  /*'unit_name': $scope.unit_select_model.unit_name,*/
				  'unit_id': purchase_obj.purchaseInfo[i].unitid,
				  'item_total': parseFloat(purchase_obj.purchaseInfo[i].itemtotal), //fix as 2 decimal places
			  	  'warranty_todate': purchase_obj.purchaseInfo[i].warrantytodate,
			};
			$scope.details.push($scope.detail_row); //it will insert at the begining of an array
			$scope.grand_total = $scope.grand_total + parseFloat(purchase_obj.purchaseInfo[i].itemtotal)
			$scope.detailTablePart = true;
			$scope.det_id = $scope.det_id + 1;
			//splice already entered items from item typehead...
			for(var j=0;j<$scope.all_items.length;j++){
				if($scope.all_items[j].item_id == purchase_obj.purchaseInfo[i].itemid){
					$scope.index = $scope.all_items.indexOf($scope.all_items[j]); //splice the item from all_items
				  	$scope.all_items.splice($scope.index, 1);
				}
			}
			//alert(purchase_obj.purchaseInfo[i].itemname);
		}
		if($scope.details.length > 0)
			$scope.detailTablePart = true;
		//alert(purchase_obj.purchaseInfo[0].description);
	}

	$scope.purchaseClearClicked = function(){
		$scope.clearDetailClicked(); //clear all controls in details part
		$scope.details = [];
		$scope.detailTablePart=false;
		$scope.selectedPID = null;
		$scope.delButton = false;
		$scope.btnTxt = "Save";
		$scope.selected_purchaseid=$scope.invoice_no_model=$scope.invoice_date_model=$scope.purchase_date_model=$scope.tot_price_model=$scope.tot_tax_model=$scope.net_amount_model=$scope.tot_discount_model=$scope.selectedSupplier="";
		$scope.item_total=$scope.grand_total=0;
		//load the initial parameters...
		$http({
				method : "POST",
				url : "purchaseParams"
			}).then(function mySucces(response) {
				$scope.maincats = response.data.stkMainCategory;
				$scope.all_items = response.data.stkItemMaster;
				$scope.all_suppliers = response.data.stkSupplier;
				$scope.units = response.data.stkUnits;
			}, function myError(response) {

		});//initial parameter loading end...
	}

	$scope.purchaseDelete = function(){
		//notify user that you are deleting the record.
		if (confirm("You are going to delete the record.") == true) {
			console.log("pressed ok so execute delete.");
		} else {
			console.log("pressed cancel so return.");
			return;
		}

		//delete http start...
		$http({
				method : "POST",
				url : "purchaseDelete",
				data: {purchase_id: $scope.selected_purchaseid}
			}).then(function mySucces(response) {
				if(response.data == "success"){
					notifyMessage('fa fa-check-circle',"<b>Success</b><br>Purchase Deleted Successfully.",'info');
					$scope.loadtabledata();
					/*for (var i = 0; i < $scope.all_purchases.length; i++) {
						if($scope.all_purchases[i].purchaseid == $scope.selected_purchaseid){
							$scope.index = $scope.all_purchases.indexOf($scope.all_purchases[i]);
  							$scope.all_purchases.splice($scope.index, 1);
							break;
						}
					}*/
				}
				else if(response.data == "depent"){
					notifyMessage('',"<b>Failed</b><br>Record can't be deleted. Have dependent entries.",'danger');
				}
				else{
					notifyMessage('',"<b>Failed</b><br>Record can't be deleted."+response.data,'danger');
				}
			}, function myError(response) {

		});//delete http end...
		$scope.purchaseClearClicked();
	}

	//function check whether an item is already inserted into the list...
	$scope.checkItemExistence = function(item_id){
		if($scope.insertedItems.indexOf(item_id) !== -1)
			return false; //existing item no need to include in ng-repeat
		else
			return true; //not already added, so it must included in ng-repeat
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
	$scope.customFilterForSupplier = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['supplier_name'];
		
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
	$scope.customFilterForPurchase = function (searchText) {
	  function comparator(a, b) {
		return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
	  }

	  var lookInKeys = ['invoiceno','invoicedate','netamount','suppliername','purchasedate'];
		
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

});//purchase ctrl end...

























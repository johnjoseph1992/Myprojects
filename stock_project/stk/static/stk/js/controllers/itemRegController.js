//ctrl begin...
	app.controller("itemRegCtrl", function($scope, $http, $anchorScroll, $location, $rootScope, $window, $document) {

		$scope.searchBrandText = "";
		$scope.all_models = [];
		$scope.all_items = [];
		$scope.subitem_check_submit_model = false; //checkbox initially false
		$scope.bcode_disabled = false; //initially brand code not disabled
		$scope.delButton = false;
		$scope.selectedID = null;
		$scope.btnTxt = "Save";
		$scope.autocompleteSelectedBrandId = null;
		$scope.temp_model_name = "";
		$scope.loadingPart = true;
		$scope.nodataPart = false;
		$scope.filtereditems = [];
		$rootScope.newall_items = [];


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
		$scope.$on('itemNgRepeatFinished', function(ngRepeatFinishedEvent) { //worked when ng-repeat finished.(on-finish-render="..ngRepeatFinished")
			$scope.loadingPart = false;
		});

		//function to clear all controls to default values...
		$scope.clearAll = function(){
			$scope.selectedBrand=$scope.bcode_submit_model=$scope.mcode_submit_model=$scope.selectedModel=$scope.info_submit_model=$scope.remark_submit_model=$scope.spec_submit_model = "";
			$scope.qty_submit_model=$scope.contents_submit_model = 0;
			$scope.subitem_check_submit_model = false; //clear checkbox to default
			$scope.all_brands = [];
			$scope.all_models = [];
			if(angular.isDefined($scope.unit_select_submit_model)){ //clearing the selection of unit select box
		        delete $scope.unit_select_submit_model;
		    }
			if(angular.isDefined($scope.type_select_submit_model)){ //clearing the selection of maincat select box
		        delete $scope.type_select_submit_model;
		    }
			if(angular.isDefined($scope.subcat_select_submit_model)){ //clearing the selection of subcat select box
		        delete $scope.subcat_select_submit_model;
		    }
		}	

		//load the selectbox...
		$http({
				method : "POST",
				url : "itemRegistrationParams"
			}).then(function mySucces(response) {
				//$scope.all_brands = response.data.stkBrandMaster;
				$scope.units = response.data.stkUnits;
				//$scope.all_models = response.data.stkModelMaster;
				$scope.subcats = response.data.stkSubCategory;
				$scope.firms = response.data.stkCompanyMaster;
				$scope.stores = response.data.stkStoreMaster;
				$scope.maincats = response.data.stkMainCategory;
				//for (var i = 0; i < $scope.units.length; i++) {
				  			//$scope.unit_select_submit_model = 2;
						//}
			}, function myError(response) {

		});//loading selectbox end...

		//function load the table with firm names...
		$scope.loadtabledata = function(){
			$http({
					method : "POST",
					url : "itemTableView"
				}).then(function mySucces(response) {
					$scope.all_items = response.data.stkItemMaster;
					if($scope.all_items.length == 0){
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
		console.log("ItemReg loadtime: " + (end-start) + " milliseconds");

		$scope.itemTypeSelected = function(){ //load all brands corresponding to selected item type [ie main category]
			//$scope.selectedBrand = "";
			$http({
					method : "POST",
					url : "brandsForMaincatId",	
					params: {maincat_id: $scope.type_select_submit_model}
				}).then(function mySucces(response) {
					$scope.all_brands = response.data.stkBrandMaster;
				}, function myError(response) {

			});
		}

		$scope.brandSelectChanged = function(){
				$scope.bcode_submit_model = $scope.selectedBrand.brand_code;
				if($scope.delButton == false) //if insert is going on then
					$scope.bcode_disabled = true; //brand code disabled
				else //update going on
					$scope.bcode_disabled = false; //brand code disabled
				//$scope.selectedModel = "";
				//load the selectbox with brand names...
				$http({
						method : "POST",
						url : "itemModelForBrand",
						params: {brand_id: $scope.selectedBrand.brand_id}
					}).then(function mySucces(response) {
						$scope.all_models = response.data.stkModelMaster;
					}, function myError(response) {

				});//loading selectbox end...
		}	

		$scope.modelSelectChanged = function(){
			if(typeof($scope.selectedBrand) && typeof($scope.selectedModel) == 'object'){
				notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.selectedBrand.brand_name+" "+$scope.selectedModel.model_name+" already existing.",'warning');
				return;
			}
		}

		$scope.brandTextChanged = function(){
			if(typeof($scope.selectedBrand) != 'object'){ //clear model array if no brands selected
				$scope.all_models = "";
				$scope.bcode_submit_model = "";
				$scope.bcode_disabled = false; //make brand code not disabled
			}
		}

		//item submit start...
		$scope.itemSubmit = function(){
			if($scope.delButton == false){ //condition for new item submit...
				if(typeof($scope.selectedBrand) && typeof($scope.selectedModel) == 'object'){ //if both exists show error
					notifyMessage('fa fa-exclamation-triangle',"<b>Existing</b><br>"+$scope.selectedBrand.brand_name+" "+$scope.selectedModel.model_name+" already existing.",'warning');
					return;
				}
				if(typeof($scope.selectedBrand) == 'object') //adjust according to existing or non existing[ get brand name]
					$scope.brand_name = $scope.selectedBrand.brand_name;
				else
					$scope.brand_name = $scope.selectedBrand;

				$http({
							method : "POST",
							url : "itemSubmit",
							params: {brand_name: $scope.brand_name, model_name:$scope.selectedModel, brand_code:$scope.bcode_submit_model,model_code:$scope.mcode_submit_model, product_info:$scope.info_submit_model, remark:$scope.remark_submit_model, specification:$scope.spec_submit_model, is_subitem:$scope.subitem_check_submit_model, qty_available:$scope.qty_submit_model, no_of_contents:$scope.contents_submit_model, unit_id:$scope.unit_select_submit_model, subcat_id:$scope.subcat_select_submit_model,/* firm_id:$scope.firm_select_submit_model, store_id:$scope.store_select_submit_model, */maincat_id:$scope.type_select_submit_model}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data[0].status == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Saved Successfully.",'info');
									$scope.delButton = false;
									//add inserted item to tableview...
									$scope.list_row_to_push = {
									  'item_id': response.data[0].item_id,
									  'qty_available': response.data[0].qty_available,
									  'no_of_contents': response.data[0].no_of_contents,
									  'whether_subitem': response.data[0].whether_subitem,
									  'unit_id': response.data[0].unit_id,
									  'unit_name': response.data[0].unit_name,
									  'subcat_id': response.data[0].subcat_id,
									  'subcat_name': response.data[0].subcat_name,
									  'firm_id': response.data[0].firm_id,
									  'firm_name': response.data[0].firm_name,
									  'maincat_id': response.data[0].maincat_id,
									  'maincat_name': response.data[0].maincat_name,
									  'store_id': response.data[0].store_id,
									  'mainstore_name': response.data[0].mainstore_name,
									  'model_id': response.data[0].model_id,
									  'model_name': response.data[0].model_name,
									  'model_code': response.data[0].model_code,
									  'specification': response.data[0].specification,
									  'product_info': response.data[0].product_info,
									  'remarks': response.data[0].remarks,
									  'brand_id': response.data[0].brand_id,
									  'brand_name': response.data[0].brand_name,
									  'brand_code': response.data[0].brand_code,
									};
									$scope.all_items.push($scope.list_row_to_push);
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to save data."+response.data,'danger');
								}
							}, function myError(response) {
							  //$scope.myResponse = response.statusText;
						});
			}
			else{ //condition for item update... [$scope.delButton == true]
				if(typeof($scope.selectedBrand) == 'object'){ //then need to update brand code of autocomplete selected brand and brandid_id of product model
					$scope.brand_name = $scope.selectedBrand.brand_name;
					$scope.autocompleteSelectedBrandId = $scope.selectedBrand.brand_id;
				}
				else{ //if not object then update brand_name,brandcode of selected brand from tableview
					$scope.brand_name = $scope.selectedBrand.brand_name;
					$scope.autocompleteSelectedBrandId = $scope.selected_brand_id;
				}

				if(typeof($scope.selectedModel) == 'object') //then need to update brand code of autocomplete selected brand and brandid_id of product model
					$scope.temp_model_name = $scope.selectedModel.model_name;
				else
					$scope.temp_model_name = $scope.selectedModel;
				
				//http update start...
				$http({
							method : "POST",
							url : "itemUpdate",
							params: {brand_name: $scope.brand_name, model_name:$scope.temp_model_name, brand_code:$scope.bcode_submit_model,model_code:$scope.mcode_submit_model, product_info:$scope.info_submit_model, remark:$scope.remark_submit_model, specification:$scope.spec_submit_model, is_subitem:$scope.subitem_check_submit_model, qty_available:$scope.qty_submit_model, no_of_contents:$scope.contents_submit_model, unit_id:$scope.unit_select_submit_model, subcat_id:$scope.subcat_select_submit_model,maincat_id:$scope.type_select_submit_model, brand_id:$scope.autocompleteSelectedBrandId, model_id:$scope.selected_model_id, item_id:$scope.selected_item_id}

						  }).then(function mySucces(response) {
							 // $scope.myResponse = response.data;
								if(response.data == "success"){
									notifyMessage('fa fa-check-circle',"<b>Success</b><br>Data Updated Successfully.",'info');
									$scope.delButton = false;
									$scope.btnTxt = "Save";
									//reflect new values in client side table view...
									for (var i = 0; i < $scope.all_items.length; i++) {
								  		if($scope.all_items[i].item_id == $scope.selected_item_id){
											$scope.all_items[i].brand_name = $scope.brand_name;
											$scope.all_items[i].brand_code = $scope.bcode_submit_model;
											$scope.all_items[i].brand_id = $scope.autocompleteSelectedBrandId;
											$scope.all_items[i].model_id = $scope.selected_model_id;
											$scope.all_items[i].model_name = $scope.temp_model_name;
											$scope.all_items[i].model_code = $scope.mcode_submit_model;
											$scope.all_items[i].qty_available = $scope.qty_submit_model;
											$scope.all_items[i].no_of_contents = $scope.contents_submit_model;
											$scope.all_items[i].specification = $scope.spec_submit_model;
											$scope.all_items[i].product_info = $scope.info_submit_model;
											$scope.all_items[i].remarks = $scope.remark_submit_model;
											$scope.all_items[i].whether_subitem = ($scope.subitem_check_submit_model ? 'Y':'N');
											$scope.all_items[i].maincat_id = $scope.type_select_submit_model;
											for (var j = 0; j < $scope.maincats.length; j++) { //get maincat name corresponds to the maincat_id
								  				if($scope.maincats[j].maincat_id == $scope.type_select_submit_model){
													$scope.all_items[i].maincat_name = $scope.maincats[j].maincat_name;
													break;
												}
											}
											$scope.all_items[i].subcat_id = $scope.subcat_select_submit_model;
											for (var j = 0; j < $scope.subcats.length; j++) { //get subcat name corresponds to the subcat_id
								  				if($scope.subcats[j].subcat_id == $scope.subcat_select_submit_model){
													$scope.all_items[i].subcat_name = $scope.subcats[j].subcat_name;
													break;
												}
											}
											$scope.all_items[i].unit_id = $scope.unit_select_submit_model;
											for (var j = 0; j < $scope.units.length; j++) { //get unit name corresponds to the unit_id
								  				if($scope.units[j].unit_id == $scope.unit_select_submit_model){
													$scope.all_items[i].unit_name = $scope.units[j].unit_name;
													break;
												}
											}
											break;
										}
									}
								}
								else if(response.data=="counterror"){
									notifyMessage('',"<b>Failed</b><br>Already have more registered items.",'warning');
								}
								else{
									notifyMessage('',"<b>Failed</b><br>Failed to update data."+response.data,'danger');
								}
							}, function myError(response) {
							  //$scope.myResponse = response.statusText;
						});	//http update end...

			} //delbutton else end
		}//item submit end...

		$scope.itemTableRowClicked = function(item_obj){
			//$location.hash('scrollToTopDivID'); //scrolling to top
			//$anchorScroll(); //scrolling to top
			$scope.delButton = true; //show delete button
			$scope.btnTxt = "Update";
			$scope.bcode_disabled = false; //brand code disabled
			$scope.selectedID = item_obj.item_id; //to make table selection hilight
			$scope.selected_item_id = item_obj.item_id;
			$scope.selected_brand_id = item_obj.brand_id;
			$scope.selected_model_id = item_obj.model_id;
			$scope.type_select_submit_model = item_obj.maincat_id;
			$scope.bcode_submit_model = item_obj.brand_code;
			$scope.mcode_submit_model = item_obj.model_code;
			$scope.unit_select_submit_model = item_obj.unit_id;
			$scope.qty_submit_model = item_obj.qty_available;
			$scope.contents_submit_model = item_obj.no_of_contents;
			$scope.subcat_select_submit_model = item_obj.subcat_id;
			$scope.info_submit_model = item_obj.product_info;
			$scope.remark_submit_model = item_obj.remarks;
			$scope.spec_submit_model = item_obj.specification;
			if(item_obj.whether_subitem == "Y")
				$scope.subitem_check_submit_model = true;
			else
				$scope.subitem_check_submit_model = false;				
			//load brands corresponds to maincat_id...
			$http({
					method : "POST",
					url : "brandsForMaincatId",	
					params: {maincat_id: item_obj.maincat_id}
				}).then(function mySucces(response) {
					$scope.all_brands = response.data.stkBrandMaster;
					for (var i = 0; i < $scope.all_brands.length; i++) { //the object corresponds to the brand_id is assigned to typeahead
				  			if($scope.all_brands[i].brand_id == item_obj.brand_id){
								$scope.selectedBrand = $scope.all_brands[i];
								break;
							}
					}
				}, function myError(response) {

			});
			//load the selectbox with model names...
			$http({
					method : "POST",
					url : "itemModelForBrand",
					params: {brand_id: item_obj.brand_id}
				}).then(function mySucces(response) {
					$scope.all_models = response.data.stkModelMaster;
					for (var i = 0; i < $scope.all_models.length; i++) { //the object corresponds to the model_id is assigned to typeahead
				  			if($scope.all_models[i].model_id == item_obj.model_id){
								$scope.selectedModel = $scope.all_models[i];
								break;
							}
					}
				}, function myError(response) {

			});//loading selectbox end...
		}//table row clicked end

		$scope.cancelClicked = function(){
			$scope.delButton = false; //hide delete button
			$scope.btnTxt = "Save";
			$scope.bcode_disabled = false; //brand code disabled
			$scope.selectedID = null; //remove table selection		
			$scope.clearAll(); //clear all controls to default values	
		}

		//delete button click...
		$scope.itemDelete = function(){
			$http({
					method : "POST",
					url : "itemDelete",
					params: {item_id: $scope.selected_item_id, model_id:$scope.selected_model_id}
				}).then(function mySucces(response) {
					if(response.data == "success"){
						notifyMessage('fa fa-check-circle',"<b>Success</b><br>Item Deleted Successfully.",'info');
						$scope.cancelClicked();
						for (var i = 0; i < $scope.all_items.length; i++) { //the object corresponds to the model_id is assigned to typeahead
				  			if($scope.all_items[i].item_id == $scope.selected_item_id){
								$scope.index = $scope.all_items.indexOf($scope.all_items[i]);
  								$scope.all_items.splice($scope.index, 1);
								break;
							}
						}
					}
					else{
						notifyMessage('',"<b>Failed</b><br>Item can't be deleted."+response.data,'danger');
					}
				}, function myError(response) {

			});
		}//delete click end

		//when back button clicked...
		$scope.backToPrevous = function(){
			$rootScope.showItemBack = false;
			$window.history.back(); //back to previous page
		}

		/*$scope.scrollToTableViewOnSearchChange = function(){ //focus on table view after each searching
			if(angular.isDefined($scope.search_model)){
				$location.hash('tabViewDiv'); //scrolling to tableview
				$anchorScroll(); //scrolling to tableview
			}
		}*/

		//custom filter start...
		$scope.customFilterForBrand = function (searchText) {
		  function comparator(a, b) {
			return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
		  }

		  var lookInKeys = ['brand_name', 'brand_code'];

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
		$scope.customFilterForTableView = function (searchText) {
		  function comparator(a, b) {
			return (''+a).toLowerCase().indexOf((''+b).toLowerCase()) > -1;
		  }

		  var lookInKeys = ['brand_name', 'model_name','maincat_name','subcat_name','qty_available','no_of_contents','unit_name'];
			
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

		//function for printing the report to hard copy...
		$scope.openPrintPopupWindow = function () {
			var jsonAllDetails=angular.toJson($scope.filtereditems);
			$scope.headingdata = "ALL ITEM REGISTRATION DETAILS"
            $scope.newWin=$window.open('itemRegistrationPreview?headingdata=' + $scope.headingdata +'&&jsondata=' +jsonAllDetails, '_blank', 'toolbar=no,location=no,statusbar=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600');
			//$scope.newWin.document.write('#itemdetails');
			//$scope.newWin.print();
        }

		/*$scope.getPrint = function(){
			newWin= window.open('report/print_preview.html','_blank','toolbar=no,location=no,statusbar=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600');

			newWin.document.write("<style>#OUTAttendancePrintReportStudentListTable { width:100%; font-size:11px;   border-collapse: collapse;}#OUTAttendancePrintReportStudentListTable th{background-color: white;    border: 1px solid #0097c8;    color:black;}#OUTAttendancePrintReportStudentListTable td{    border: 1px solid #000;}</style><center><div align='center' style='width:595px;' > <span style='font-size:15px'>"+html[0]['campusname']+"("+html[0]['campuscode']+")<sup style='font-size:12px'>TM</sup></span><br/><span style='font-size:12px'>"+html[0]['address1']+" , "+html[0]['address2']+" , "+html[0]['address3']+"</span></span><span style='font-size:12px'>, PIN-"+html[0]['pin']+", Phone"+html[0]['phone']+" </span><br/><br/><span style='font-size:15px'>SUBJECTWISE ATTENDANCE REPORT</span><br/><span style='font-size:12px'> Subject: "+sub[0]['subjectdesc']+" Batch :"+bat[0]['batchcode']+"</span><br/>"+$("#OUTAttendancePrintReportStudentListDiv").html()+"</div></center>");
			   newWin.window.print();
		}

		$scope.getPdfFromJson = function(){
				var item = {
				  "Name" : "XYZ",
				  "Age" : "22",
				  "Gender" : "Male"
				};
				var doc = new jsPDF();
				var col = ["Details", "Values"];
				var rows = [];

				for(var key in item){
					var temp = [key, item[key]];
					rows.push(temp);
				}

				doc.autoTable(col, rows);

				doc.save('Test.pdf');
		}

		//////////////////get pdf start...
		$scope.getPDF = function() {
			var pdf = new jsPDF('p', 'pt','a4', 'letter');
			// source can be HTML-formatted string, or a reference
			// to an actual DOM element from which the text will be scraped.
			source = $('#itemdetails')[0];

			// we support special element handlers. Register them with jQuery-style 
			// ID selector for either ID or node name. ("#iAmID", "div", "span" etc.)
			// There is no support for any other type of selectors 
			// (class, of compound) at this time.
			specialElementHandlers = {
				// element with id of "bypass" - jQuery style selector
				'#bypassme': function (element, renderer) {
				    // true = "handled elsewhere, bypass text extraction"
				    return true
				}
			};
		

			margins = {
				top: 80,
				bottom: 60,
				left: 40,
				width: 522
			};

			// all coords and widths are in jsPDF instance's declared units
			// 'inches' in this case
			pdf.fromHTML(
			source, // HTML string or DOM elem ref.
			margins.left, // x coord
			margins.top, { // y coord
				'width': margins.width, // max width of content on PDF
				'elementHandlers': specialElementHandlers
			},

			function (dispose) {
				// dispose: object with X, Y of the last line add to the PDF 
				//          this allow the insertion of new lines after html
				pdf.save('itemdetails.pdf');
			}, margins);
		}
		//////////////////get pdf end...*/

		//reportlab pdf
		$scope.getPDF = function(){
				//alert();
				var json_items=angular.toJson($scope.filtereditems);
				$window.open("itemDetailsPdf?json_items="+ json_items);
		}
	
	});//ctrl end...


























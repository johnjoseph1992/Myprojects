app.controller("adminHomeCtrl", function($scope,$http,$interval,$rootScope) {
		
		$scope.home_data = [];//old...
		/*if(storeSelect == 0){
			$scope.store_select_part = true;
			$scope.home_part = false;
		}
		else{
			$scope.store_select_part = false;
	  	    $scope.home_part = true;
		}*/

		//checking whether store is selected...
			$http({
					method : "POST",
					url : "checkStoreSelected"
				}).then(function mySucces(response) {
					if(response.data[0].status == "success"){ //store already selected
						$scope.store_select_part = false;
	  	    			$scope.home_part = true;
						$rootScope.currentStore = response.data[0].storename //show after refresh
					}
					else{ //store not selected yet
						$scope.store_select_part = true;
						$scope.home_part = false;
					}
				}, function myError(response) {

				});//checking end...	

		//load the selectbox with dependent store names...
			$http({
					method : "POST",
					url : "selectStore"
				}).then(function mySucces(response) {
					$scope.stores = response.data.stkStoreMaster;
				}, function myError(response) {

				});//loading selectbox end...		

		$scope.selectStoreClicked = function(store_selected_value){
			
			$http({
					method : "POST",
					url : "confirmSelectedStore",
					params: {store_id: store_selected_value}

				  }).then(function mySucces(response) {
						notifyMessage('',"<b>Success</b><br>Store Selected Successfully.",'info');
						for(var i=0;i<$scope.stores.length;i++){
							if($scope.stores[i].storeid == store_selected_value){
								$rootScope.currentStore = $scope.stores[i].mainstorename;
								break;
							}
						}
						//$rootScope.currentStore = store_selected_value;
						$scope.store_select_part = false;
	  	 		        $scope.home_part = true;
						//storeSelect = 1;
					}, function myError(response) {
					 	notifyMessage('',"<b>Failed</b><br>Failed to select store.",'danger');
				});

		}

		/*//check session existance...
		$interval(function () {
			$http({
						method : "GET",
						url : "checkSession"
					}).then(function mySucces(response) {
						if(response.data=="success"){}
						else{
							window.location.replace("..");
						}
					
					}, function myError(response) {

			});
		}, 6000);
		//session end...


		//intially refresh the controls with the retrieved data on every specified delay time... 
		$http({
					method : "GET",
					url : "refreshAdminHome/"
				}).then(function mySucces(response) {
					$scope.home_data = response.data.AdminHomeData;
					//alert($scope.home_data[0].main_store_count);
					$scope.main_store_count_var = $scope.home_data[0].main_store_count;
					$scope.dept_count_var = $scope.home_data[0].dept_count;

					$scope.supplier_count_var = $scope.home_data[0].supplier_count;
					$scope.brand_count_var = $scope.home_data[0].brand_count;
					$scope.item_count_var = $scope.home_data[0].item_count;
					$scope.external_purchase_count_var = $scope.home_data[0].external_purchase_count;
					$scope.total_quotation_count_var = $scope.home_data[0].total_quotation_count;
					$scope.selected_quotation_count_var = $scope.home_data[0].selected_quotation_count;
					
				}, function myError(response) {

		});//refreshing end...


		$interval(function () {
     			
			//refresh the controls with the retrieved data on every specified delay time... 
			$http({
						method : "GET",
						url : "refreshAdminHome/"
					}).then(function mySucces(response) {
						$scope.home_data = response.data.AdminHomeData;
						//alert($scope.home_data[0].main_store_count);
						$scope.main_store_count_var = $scope.home_data[0].main_store_count;
						$scope.dept_count_var = $scope.home_data[0].dept_count;

						$scope.supplier_count_var = $scope.home_data[0].supplier_count;
						$scope.brand_count_var = $scope.home_data[0].brand_count;
						$scope.item_count_var = $scope.home_data[0].item_count;
						$scope.external_purchase_count_var = $scope.home_data[0].external_purchase_count;
						$scope.total_quotation_count_var = $scope.home_data[0].total_quotation_count;
						$scope.selected_quotation_count_var = $scope.home_data[0].selected_quotation_count;
						//alert(response.data);
					}, function myError(response) {

			});//refreshing end...

  		}, 6000);*/
	
});


































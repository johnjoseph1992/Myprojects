

    app.controller('SearchController', function ($window, $http,$scope, $rootScope){                     
      $scope.selected="";
        $scope.states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 
        'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 
        'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
        'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
        'New Jersey', 'New Mexico', 'New York', 'North Dakota', 
        'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
        'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
        'West Virginia', 'Wisconsin', 'Wyoming'];

	$scope.sampleSubmit = function(){
				//load the selectbox with firm names...
				$http({
						method : "POST",
						url : "firmForLogin",
						params: {emp_code: $scope.sample_model}
					}).then(function mySucces(response) {
						alert(response.data.stkCompanyMaster[0].firm_name);
					}, function myError(response) {

				});//loading selectbox end...
			}

	$scope.backclick = function(){
		$window.history.back();
	}

	$scope.addnew = function(){
		$rootScope.showItemBack = true; //show back button in item registration page
	}

	$scope.popup2 = {
	    opened: false
	  };

	$scope.dateOptions = {
	    formatYear: 'yyyy',
	    /*maxDate: new Date(2020, 5, 22),
	    minDate: new Date(),*/
	    startingDay: 1,
	    showWeeks:false
	  };	

	$scope.open2 = function() {
	    $scope.popup2.opened = true;
	  };

}); 





















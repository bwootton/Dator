function LocalComputer($scope, $routeParams,Restangular){

    $scope.saveComputer = function(){
        $scope.localComputer.save().then(function(computer){
            alert("Saved Computer");
        }, function(reason){
            alert("Failed to Save " + reason);
        });
    };

    $scope.loadComputer = function(){
        return  Restangular.one("/api/v1/local_computer", $routeParams.id).get().then(function (localComputer){
            $scope.localComputer=localComputer;
        }, function(reason){
            alert("Couldn't load localComputer: " + reason);
        });
    };

    $scope.loadComputer();
}

angular.module('Ruenoor').controller('LocalComputer',
    ['$scope','$routeParams','Restangular', LocalComputer] );
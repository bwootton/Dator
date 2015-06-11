function LocalComputer($scope, $routeParams,Restangular){

    $scope.saveComputer = function(){
        $scope.localComputer.save().then(function(computer){
            alert("Saved Computer");
            $scope.loadComputer();
        }, function(reason){
            alert("Failed to Save " + reason);
        });
    };

    $scope.loadComputer = function(){
        return  Restangular.one("local_computer", $routeParams.id).get().then(function (localComputer){
            $scope.localComputer=localComputer;
        }, function(reason){
            alert("Couldn't load localComputer: " + reason);
        });
    };

    $scope.loadComputer();
}

angular.module('Ruenoor').controller('LocalComputer',
    ['$scope','$routeParams','Restangular', LocalComputer] );
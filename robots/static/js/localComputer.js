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

    $scope.loadPrograms = function(){
        return Restangular.all("program").getList().then(function(programs){
            $scope.programs = programs;
        }, function(reason){
            alert("Couldn't load programs: " + reason)
        });
    };

    //
    // Send a COMMAND_DONE to the local computer
    $scope.stopComputer= function(){
        var command = {};
        command.type = 1;
        command.local_computer_id = $scope.localComputer.id;
        command.is_executed = false;

        return Restangular.post("command", command).then(function(){
            alert("Sent shutdown to box");
        },function(reason){
            alert("Couldn't shutdown local computer: " + reason);
        });
    };


    $scope.loadComputer();
    $scope.loadPrograms();


}

angular.module('Ruenoor').controller('LocalComputer',
    ['$scope','$routeParams','Restangular', LocalComputer] );
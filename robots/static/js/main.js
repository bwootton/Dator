var app = angular.module('Ruenoor');

function MainControl($scope, Restangular){

    $scope.getPrograms = function(){
        return Restangular.all("program").getList().then(function(programs){
            $scope.programs = programs;
        }, function(error){
            alert("Error in response");
        });
    };

    $scope.newProgram = function(){
        return Restangular.all("program").post({name:"new program", code:""}).then(function (created){
            $scope.getPrograms();
        });
    };

    $scope.deleteProgram = function(programId){
        var program = _.find($scope.programs, function(program){
            return program.id == programId;
        });
        return Restangular.one("program", program.id).get().then(function(foundProgram){
            foundProgram.remove().then(
                function(removeStatus){
                    $scope.getPrograms();
                });
        });
    };

    $scope.getPrograms();


}

app.controller('MainControl',['$scope', 'Restangular', MainControl]);
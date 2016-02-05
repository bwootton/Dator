/**
 * Created by brucewootton on 9/20/15.
 */
function SignalGraph($scope, $routeParams, Restangular, $http, $timeout) {

    $scope.graphSignals = {
        data: [],
        labels: [],
        shouldHaveTime: true
    };

    $scope.graphEvents = {};

    $scope._loadData = function (signalId) {
        Restangular.one('signal', signalId).get({format: 'json'}).then(function (signal) {

            $http.get('/data_api/v1/signal/' + signalId + '/?format=json').then(function (response) {
                if ($scope.graphSignals.shouldHaveTime) {

                    $scope.graphSignals.labels.push("time");
                    $scope.graphSignals.data = _convertTime(response.data);
                    for (var i=0; i < $scope.graphSignals.data[0].length - 1; i++){
                        $scope.graphSignals.labels.push("Col " + i);
                    }
                }
                $timeout(function () {
                    new Dygraph(document.getElementById("signals"), $scope.graphSignals.data,
                        {
                            draw_points: true,
                            title: "Signal - " + signal.name,
                            labels: $scope.graphSignals.labels
                        }
                    );
                });
            });
        });
    };

    /**
     * Create labels for the given time series.
     */

    /**
     * Convert the last column of a time-base signal to js Dates.
     * @param signalData a 2d array of time series where the last column is time in millisec from the epoch.
     * @return the converted array
     */
    function _convertTime(signalData) {
        var timeIndex = signalData[0].length - 1;
        var sortedSignalData = signalData.sort(function(a,b){
            return a[timeIndex]-b[timeIndex];
        });
        //return _.each(signalData, function (datum) {
        //    datum[timeIndex] = new Date(datum[timeIndex] * 1000);
        //});
        return _.map(sortedSignalData, function (datum) {
            return [new Date(datum[timeIndex] * 1000)].concat(datum.slice(0,timeIndex));
        });
    }

    $scope._loadData($routeParams.signal_id);

}

angular.module('Ruenoor').controller('SignalGraph',
    ['$scope', '$routeParams', 'Restangular', '$http', '$timeout', SignalGraph]);

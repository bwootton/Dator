/**
 * Created by brucewootton on 9/20/15.
 */
function SignalGraph($scope, $routeParams, Restangular, $http, $timeout) {
    $scope.graphSignals = {
        data: [],
        labels: ['time']
    };
    $scope.graphEvents = {};

    $scope.loadData = function (signalId) {

        Restangular.one('signal', signalId).get({format: 'json'}).then(function (signal) {
            console.log("got signal id " + signalId);
            $http.get('/data_api/v1/signal/' + signalId + '/?format=json').then(function (response) {
                console.log("signalData " + signalId);
                mergeSignal(response.data);
                $scope.graphSignals.labels.push(signal.name);
                $timeout(function () {
                    console.log("timeout signal " + signalId);
                    new Dygraph(document.getElementById("signals"), $scope.graphSignals.data,
                        {
                            draw_points: true,
                            title: "Signal - " + signal.name,
                            labels: $scope.graphSignals.labels

                        }
                    )
                });
            });
        });

    };

    function mergeSignal(signalData) {

        var sortedSignalData = signalData.sort(function(a,b){
            return a[0]-b[0];
        });
        $scope.graphSignals.data = _.map(sortedSignalData, function (datum) {
            return [new Date(datum[0] * 1000), datum[1]];
        });
    }

    $scope.loadData($routeParams.signal_id);
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
>>>>>>> 9e48beab291adb0e988b4fe1bc2cd3a1114dc59f

}

angular.module('Ruenoor').controller('SignalGraph',
    ['$scope', '$routeParams', 'Restangular', '$http', '$timeout', SignalGraph]);

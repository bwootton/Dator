var app = angular.module('Ruenoor', ['restangular', 'ngRoute', 'ui.ace'])
    .config(function (RestangularProvider, $routeProvider, $httpProvider) {

        // set routes
        $routeProvider.when('/editor/:id', {
            templateUrl: '/static/templates/editor.html'
        }).when('/', {
            templateUrl: '/static/templates/main.html'
        });

        // configure restangular to work with tastypie, which returns data in an objects list, meta data in a meta object
        RestangularProvider.setBaseUrl("/api/v1");

        RestangularProvider.setResponseExtractor(function (response, operation, what, url) {
            var newResponse;

            if (operation === "getList") {
                newResponse = response.objects;
                newResponse.metadata = response.meta;
            } else {
                newResponse = response;
            }

            return newResponse;
        });

        RestangularProvider.setRequestSuffix('/?format=json');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


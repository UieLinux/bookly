/**
 * Created by carlozamagni on 24/08/14.
 */

var booklyApp = angular.module('booklyApp', ['ngRoute'], function ($interpolateProvider) {
    // custom delimiters to avoid collision with jinja2
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


booklyApp.controller('searchCtrl', function ($scope, $http) {
    //var baseUrl = 'http://bookly-app.herokuapp.com';
    var baseUrl = 'http://bookly-app.herokuapp.com';
    $scope.submit = function () {

        var isbnQuerystringArg = '';
        var fulltextQuerystringArg = '';

        var queryString = '';

        if ($scope.isbn != null) {
            queryString = queryString.concat('isbn=' + $scope.isbn + '&');
        }

        if ($scope.fulltext != null) {
            queryString = queryString.concat('q='.concat($scope.fulltext));
        }

        $scope.searchUrl = baseUrl + '/api/search?' + queryString;
        console.log($scope.searchUrl);

        if($scope.searchUrl.indexOf('?', $scope.searchUrl.length - '?'.length) === -1){
            $http.get($scope.searchUrl)
                .then(function(res){
                    $scope.searchResult = res.data;

                    console.log($scope.searchResult);
            });
        }

    }
});
var elearningApp = angular.module('elearningApp', []);

elearningApp.controller('MainCtrl', ['$scope', '$http', function ($scope, $http) {
    // Messages array
    $scope.messages = {};

    // retrieve Messages from the restAPI
    $http({
        method: 'GET',
        url: '/stored-messages/inbox/'
    })
    .success(function (data, status, headers, config) {
        $scope.messages = data;
    })
    .error(function (data, status, headers, config) {
        // something went wrong :(
    });

    // mark messages read
    $scope.markRead = function (index) {
        var id = $scope.messages[index].id;
        $http({
            method: 'POST',
            url: '/stored-messages/inbox/'+id+'/read/',
            xsrfHeaderName: 'X-CSRFToken',
            xsrfCookieName: 'csrftoken'
        })
        .success(function (data, status, headers, config) {
            $scope.messages.splice(index, 1);
        })
        .error(function (data, status, headers, config) {
            // something went wrong :(
        })
    };

    // mark all read
    $scope.markAllRead = function () {
        $http({
            method: 'POST',
            url: '/stored-messages/mark_all_read/',
            xsrfHeaderName: 'X-CSRFToken',
            xsrfCookieName: 'csrftoken'
        })
        .success(function(data, status, headers, config) {
            $scope.messages.splice(0, $scope.messages.length);
        })
        .error(function(data, status, headers, config){
            // something went wrong :(
        })
    };
    // send a Broadcast Message
    $scope.sendBroadcast = function () {
        $http({
            method: 'GET',
            url: '/stored-messages/broadcast/',
        })
        .success(function(data, status, headers, config) {
	    // retrieve Messages from the restAPI
	    $http({
		method: 'GET',
		url: '/stored-messages/inbox/'
	    })
	    .success(function (data, status, headers, config) {
		$scope.messages = data;
	    })
        })
        .error(function(data, status, headers, config){
            // something went wrong :(
        })
    };
}]);

var myApp = angular.module('deck', ['ngRoute','angularMoment','ui.bootstrap']);

myApp.config(function ($routeProvider) {
  $routeProvider
      .when('/deck/:name/listprofile', {
      templateUrl: 'static/partials/deck/listprofile.html',
      controller: 'decklistprofileController',
      access: {restricted: true, admin:true}
    })
      .when('/deck/:name/listuser', {
      templateUrl: 'static/partials/deck/listuser.html',
      controller: 'decklistuserController',
      access: {restricted: true, admin:true}
    })
    .when('/deck/:deckid/verify', {
      controller: 'deckverifyController',
      templateUrl: 'static/partials/admin/verify.html',
      access: {restricted: true}
    })
    .when('/deck/:username/password', {
      templateUrl: 'static/partials/deck/password.html',
      controller: 'deckpasswordController',
      access: {restricted: true, admin:true}
    })
});

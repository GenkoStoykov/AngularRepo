var myApp = angular.module('myApp', ['admin','deck','ngRoute','angularMoment','ui.bootstrap']);

myApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/partials/home.html',
      access: {restricted: true}
    })
    .when('/login', {
      templateUrl: 'static/partials/login.html',
      controller: 'loginController',
      access: {restricted: false}
    })
    .when('/logout', {
      controller: 'logoutController',
      access: {restricted: true}
    })
     .when('/profile/:user', {
      controller: 'profileController',
      templateUrl: 'static/partials/user/profile.html',
      access: {restricted: true}
    })
      .when('/profile/:user/listdeck', {
      controller: 'listdeckController',
      templateUrl: 'static/partials/user/deck.html',
      access: {restricted: true}
    })
      .when('/profile/:user/addAccount', {
      controller: 'accountController',
      templateUrl: 'static/partials/account.html',
      access: {restricted: true}
    })
      .when('/profile/edit/:profileId', {
      controller: 'editProfileController',
      templateUrl: 'static/partials/user/updateProfile.html',
      access: {restricted: true}
    })
       .when('/deck/edit/:deckId', {
      controller: 'editDeckController',
      templateUrl: 'static/partials/user/updateDeck.html',
      access: {restricted: true}
    })
      .when('/log/:logtype/:name', {
      controller: 'logController',
      templateUrl: 'static/partials/log.html',
      access: {restricted: true}
    })
    .otherwise({
      redirectTo: '/profile/:user'
    });
});

myApp.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart',
    function (event, next, current) {
      AuthService.getUserStatus()
      .then(function(){
        if (next.access.restricted && !AuthService.isLoggedIn()){
          $location.path('/login');
          $route.reload();
        }
      });
  });
});
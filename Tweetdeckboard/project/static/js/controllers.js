var myApp = angular.module('myApp');

myApp
    .controller('mainController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                // call login from service
                AuthService.getUserStatus()
                    .then(function () {
                        $scope.isLoggedIn = AuthService.isLoggedIn();
                        if ($scope.isLoggedIn) {
                            $scope.user = AuthService.getUser();
                        }
                    })
            }])
    .controller('loginController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {

                $scope.login = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    // call login from service
                    AuthService.login($scope.loginForm.name, $scope.loginForm.password)
                    // handle success
                        .then(function (user) {
                            $scope.disabled = false;
                            $scope.loginForm = {};
                            if (user.admin) {
                                $location.path('/admin/listprofile');
                            }
                            else if (user.deck) {
                                $location.path('/deck/' + user.name + '/listprofile');
                            }
                            else {
                                $location.path('/profile/' + user.name);
                            }
                        })
                        // handle error
                        .catch(function () {
                            $scope.error = true;
                            $scope.errorMessage = "Invalid username and/or password";
                            $scope.disabled = false;
                            $scope.loginForm = {};
                        });

                };

            }])
    .controller('logoutController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {

                $scope.logout = function () {

                    // call logout from service
                    AuthService.logout()
                        .then(function () {
                            $location.path('/login');
                        });

                };

            }])
    .controller('profileController',
        ['$scope', '$routeParams', '$location', 'AuthService',
            function ($scope, $routeParams, $location, AuthService) {

                $scope.state = false;
                $scope.toggle = function () {
                    $scope.state = !$scope.state;
                };
                initController();

                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.getLinksByUserId($scope.user.id)
                                .then(function (decks) {
                                    $scope.decks = decks
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.getApprovesByUserId($scope.user.id)
                                .then(function (approves) {
                                    $scope.approves = approves;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.getProfilesByUserId($scope.user.id)
                                .then(function (profiles) {
                                    $scope.profiles = profiles;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });

                        })
                }

                $scope.addApprove = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    for (i = 0; i < $scope.addApprove.deck.length; i++) {
                        // call register from service
                        AuthService.addApprove($scope.addApprove.deck[i].id, $scope.addApprove.keyword, $scope.addApprove.minutes)
                        // handle success
                            .then(function (result) {
                                $scope.success = true;
                                $scope.successMessage = result.msg;
                                initController();
                                $scope.addApprove.keyword = "";
                                $scope.addApprove.minutes = "";
                                // $location.path('/login');
                            })
                            // handle error
                            .catch(function (result) {
                                $scope.error = true;
                                $scope.errorMessage = result.msg;
                                $scope.disabled = false;
                                $scope.registerForm = {};
                            });
                    }

                };

                $scope.runProfile = function (id) {
                    AuthService.runProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                }
                $scope.pauseProfile = function (id) {
                    AuthService.pauseProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                }
                $scope.delProfile = function (id) {
                    AuthService.delProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                            // $location.path('/login');
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                }

            }])
    .controller('editProfileController',
        ['$scope', '$routeParams', 'AuthService',
            function ($scope, $routeParams, AuthService) {
                AuthService.getProfileById($routeParams.profileId)
                    .then(function (profile) {
                        $scope.profile = profile;
                    })
                    // handle error
                    .catch(function () {
                        $scope.error = true;
                        $scope.errorMessage = "Something went wrong!";
                    });

                $scope.updateProfile = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    AuthService.updateProfile($scope.profile.id, $scope.profile.minutes)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });

                };
            }])
     .controller('editDeckController',
        ['$scope', '$routeParams', 'AuthService',
            function ($scope, $routeParams, AuthService) {
                AuthService.getDeckById($routeParams.deckId)
                    .then(function (deck) {
                        $scope.deck = deck;
                    })
                    // handle error
                    .catch(function () {
                        $scope.error = true;
                        $scope.errorMessage = "Something went wrong!";
                    });

                $scope.updateDeck = function () {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    AuthService.updateDeck($scope.deck.id, $scope.deck.email_address,$scope.password )
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                };
            }])
    .controller('logController',
        ['$scope', '$routeParams', 'AuthService',
            function ($scope, $routeParams, AuthService) {
                // initial values
                $scope.error = false;
                $scope.disabled = true;

                $scope.logtype = $routeParams.logtype
                $scope.name = $routeParams.name

                AuthService.getLogs($scope.logtype, $scope.name)
                    .then(function (logs) {
                        $scope.logs = logs;
                    })
                    // handle error
                    .catch(function () {
                        $scope.error = true;
                        $scope.errorMessage = "Something went wrong!";
                    })
            }
        ])
    .controller('listdeckController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                $scope.state = false;
                $scope.toggle = function () {
                    $scope.state = !$scope.state;
                };
                initController();
                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.getLinksByUserId($scope.user.id)
                                .then(function (decks) {
                                    $scope.decks = decks;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                        })
                }
                // $scope.delDeck = function (id) {
                //     AuthService.delDeck(id)
                //     // handle success
                //         .then(function (result) {
                //             $scope.success = true;
                //             $scope.successMessage = result.msg;
                //             initController();
                //             $scope.addDeckForm = {};
                //             // $location.path('/login');
                //         })
                //         // handle error
                //         .catch(function (result) {
                //             $scope.error = true;
                //             $scope.errorMessage = result.msg;
                //             $scope.disabled = false;
                //             $scope.registerForm = {};
                //         });
                // }
                // $scope.adddeck = function () {
                //
                //     // initial values
                //     $scope.error = false;
                //     $scope.disabled = true;
                //
                //     // call register from service
                //     AuthService.adddeck(
                //         $scope.user.id,
                //         $scope.addDeckForm.name,
                //         $scope.addDeckForm.password
                //     )
                //     // handle success
                //         .then(function (result) {
                //             $scope.success = true;
                //             $scope.successMessage = result.msg;
                //             $scope.disabled = false;
                //             $scope.addDeckForm = {};
                //             initController()
                //             // $location.path('/profile/'+ $scope.user.name);
                //         })
                //         // handle error
                //         .catch(function (result) {
                //             if (result.status === 0) {
                //                 deckid = result.deckid;
                //                 $location.path('/profile/' + $scope.user.name + '/' + deckid + '/verify');
                //             }
                //             else {
                //                 $scope.error = true;
                //                 $scope.errorMessage = result.msg;
                //                 $scope.disabled = false;
                //                 $scope.registerForm = {};
                //             }
                //         });
                //
                // };
            }])
    .controller('adminlistuserController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                $scope.adduser_state = false;
                $scope.adduser_toggle = function () {
                    $scope.adduser_state = !$scope.adduser_state;
                };
                var pageSize = $scope.pageSize = 10;
                $scope.itemsPerPage = pageSize;

                initController();
                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.listUsers()
                                .then(function (data) {
                                    $scope.users = data.users;

                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.listDecks()
                                .then(function (data) {
                                    $scope.decks = data.decks;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                        })
                }


                $scope.link_toggle = function (index) {
                    $scope.users[index]['show_deck'] = !$scope.users[index]['show_deck'];
                };
                $scope.addUser = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    // call register from service
                    AuthService.addUser($scope.registerForm.name,
                        $scope.registerForm.password)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                };
                $scope.linkdeck = function (userid, deckid) {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    AuthService.linkdeck(userid, deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                };
                $scope.unlinkdeck = function (userid, deckid) {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    AuthService.unlinkdeck(userid, deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                };
                $scope.delUser = function (userid) {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    // call register from service
                    AuthService.delUser(userid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                };

            }])
    .controller('adminlistdeckController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                $scope.state = false;
                $scope.toggle = function () {
                    $scope.state = !$scope.state;
                };
                initController();
                var pageSize = $scope.pageSize = 10;
                $scope.itemsPerPage = pageSize;
                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.listUsers()
                                .then(function (data) {
                                    $scope.users = data.users;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.listDecks()
                                .then(function (data) {
                                    $scope.decks = data.decks;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                        })
                }

                $scope.link_toggle = function (index) {
                    $scope.decks[index]['show_user'] = !$scope.decks[index]['show_user'];
                };
                $scope.linkdeck = function (userid, deckid) {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    AuthService.linkdeck(userid, deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};

                        });
                };
                $scope.unlinkdeck = function (userid, deckid) {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    AuthService.unlinkdeck(userid, deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                };
                $scope.logindeck = function (deckid) {
                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    AuthService.logindeck(deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            initController();
                        });
                };
                $scope.adddeck = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;
                    // call register from service
                    AuthService.adddeck($scope.addDeckForm.name,
                        $scope.addDeckForm.password,$scope.addDeckForm.user_password, $scope.addDeckForm.email)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.addDeckForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            // if (result.status === 0) {
                            //     deckid = result.deckid;
                            //     $location.path('/admin/' + $scope.addDeckForm.user.id + '/' + deckid + '/verify');
                            // }
                            // else {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.addDeckForm = {};
                            // }
                        });
                };
                $scope.delDeck = function (deckid) {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    // call register from service
                    AuthService.delDeck(deckid)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.addDeckForm = {};
                            $scope.state = false;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.addDeckForm = {};
                        });
                };
            }])
    .controller('deckverifyController',
        ['$scope', '$routeParams', '$location', 'AuthService',
            function ($scope, $routeParams, $location, AuthService) {
                deckid = $routeParams.deckid;
                $scope.verifydeck = function () {

                    // initial values
                    $scope.error = false;
                    $scope.disabled = true;

                    // call register from service
                    AuthService.verifydeck(
                        deckid,
                        $scope.registerForm.code
                    )
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                            //back to history
                            window.history.back();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });

                };
            }])
    .controller('adminlistprofileController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {

                $scope.toggle = function () {
                    $scope.state = !$scope.state;
                };
                initController();
                $scope.changeUser = function ($item, $model, $label) {
                    AuthService.getLinksByUserId($item.id)
                        .then(function (linkdecks) {
                            $scope.linkdecks = linkdecks;
                        })
                        // handle error
                        .catch(function () {
                            $scope.error = true;
                            $scope.errorMessage = "Something went wrong!";
                        });
                }

                function initController() {
                    $scope.state = false;
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.listUsers()
                                .then(function (data) {
                                    $scope.users = data.users;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.listProfiles()
                                .then(function (data) {
                                    $scope.profiles = data.profiles;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                        })
                }
                $scope.runProfile = function (id) {
                    AuthService.runProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                }
                $scope.pauseProfile = function (id) {
                    AuthService.pauseProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                }
                $scope.delProfile = function (id) {
                    AuthService.delProfile(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                            $scope.addProfile.keyword = "";
                            $scope.addProfile.minutes = "";
                            // $location.path('/login');
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });
                }

                $scope.addProfile = function () {

                    for (i = 0; i < $scope.addProfile.linkdecks.length; i++) {
                        // call register from service

                        AuthService.addProfile($scope.addProfile.linkdecks[i].id, $scope.addProfile.keyword, $scope.addProfile.minutes)
                        // handle success
                            .then(function (result) {
                                $scope.success = true;
                                $scope.successMessage = result.msg;
                                initController();
                                $scope.addProfile = {};
                            })
                            // handle error
                            .catch(function (result) {
                                $scope.error = true;
                                $scope.errorMessage = result.msg;
                                $scope.disabled = false;
                                $scope.addProfile = {};
                            });
                    }

                };

            }])
    .controller('adminpasswordController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                $scope.changeAdminPass = function () {
                    if ($scope.passForm.newPass == $scope.passForm.oldpass) {
                        $scope.error = true;
                        $scope.errorMessage = 'New Password is equal to old password.';
                        $scope.disabled = false;
                        $scope.registerForm = {};
                        return;
                    }
                    if ($scope.passForm.newPass != $scope.passForm.confirm) {
                        $scope.error = true;
                        $scope.errorMessage = 'Password did not matched.';
                        $scope.disabled = false;
                        $scope.registerForm = {};
                        return;
                    }
                    // initial values
                    $scope.error = false;
                    $scope.success = false;
                    $scope.disabled = true;

                    AuthService.changeAdminPass(
                        $scope.passForm.oldpass, $scope.passForm.newPass
                    )
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });

                };
            }])
    .controller('deckpasswordController',
        ['$scope', '$location', '$routeParams','AuthService',
            function ($scope, $location,$routeParams, AuthService) {
                $scope.username = $routeParams.username;
                AuthService.getDeckByUsername($scope.username)
                    .then(function (data) {
                        $scope.deck = data.deck;
                    })
                $scope.changeDeckPass = function () {
                    // initial values
                    $scope.error = false;
                    $scope.success = false;
                    $scope.disabled = true;

                    AuthService.changeDeckPass(
                        $scope.deck.id, $scope.passForm.newPass
                    )
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.registerForm = {};
                        });

                };
            }])
    .controller('adminmailController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                AuthService.checkEmail()
                // handle error
                    .catch(function (result) {
                        $scope.error = true;
                        $scope.errorMessage = result.msg;
                    });
                $scope.setEmail = function () {
                    $scope.error = false;
                    $scope.success = false;
                    $scope.disabled = true;

                    AuthService.setEmail(
                        $scope.emailForm.email,
                        $scope.emailForm.username,
                        $scope.emailForm.password,
                        $scope.emailForm.smtpserver
                    )
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            $scope.disabled = false;
                            $scope.emailForm = {};
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                            $scope.emailForm = {};
                        });

                };
            }])
    .controller('decklistuserController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                initController();
                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.getUsersByDeckname($scope.user.name)
                                .then(function (data) {
                                    $scope.users = data.users;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });

                        })
                }
            }])
    .controller('decklistprofileController',
        ['$scope', '$location', 'AuthService',
            function ($scope, $location, AuthService) {
                initController();
                function initController() {
                    AuthService.getUserStatus()
                        .then(function () {
                            $scope.user = AuthService.getUser();
                            AuthService.getDeckByUsername($scope.user.name)
                                .then(function (data) {
                                    $scope.deck = data.deck;
                                })

                            AuthService.getProfilesByDeckname($scope.user.name)
                                .then(function (data) {
                                    $scope.profiles = data.profiles;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                            AuthService.getApprovesByDeckname($scope.user.name)
                                .then(function (data) {
                                    $scope.approves = data.approves;
                                })
                                // handle error
                                .catch(function () {
                                    $scope.error = true;
                                    $scope.errorMessage = "Something went wrong!";
                                });
                        })
                }

                $scope.acceptPending = function (id) {
                    AuthService.acceptPendingById(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                }
                $scope.declinePending = function (id) {
                    AuthService.declinePendingById(id)
                    // handle success
                        .then(function (result) {
                            $scope.success = true;
                            $scope.successMessage = result.msg;
                            initController();
                        })
                        // handle error
                        .catch(function (result) {
                            $scope.error = true;
                            $scope.errorMessage = result.msg;
                            $scope.disabled = false;
                        });
                }
            }])
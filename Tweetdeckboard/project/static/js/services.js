angular.module('myApp').factory('AuthService',
    ['$q', '$timeout', '$http',
        function ($q, $timeout, $http) {

            // create user variable
            var user = null;

            // return available functions for use in controllers
            return ({
                isLoggedIn: isLoggedIn,
                login: login,
                logout: logout,
                addUser: addUser,
                adddeck: adddeck,
                getUserStatus: getUserStatus,
                getUser: getUser,
                addProfile: addProfile,
                addApprove: addApprove,
                getProfilesByUserId: getProfilesByUserId,
                getLogs: getLogs,
                getProfileById: getProfileById,
                getDeckById: getDeckById,
                updateProfile: updateProfile,
                updateDeck: updateDeck,
                addAccount: addAccount,
                verifydeck: verifydeck,
                delProfile: delProfile,
                delDeck: delDeck,
                listUsers: listUsers,
                delUser: delUser,
                listDecks: listDecks,
                listProfiles: listProfiles,
                changeAdminPass: changeAdminPass,
                changeDeckPass: changeDeckPass,
                linkdeck: linkdeck,
                unlinkdeck: unlinkdeck,
                logindeck: logindeck,
                getLinksByUserId: getLinksByUserId,
                setEmail: setEmail,
                checkEmail: checkEmail,
                getUsersByDeckname: getUsersByDeckname,
                getProfilesByDeckname:getProfilesByDeckname,
                getDeckByUsername:getDeckByUsername,
                getApprovesByUserId:getApprovesByUserId,
                getApprovesByDeckname:getApprovesByDeckname,
                acceptPendingById:acceptPendingById,
                declinePendingById:declinePendingById,
                runProfile:runProfile,
                pauseProfile:pauseProfile

            });

            function isLoggedIn() {
                if (user) {
                    return true;
                } else {
                    return false;
                }
            }

            function getUser() {
                return user;
            }

            function login(name, password) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/login', {name: name, password: password})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status) {
                            user = data.result.user;
                            console.log(user);
                            deferred.resolve(user);
                        } else {
                            user = false;
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        user = false;
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function logout() {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a get request to the server
                $http.get('/logout')
                // handle success
                    .success(function (data) {
                        user = false;
                        deferred.resolve();
                    })
                    // handle error
                    .error(function (data) {
                        user = false;
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function addUser(name, password) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/addUser', {
                    name: name, password: password
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function runProfile(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/runProfile', {id: id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function pauseProfile(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/pauseProfile', {id: id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }


            function delProfile(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/delProfile', {id: id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function delDeck(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/delDeck', {id: id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function addProfile(linkid, keyword, minutes) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/addProfile', {linkid: linkid, keyword: keyword, minutes: minutes})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function addApprove(linkid, keyword, minutes) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/addApprove', {linkid: linkid, keyword: keyword, minutes: minutes})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function addAccount(userid, name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/api/addAccount', {userid: userid, name: name})
                // handle success
                    .success(function (data, status, headers, config) {
                        if (data.redirect) {
                            window.location.href = data.redirect;
                            deferred.resolve();
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function updateProfile(id, minutes) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/updateProfile', {id: id, minutes: minutes})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function updateDeck(id,email_address, password ){

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/updateDeck', {
                    id: id,
                    email_address: email_address,
                    password: password
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function adddeck(name, password,user_password, email) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/adddeck', {
                    name: name,
                    password: password,
                    user_password:user_password,
                    email: email
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function verifydeck(deckid, code) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/verifydeck', {
                    deckid: deckid,
                    code: code
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function getProfilesByUserId(userid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getProfilesByUserId', {
                    userid: userid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }
            function getApprovesByUserId(userid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getApprovesByUserId', {
                    userid: userid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }
            function getLinksByUserId(userid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getLinksByUserId', {
                    userid: userid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function getLogs(logtype, name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getLogs', {
                    logtype: logtype, name: name
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function listUsers() {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/listUsers', {})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function delUser(userid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/delUser', {
                    userid: userid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function listDecks() {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/listDecks', {})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function logindeck(deckid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/logindeck', {
                    deckid: deckid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function listProfiles() {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/listProfiles', {})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function changeAdminPass(oldpass, newpass) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/changeAdminPass', {
                    oldpass: oldpass, newpass: newpass
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function changeDeckPass(deckid, newpass) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/changeDeckPass', {
                    deckid:deckid, newpass: newpass
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }
            function setEmail(email, username, password, smtpserver) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/setEmail', {
                    email: email, username: username, password: password, smtpserver: smtpserver
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function linkdeck(userid, deckid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/linkdeck', {
                    userid: userid, deckid: deckid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function unlinkdeck(userid, deckid) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/admin/unlinkdeck', {
                    userid: userid, deckid: deckid
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function getProfileById(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getProfileById', {
                    id: id
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }
            function getDeckById(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/user/getDeckById', {
                    id: id
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }
            function getUsersByDeckname(name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/getUsersByDeckname', {
                    name: name
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function getProfilesByDeckname(name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/getProfilesByDeckname', {
                    name: name
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function getDeckByUsername(name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/getDeckByUsername', {
                    name: name
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }

            function getApprovesByDeckname(name) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/getApproveByDeckname', {
                    name: name
                })
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject();
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject();
                    });

                // return promise object
                return deferred.promise;

            }
            function checkEmail() {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.get('/admin/checkEmail', {})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function acceptPendingById(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/acceptPendingById', {id:id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function declinePendingById(id) {

                // create a new instance of deferred
                var deferred = $q.defer();

                // send a post request to the server
                $http.post('/deck/declinePendingById', {id:id})
                // handle success
                    .success(function (data, status) {
                        if (status === 200 && data.result.status > 0) {
                            deferred.resolve(data.result);
                        } else {
                            deferred.reject(data.result);
                        }
                    })
                    // handle error
                    .error(function (data) {
                        deferred.reject(data.result);
                    });

                // return promise object
                return deferred.promise;

            }

            function getUserStatus() {
                return $http.get('/status')
                // handle success
                    .success(function (data) {
                        if (data.result.status) {
                            user = data.result.user;
                        } else {
                            user = false;
                        }
                    })
                    // handle error
                    .error(function (data) {
                        user = false;
                    });
            }

        }]);
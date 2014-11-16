var vup = angular.module('vup', ['LocalStorageModule', 'ngDraggable']);

vup.controller('dashboard', ['$rootScope', '$scope', '$location', '$http', 'localStorageService', function ($rootScope, $scope, $location, $http, localStorageService) {
    console.log("Dashboard started.");

    $scope.notification = {};
    $scope.notification['timeout'] = 1500;
    $scope.notification['position'] = 'bottom-center';

    $scope.projects = [];

    $scope.newProject = function () {
        $scope.project = {};
        $scope.project['name'] = 'New Project';
        $scope.project['newName'] = '';
        $scope.project['containers'] = [];
        $scope.project['version'] = "0.01";
        $scope.project['id'] = '';
    };

    $scope.newProject();

    $scope.modal = null;

    $scope.stacklets = {
        'nginx': {
            'name': 'nginx',
            'label': 'nginx',
            'type': 'nginx'
        },
        'mysql': {
            'name': 'mysql',
            'label': 'mysql',
            'type': 'mysql',
            'mysql_name': 'demo',
            'mysql_user': 'demouser',
            'mysql_pass': 'demopass',
            'mysql_sql': 'whateverIwant!',
            "ports": [3306]
        },
        'php': {
            'name': 'php',
            'label': 'php',
            'type': 'php'
        },
        'uwsgi': {
            'name': 'uwsgi',
            'label': 'uwsgi',
            'type': 'uwsgi'
        },
        'haproxy': {
            'name': 'haproxy',
            'label': 'ha proxy',
            'type': 'haproxy'
        },
        'apache': {
            'name': 'apache',
            'label': 'apache',
            'type': 'apache'
        },
        'folder': {
            'name': 'folder',
            'label': 'source folder',
            'type': 'folder'
        }
    };

    $scope.containerToDelete = null;


    var apiUrl = '/api/v1';

    $scope.dropped = function (data, event) {
        console.log('Dropped', data, event);

        if (!$scope.project) {
            $scope.project = {};
            $scope.project['containers'] = [];
        }

        $scope.project.containers.push(data);
        $rootScope.$broadcast('Project:LocalChange');
    };

    $scope.loadProject = function (id) {
        for (var index in $scope.projects) {
            if (id == $scope.projects[index].id) {
                $scope.project = $scope.projects[index];
                $scope.notify('<i class="uk-icon-folder-open"></i> Loaded project ' + $scope.project.name, 'success');
            }
        }
    };

    $scope.deleteProject = function () {
        if (!$scope.project.id) {
            $scope.newProject();
            return;
        }
        $http({method: 'DELETE', data: $scope.project, url: apiUrl + '/projects/' + $scope.project.id})
            .success(function (response) {
                $scope.newProject();
                $scope.refreshPending = false;
                $scope.loading = false;
                $scope.notify('<i class="uk-icon-close"></i> Deleted project successfully!', 'success');
                $scope.refresh();
            })
            .error(function (error) {
                $scope.projects = [];
                $scope.refreshPending = false;
                $scope.loading = false;
                console.log('Failed to delete project...', error);
                $scope.notify('Bad news, everybody! ' + error, 'danger');
            });
    };

    $scope.editProjectName = function ($event, start) {
        if (start) {
            $scope.project.editName = 1;
            if (!$scope.project.newName) $scope.project.newName = $scope.project.name;
            jQuery('#edit-project-name').focus();
        } else {
            $scope.project.editName = 0;
            $scope.project.newName = '';
        }

        if ($event.which) {
            if ($event.which == 13) {
                $scope.project.editName = 0;
                $scope.project.name = $scope.project.newName;
                $rootScope.$broadcast('Project:LocalChange');
            }

            if ($event.which == 27) {
                $scope.project.editName = 0;
                $scope.project.newName = '';
            }
        }
    };

    $scope.deleteContainer = function (container) {
        $scope.modal = jQuery.UIkit.modal("#delete-container-modal");

        if ($scope.modal.isActive()) {
            $scope.modal.hide();
        } else {
            $scope.modal.show();
            $scope.containerToDelete = container;
        }
    };

    $scope.confirmDeleteContainer = function() {
        for (var index in $scope.project.containers) {
            if (angular.equals($scope.project.containers[index], $scope.containerToDelete)) {
                $scope.project.containers.splice(index, 1);
                $scope.modal.hide();
                $rootScope.$broadcast('Project:LocalChange');
            }
        }
    };

    $scope.refresh = function () {
        if ($scope.refreshPending) return;
        $scope.refreshPending = true;

        $http({method: 'GET', url: apiUrl + '/projects'})
            .success(function (response) {
                $scope.projects = response.data;
                $rootScope.$broadcast('Project:Change');
                $scope.refreshPending = false;
                $scope.loading = false;
                $scope.notify('<i class="uk-icon-exchange"></i> Loaded existing projects...', 'success');
            })
            .error(function (error) {
                $scope.projects = [];
                $scope.refreshPending = false;
                $scope.loading = false;
                console.log('Failed to list projects...', error);
                $scope.notify('Bad news, everybody! ' + error, 'danger');
            });
    };

    $rootScope.$on('Project:LocalChange', function () {
        var method = '';
        var url = '/projects';
        if ($scope.project.id) {
            method = 'PUT';
            url = url + '/' + $scope.project.id;
        } else {
            method = 'POST';
        }



        console.log(method, $scope.project);

        $http({method: method, data: $scope.project, url: apiUrl + url})
            .success(function (response) {
                $scope.projects = response.data;
                $rootScope.$broadcast('Project:Change');
                $scope.refreshPending = false;
                $scope.loading = false;
                $scope.notify('<i class="uk-icon-save"></i> Updated project successfully!', 'success');
            })
            .error(function (error) {
                $scope.projects = [];
                $scope.refreshPending = false;
                $scope.loading = false;
                console.log('Failed to update project...', error);
                $scope.notify('Bad news, everybody! ' + error, 'danger');
            });

        $scope.refresh();
    });

    $scope.notify = function (text, status) {
        jQuery.UIkit.notify({
            message : text,
            status  : status,
            timeout : $scope.notification.timeout,
            pos     : $scope.notification.position
        });
    };

    $scope.refresh();
}]);

/* Start angularLocalStorage */
var angularLocalStorage = angular.module('LocalStorageModule', []);

// You should set a prefix to avoid overwriting any local storage variables from the rest of your app
// e.g. angularLocalStorage.constant('prefix', 'youAppName');
angularLocalStorage.constant('prefix', 'vup');
// Cookie options (usually in case of fallback)
// expiry = Number of days before cookies expire // 0 = Does not expire
// path = The web path the cookie represents
angularLocalStorage.constant('cookie', { expiry: 30, path: '/'});
angularLocalStorage.constant('notify', { setItem: true, removeItem: false});

angularLocalStorage.service('localStorageService', [
    '$rootScope',
    'prefix',
    'cookie',
    'notify',
    function ($rootScope, prefix, cookie, notify) {

        // Checks the browser to see if local storage is supported
        var browserSupportsLocalStorage = function () {
            try {
                return ('localStorage' in window && window['localStorage'] !== null);
            } catch (e) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                return false;
            }
        };

        // Directly adds a value to local storage
        // If local storage is not available in the browser use cookies
        // Example use: localStorageService.add('library','angular');
        var addToLocalStorage = function (key, value) {

            // If this browser does not support local storage use cookies
            if (!browserSupportsLocalStorage()) {
                $rootScope.$broadcast('LocalStorageModule.notification.warning', 'LOCAL_STORAGE_NOT_SUPPORTED');
                if (notify.setItem) {
                    $rootScope.$broadcast('LocalStorageModule.notification.setitem', {key: key, newvalue: value, storageType: 'cookie'});
                }
                return addToCookies(key, value);
            }

            // Let's convert undefined values to null to get the value consistent
            if (typeof value == "undefined") value = null;
            try {
                localStorage.setItem(prefix + key, JSON.stringify(value));
                if (notify.setItem) {
                    $rootScope.$broadcast('LocalStorageModule.notification.setitem', {key: key, newvalue: value, storageType: 'localStorage'});
                }
            } catch (e) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                return addToCookies(key, value);
            }
            return true;
        };

        // Directly get a value from local storage
        // Example use: localStorageService.get('library'); // returns 'angular'
        var getFromLocalStorage = function (key) {
            if (!browserSupportsLocalStorage()) {
                $rootScope.$broadcast('LocalStorageModule.notification.warning', 'LOCAL_STORAGE_NOT_SUPPORTED');
                return getFromCookies(key);
            }

            var item = localStorage.getItem(prefix + key);
            if (!item) return null;
            return JSON.parse(item);
        };

        // Remove an item from local storage
        // Example use: localStorageService.remove('library'); // removes the key/value pair of library='angular'
        var removeFromLocalStorage = function (key) {
            if (!browserSupportsLocalStorage()) {
                $rootScope.$broadcast('LocalStorageModule.notification.warning', 'LOCAL_STORAGE_NOT_SUPPORTED');
                if (notify.removeItem) {
                    $rootScope.$broadcast('LocalStorageModule.notification.removeitem', {key: key, storageType: 'cookie'});
                }
                return removeFromCookies(key);
            }

            try {
                localStorage.removeItem(prefix + key);
                if (notify.removeItem) {
                    $rootScope.$broadcast('LocalStorageModule.notification.removeitem', {key: key, storageType: 'localStorage'});
                }
            } catch (e) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                return removeFromCookies(key);
            }
            return true;
        };

        // Remove all data for this app from local storage
        // Example use: localStorageService.clearAll();
        // Should be used mostly for development purposes
        var clearAllFromLocalStorage = function () {
            if (!browserSupportsLocalStorage()) {
                $rootScope.$broadcast('LocalStorageModule.notification.warning', 'LOCAL_STORAGE_NOT_SUPPORTED');
                return clearAllFromCookies();
            }

            var prefixLength = prefix.length;

            for (var key in localStorage) {
                // Only remove items that are for this app
                if (key.substr(0, prefixLength) === prefix) {
                    try {
                        removeFromLocalStorage(key.substr(prefixLength));
                    } catch (e) {
                        $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                        return clearAllFromCookies();
                    }
                }
            }
            return true;
        };

        // Checks the browser to see if cookies are supported
        var browserSupportsCookies = function () {
            try {
                return navigator.cookieEnabled ||
                    ("cookie" in document && (document.cookie.length > 0 ||
                        (document.cookie = "test").indexOf.call(document.cookie, "test") > -1));
            } catch (e) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                return false;
            }
        };

        // Directly adds a value to cookies
        // Typically used as a fallback is local storage is not available in the browser
        // Example use: localStorageService.cookie.add('library','angular');
        var addToCookies = function (key, value) {
            if (typeof value == "undefined") return false;

            if (!browserSupportsCookies()) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', 'COOKIES_NOT_SUPPORTED');
                return false;
            }

            try {
                var expiry = '', expiryDate = new Date();
                if (value === null) {
                    cookie.expiry = -1;
                    value = '';
                }
                if (cookie.expiry !== 0) {
                    expiryDate.setTime(expiryDate.getTime() + (cookie.expiry * 24 * 60 * 60 * 1000));
                    expiry = "; expires=" + expiryDate.toGMTString();
                }
                if (!!key) {
                    document.cookie = prefix + key + "=" + encodeURIComponent(value) + expiry + "; path=" + cookie.path;
                }
            } catch (e) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', e.message);
                return false;
            }
            return true;
        };

        // Directly get a value from a cookie
        // Example use: localStorageService.cookie.get('library'); // returns 'angular'
        var getFromCookies = function (key) {
            if (!browserSupportsCookies()) {
                $rootScope.$broadcast('LocalStorageModule.notification.error', 'COOKIES_NOT_SUPPORTED');
                return false;
            }

            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var thisCookie = cookies[i];
                while (thisCookie.charAt(0) == ' ') {
                    thisCookie = thisCookie.substring(1, thisCookie.length);
                }
                if (thisCookie.indexOf(prefix + key + '=') === 0) {
                    return decodeURIComponent(thisCookie.substring(prefix.length + key.length + 1, thisCookie.length));
                }
            }
            return null;
        };

        var removeFromCookies = function (key) {
            addToCookies(key, null);
        };

        var clearAllFromCookies = function () {
            var thisCookie = null, thisKey = null;
            var prefixLength = prefix.length;
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                thisCookie = cookies[i];
                while (thisCookie.charAt(0) == ' ') {
                    thisCookie = thisCookie.substring(1, thisCookie.length);
                }
                var key = thisCookie.substring(prefixLength, thisCookie.indexOf('='));
                removeFromCookies(key);
            }
        };

        // JSON stringify functions based on https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/JSON
        var stringifyJson = function (vContent, isJSON) {
            // If this is only a string and not a string in a recursive run of an object then let's return the string unadulterated
            if (typeof vContent === "string" && vContent.charAt(0) !== "{" && !isJSON) {
                return vContent;
            }
            if (vContent instanceof Object) {
                var sOutput = "";
                if (vContent.constructor === Array) {
                    for (var nId = 0; nId < vContent.length; sOutput += this.stringifyJson(vContent[nId], true) + ",", nId++);
                    return "[" + sOutput.substr(0, sOutput.length - 1) + "]";
                }
                if (vContent.toString !== Object.prototype.toString) {
                    return "\"" + vContent.toString().replace(/"/g, "\\$&") + "\"";
                }
                for (var sProp in vContent) {
                    sOutput += "\"" + sProp.replace(/"/g, "\\$&") + "\":" + this.stringifyJson(vContent[sProp], true) + ",";
                }
                return "{" + sOutput.substr(0, sOutput.length - 1) + "}";
            }
            return typeof vContent === "string" ? "\"" + vContent.replace(/"/g, "\\$&") + "\"" : String(vContent);
        };

        var parseJson = function (sJSON) {
            if (sJSON.charAt(0) !== '{') {
                return sJSON;
            }
            return eval("(" + sJSON + ")");
        };

        return {
            isSupported: browserSupportsLocalStorage,
            set: addToLocalStorage,
            add: addToLocalStorage, //DEPRECATED
            get: getFromLocalStorage,
            remove: removeFromLocalStorage,
            clearAll: clearAllFromLocalStorage,
            stringifyJson: stringifyJson,
            parseJson: parseJson,
            cookie: {
                set: addToCookies,
                add: addToCookies, //DEPRECATED
                get: getFromCookies,
                remove: removeFromCookies,
                clearAll: clearAllFromCookies
            }
        };

    }]);
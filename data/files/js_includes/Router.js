// Generated by CoffeeScript 1.9.1

/**
* Helper class for easy routing. Works with the routing that is used for PHP.
* Examples:
* GET:  router.get("api/my_test_route?a=10&b=20")       => $.get("api.php?route=my_test_route?a=10&b=20")
* GET:  router.get("api/my_test_route", {a: 10, b: 20}) => $.get("api.php?route=my_test_route", {a: 10, b: 20})
*
* POST: router.post("api/my_test_route", {a: 10})       => $.post("api.php", {route: "my_test_route", a: 10})
*
 */

(function() {
  window.Router = (function() {
    var _transformGetURL, _transformPostURL;

    function Router() {
      this.prefix = "api/";
    }

    _transformGetURL = function(url) {
      if (url.slice(0, this.prefix.length) === this.prefix) {
        return "api.php?route=" + (url.slice(this.prefix.length));
      }
      return url;
    };

    _transformPostURL = function(url) {
      if (url.slice(0, this.prefix.length) === this.prefix) {
        return "api.php?route=" + (url.slice(this.prefix.length));
      }
      return url;
    };

    Router.get = function(route, params, callback) {
      route = _transformGetURL.call(this, route);
      if (arguments.length === 2) {
        return $.get(route, params);
      }
      return $.get(route, params, callback);
    };

    Router.post = function(route, params, callback) {
      route = _transformPostURL(route, this.prefix);
      if (params instanceof Function) {
        callback = params;
        params = {
          route: route
        };
      } else if (params != null) {
        params.route = route;
      } else {
        params = {
          route: route
        };
      }
      return $.post("api.php", params, callback);
    };

    return Router;

  })();

  window.router = new Router();

}).call(this);

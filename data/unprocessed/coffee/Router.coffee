###*
* Helper class for easy routing. Works with the routing that is used for PHP.
* Examples:
* GET:  router.get("api/my_test_route?a=10&b=20")       => $.get("api.php?route=my_test_route?a=10&b=20")
* GET:  router.get("api/my_test_route", {a: 10, b: 20}) => $.get("api.php?route=my_test_route", {a: 10, b: 20})
*
* POST: router.post("api/my_test_route", {a: 10})       => $.post("api.php", {route: "my_test_route", a: 10})
*###
class window.Router

    # CONSTRUCTOR
    constructor: () ->
        @prefix = "api/"

    # PRIVATE
    _transformGetURL = (url) ->
        if url.slice(0, @prefix.length) is @prefix
            return "api.php?route=#{url.slice(@prefix.length)}"

        return url

    _transformPostURL = (url) ->
        if url.slice(0, @prefix.length) is @prefix
            return "api.php?route=#{url.slice(@prefix.length)}"

        return url

    # PUBLIC
    @get: (route, params, callback) ->
        route = _transformGetURL.call(@, route)

        if arguments.length is 2
            return $.get route, params

        return $.get route, params, callback

    @post: (route, params, callback) ->
        route = _transformPostURL(route, @prefix)

        # params skipped => create params for route
        if params instanceof Function
            callback = params
            params =
                route: route
        # params passed => add route
        else if params?
            params.route = route
        # no params passed (null / undefined)
        else
            params =
                route: route

        return $.post "api.php", params, callback


window.router = new Router()

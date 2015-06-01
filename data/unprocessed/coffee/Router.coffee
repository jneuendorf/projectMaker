class window.Router

    # CONSTRUCTOR
    constructor: () ->

    @get: (route, params, callback) ->
        if route.slice(0, 3) is "api"
            route = "something fancy"

        if arguments.length is 2
            return $.get route, callback

        return $.get route, params, callback

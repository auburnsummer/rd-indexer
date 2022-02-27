from typing import Dict, List
from starlette.background import BackgroundTask
from orchard.bot.constants import ResponseType
from starlette.responses import JSONResponse
from inspect import signature


class SlashOptionPermission:
    def __init__(self, id, type, permission):
        self._id = id
        self._type = type
        self._permission = permission

    def permission_api(self):
        return {"id": self._id, "type": self._type, "permission": self._permission}


class SlashOptionChoice:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def api(self):
        return {"name": self._name, "value": self._value}


class SlashOption:
    def __init__(self, type, name, description, required=False, choices=None):
        self._type = type
        self._name = name
        self._description = description
        self._required = required
        self._choices = choices

    def api(self):
        output = {
            "type": self._type,
            "name": self._name,
            "description": self._description,
            "required": self._required,
        }
        # if the option has choices, add them.
        if self._choices is not None:
            output["choices"] = [c.api() for c in self._choices]

        return output


class SlashRoute:
    def __init__(
        self,
        name,
        description,
        handler,
        default_permission=True,
        options=None,
        defer=False,
        permissions=None,
    ):
        self._name = name
        self._description = description
        self._handler = handler
        self._default_permission = default_permission
        self._options = options
        self._defer = defer
        self._permissions = permissions

    def api(self):
        output = {
            "name": self._name,
            "description": self._description,
            "default_permission": self._default_permission,
        }
        if self._options is not None:
            output["options"] = [o.api() for o in self._options]

        return output

    def permission_api(self, id):
        return {
            "id": id,
            "permissions": [p.permission_api() for p in self._permissions],
        }


class SlashRouter:
    def __init__(self, routes):
        self._routes = routes
        # build a mapping of route names to routes
        self._route_map = {}
        for route in self._routes:
            self._route_map[route._name] = route

    def api(self):
        return [r.api() for r in self._routes]

    def permission_api(self, mapping):
        return [
            r.permission_api(mapping[r._name])
            for r in self._routes
            if r._permissions is not None
        ]

    def handle(self, body, request):
        # Get the route name from the body. The body is a dictionary. The route name is located under the key "data.name"
        route_name = body["data"]["name"]
        # Check if the route name is present in the mapping.
        if route_name in self._route_map:
            # Execute the associated handler. If it's not deferred, we just return it straightaway.
            if not self._route_map[route_name]._defer:
                return self._route_map[route_name]._handler(body, request)
            else:
                # Return a deferred response, which is type 5.
                deferred_task = BackgroundTask(
                    self._route_map[route_name]._handler, body, request
                )
                return JSONResponse(
                    {"type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE},
                    background=deferred_task,
                )
        else:
            # Otherwise, return a default response. The default response has a 200 return code.
            # The key 'type' is 4, and the key 'data.content' is something like "oh no"
            return JSONResponse({"type": 4, "data": {"content": "oh no"}})

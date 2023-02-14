from enum import Enum, auto
from typing import Callable, Dict, List, Union, Any, Optional
from starlette.background import BackgroundTask
from orchard.bot.lib.constants import OptionType, ResponseType
from starlette.responses import JSONResponse

EVERY_PERMISSION = str(2**41 - 1)
NO_PERMISSIONS = str(0)


class SlashOptionChoice:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def api(self):
        return {"name": self._name, "value": self._value}


class SlashOption:
    def __init__(
        self,
        type: OptionType,
        name: str,
        description: str,
        required=False,
        choices=None,
    ):
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


class RouteType(Enum):
    IMMEDIATE = auto()
    DEFER_VISIBLE = auto()
    DEFER_EPHEMERAL = auto()


class SlashRoute:
    def __init__(
        self,
        name: str,
        description: str,
        handler,
        default_permission=False,
        options: Optional[List[SlashOption]] = None,
        defer: Union[RouteType, Callable[[Any, Any], RouteType]] = RouteType.IMMEDIATE,
    ):
        self._name = name
        self._description = description
        self._handler = handler
        self._default_permission = default_permission
        self._options = options
        self._defer = defer

    def api(self):
        output = {
            "name": self._name,
            "description": self._description,
            "default_member_permissions": EVERY_PERMISSION
            if self._default_permission
            else NO_PERMISSIONS,
        }
        if self._options is not None:
            output["options"] = [o.api() for o in self._options]

        return output


class SlashRouter:
    _route_map: Dict[str, SlashRoute]

    def __init__(self, routes: List[SlashRoute]):
        self._routes = routes
        # build a mapping of route names to routes
        self._route_map = {}
        for route in self._routes:
            self._route_map[route._name] = route

    def api(self):
        return [r.api() for r in self._routes]

    def handle(self, body, request):
        # Get the route name from the body. The body is a dictionary. The route name is located under the key "data.name"
        route_name = body["data"]["name"]
        # Check if the route name is present in the mapping.
        if route_name in self._route_map:
            # Execute the associated handler. _defer can be a function that returns a RouteType.
            route = self._route_map[route_name]
            if callable(route._defer):
                route_type = route._defer(body, request)
            else:
                route_type = route._defer
            # If it's an immediate route, just call the handler.
            if route_type == RouteType.IMMEDIATE:
                return route._handler(body, request)
            else:
                # 64 means the "clc is thinking..." is ephemeral
                flags = 64 if route_type == RouteType.DEFER_EPHEMERAL else 0
                # Return a deferred response, which is type 5.
                deferred_task = BackgroundTask(
                    self._route_map[route_name]._handler, body, request
                )
                args = {
                    "type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {"flags": flags},
                }
                return JSONResponse(
                    args,
                    background=deferred_task,
                )
        else:
            return JSONResponse(
                {
                    "type": 4,
                    "data": {
                        "content": f"I don't know what to do with the requested route {route_name}. This is always a bug; ping auburn now!"
                    },
                }
            )

#-*- coding: utf-8 -*-
from share.framework.bottle.app import APIBlueprint

from .update import UpdateOpenAPI

blueprint_api = APIBlueprint('api')

UpdateOpenAPI.attach_to(blueprint_api)

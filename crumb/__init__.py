from tortoise import Tortoise

from configuration import settings


Tortoise.init(config=settings.DATABASE)

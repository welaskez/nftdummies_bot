__all__ = ("routers",)

from .admin import routers as admin_routers
from .user import routers as user_routers

routers = admin_routers + user_routers

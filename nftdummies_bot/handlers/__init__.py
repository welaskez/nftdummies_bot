__all__ = ("routers",)

from .admin import router as admin_router
from .user import router as user_router

routers = [
    admin_router,
    user_router,
]

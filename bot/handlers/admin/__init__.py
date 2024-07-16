__all__ = ("routers",)

from .newsletter import router as newsletter_router

routers = [
    newsletter_router,
]

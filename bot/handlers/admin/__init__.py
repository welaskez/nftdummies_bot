__all__ = ("routers",)

from .update_stickers import router as update_stickers_router

routers = [
    update_stickers_router,
]

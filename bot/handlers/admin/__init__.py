__all__ = ("routers",)

from .update_stickers import router as update_stickers_router
from .delete_sticker import router as delete_sticker_router
from .add_sticker import router as add_sticker_router
from .admin import router as admin_router

routers = [
    update_stickers_router,
    delete_sticker_router,
    add_sticker_router,
    admin_router,
]

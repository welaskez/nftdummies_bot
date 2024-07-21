__all__ = ("routers",)

from .start import router as start_router
from .inline import router as inline_router

routers = [
    start_router,
    inline_router,
]

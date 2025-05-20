from app.handlers.user import user_router
from app.handlers.admin import admin_router

router = [user_router, admin_router]

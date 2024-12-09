from fastapi import APIRouter
from . import auth, users, shop, game, system, election

router = APIRouter()

router.include_router(system.router, tags=["system"])
router.include_router(auth.router, tags=["auth"])
router.include_router(users.router, tags=["users"])
router.include_router(game.router, tags=["game"])
router.include_router(shop.router, tags=["shop"])
router.include_router(election.router, tags=["election"])
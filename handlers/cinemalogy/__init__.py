"""
Пакет Cinemalogy.
"""

from aiogram import Router

from .start import router as start_router
from .choose_frame import router as choose_frame_router
from .confirm_frame import router as confirm_frame_router
from .result import router as result_router
from .invitation import router as invitation_router
from .tariff import router as tariff_router
from .payment import router as payment_router
from .payment_done import router as payment_done_router
from .unknown import router as unknown_router
from .admin import router as admin_router
from .frame_navigation import router as frame_navigation_router

router = Router()

router.include_router(start_router)
router.include_router(choose_frame_router)
router.include_router(confirm_frame_router)
router.include_router(result_router)
router.include_router(invitation_router)
router.include_router(tariff_router)
router.include_router(payment_router)
router.include_router(payment_done_router)   # ← ВАЖНО
router.include_router(unknown_router)
router.include_router(admin_router)
router.include_router(frame_navigation_router)

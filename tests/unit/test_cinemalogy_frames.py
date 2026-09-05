"""
Тесты для bot_services/cinemalogy/frames.py — навигация по 12 кадрам
квиза Cinemalogy (handlers/cinemalogy/frame_navigation.py).
"""

import pytest

from bot_services.cinemalogy.frames import (
    FRAME_COUNT,
    frame_material,
    next_frame,
    normalize,
    previous_frame,
)


def test_frame_count_is_12():
    assert FRAME_COUNT == 12


@pytest.mark.parametrize(
    "index,expected",
    [(0, 1), (5, 6), (10, 11)],
)
def test_next_frame(index, expected):
    assert next_frame(index) == expected


def test_next_frame_wraps_around_after_last_frame():
    assert next_frame(FRAME_COUNT - 1) == 0


@pytest.mark.parametrize(
    "index,expected",
    [(5, 4), (11, 10), (1, 0)],
)
def test_previous_frame(index, expected):
    assert previous_frame(index) == expected


def test_previous_frame_wraps_around_before_first_frame():
    assert previous_frame(0) == FRAME_COUNT - 1


@pytest.mark.parametrize(
    "index,expected",
    [(0, 0), (11, 11), (12, 0), (13, 1), (-1, 11)],
)
def test_normalize(index, expected):
    assert normalize(index) == expected


def test_frame_material_uses_1_based_keys():
    assert frame_material(0) == "frame_1"
    assert frame_material(11) == "frame_12"

from datetime import datetime
from unittest import TestCase

import pytz

from aqua_airdrop_checker.utils.time_periods import Period, intersect_periods, negate_periods, unite_periods


def make_datetime(*args) -> datetime:
    return pytz.utc.localize(datetime(*args))


class TestUniteFunction(TestCase):
    def test_unite_intersected_periods(self):
        period_list1 = [
            Period(
                make_datetime(2021, 1, 1),
                make_datetime(2021, 1, 3),
            ),
            Period(
                make_datetime(2021, 1, 5),
                make_datetime(2021, 1, 7),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 2),
                make_datetime(2021, 1, 6),
            ),
        ]

        self.assertEqual(
            [
                Period(
                    make_datetime(2021, 1, 1),
                    make_datetime(2021, 1, 7),
                ),
            ], unite_periods(period_list1, period_list2),
        )

    def test_unite_not_intersected_periods(self):
        period_list1 = [
            Period(
                make_datetime(2021, 1, 1),
                make_datetime(2021, 1, 3),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 5),
                make_datetime(2021, 1, 7),
            ),
        ]

        self.assertEqual(
            [
                Period(
                    make_datetime(2021, 1, 1),
                    make_datetime(2021, 1, 3),
                ),
                Period(
                    make_datetime(2021, 1, 5),
                    make_datetime(2021, 1, 7),
                ),
            ], unite_periods(period_list1, period_list2),
        )

    def test_unite_infinite_periods(self):
        period_list1 = [
            Period(
                None,
                make_datetime(2021, 1, 5),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 3),
                None,
            ),
        ]

        self.assertEqual(
            [
                Period(
                    None,
                    None,
                ),
            ], unite_periods(period_list1, period_list2),
        )


class TestIntersectFunction(TestCase):
    def test_intersect_intersected_periods(self):
        period_list1 = [
            Period(
                make_datetime(2021, 1, 1),
                make_datetime(2021, 1, 3),
            ),
            Period(
                make_datetime(2021, 1, 5),
                make_datetime(2021, 1, 7),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 2),
                make_datetime(2021, 1, 6),
            ),
        ]

        self.assertEqual(
            [
                Period(
                    make_datetime(2021, 1, 2),
                    make_datetime(2021, 1, 3),
                ),
                Period(
                    make_datetime(2021, 1, 5),
                    make_datetime(2021, 1, 6),
                ),
            ], intersect_periods(period_list1, period_list2),
        )

    def test_intersect_not_intersected_periods(self):
        period_list1 = [
            Period(
                make_datetime(2021, 1, 1),
                make_datetime(2021, 1, 3),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 5),
                make_datetime(2021, 1, 7),
            ),
        ]

        self.assertEqual(
            [], intersect_periods(period_list1, period_list2),
        )

    def test_intersect_infinite_periods(self):
        period_list1 = [
            Period(
                None,
                make_datetime(2021, 1, 5),
            ),
        ]
        period_list2 = [
            Period(
                make_datetime(2021, 1, 3),
                None,
            ),
        ]

        self.assertEqual(
            [
                Period(
                    make_datetime(2021, 1, 3),
                    make_datetime(2021, 1, 5),
                ),
            ], intersect_periods(period_list1, period_list2),
        )


class TestNegateFunction(TestCase):
    def test_negate_infinite_periods(self):
        period_list = [
            Period(
                None,
                make_datetime(2021, 1, 3),
            ),
            Period(
                make_datetime(2021, 1, 5),
                None,
            ),
        ]

        self.assertEqual(
            [
                Period(
                    make_datetime(2021, 1, 3),
                    make_datetime(2021, 1, 5),
                ),
            ], negate_periods(period_list),
        )

    def test_negate_finite_periods(self):
        period_list = [
            Period(
                make_datetime(2021, 1, 1),
                make_datetime(2021, 1, 3),
            ),
            Period(
                make_datetime(2021, 1, 5),
                make_datetime(2021, 1, 7),
            ),
        ]

        self.assertEqual(
            [
                Period(
                    None,
                    make_datetime(2021, 1, 1),
                ),
                Period(
                    make_datetime(2021, 1, 3),
                    make_datetime(2021, 1, 5),
                ),
                Period(
                    make_datetime(2021, 1, 7),
                    None,
                ),
            ], negate_periods(period_list),
        )

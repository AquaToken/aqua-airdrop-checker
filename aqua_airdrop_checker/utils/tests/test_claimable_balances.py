from unittest import TestCase

from aqua_airdrop_checker.utils.claimable_balances import get_next_claim_time
from aqua_airdrop_checker.utils.tests.test_time_periods import make_datetime


class TestGetNextClaimFunction(TestCase):
    def test_unconditional_predicate(self):
        predicate = {
            'unconditional': True,
        }

        # Case 12
        now = make_datetime(2021, 1, 1)
        self.assertEqual(
            (True, False, False, None, None),
            get_next_claim_time(predicate, now),
        )

    def test_abs_before_predicate(self):
        predicate = {
            'abs_before': '2021-01-01T00:00:00Z',
        }

        # Case 1
        now = make_datetime(2020, 12, 31)
        self.assertEqual(
            (True, False, False, None, make_datetime(2021, 1, 1)),
            get_next_claim_time(predicate, now),
        )

        # Case 2
        now = make_datetime(2021, 1, 2)
        self.assertEqual(
            (False, True, False, None, make_datetime(2021, 1, 1)),
            get_next_claim_time(predicate, now),
        )

    def test_abs_after_predicate(self):
        predicate = {
            'not': {
                'abs_before': '2021-01-01T00:00:00Z',
            },
        }

        # Case 3
        now = make_datetime(2020, 12, 31)
        self.assertEqual(
            (False, False, False, make_datetime(2021, 1, 1), None),
            get_next_claim_time(predicate, now),
        )

        # Case 4 / Case 10
        now = make_datetime(2021, 1, 2)
        self.assertEqual(
            (True, False, False, None, None),
            get_next_claim_time(predicate, now),
        )

    def test_period_predicate(self):
        predicate = {
            'and': [
                {
                    'not': {
                        'abs_before': '2021-01-01T00:00:00Z',
                    },
                },
                {
                    'abs_before': '2021-02-01T00:00:00Z',
                },
            ],
        }

        # Case 8
        now = make_datetime(2020, 12, 31)
        self.assertEqual(
            (False, False, False, make_datetime(2021, 1, 1), make_datetime(2021, 2, 1)),
            get_next_claim_time(predicate, now),
        )

        # Case 9
        now = make_datetime(2021, 1, 5)
        self.assertEqual(
            (True, False, False, make_datetime(2021, 1, 1), make_datetime(2021, 2, 1)),
            get_next_claim_time(predicate, now),
        )

        # Case 13
        now = make_datetime(2021, 2, 5)
        self.assertEqual(
            (False, True, False, make_datetime(2021, 1, 1), make_datetime(2021, 2, 1)),
            get_next_claim_time(predicate, now),
        )

    def test_except_period_predicate(self):
        predicate = {
            'or': [
                {
                    'abs_before': '2021-01-01T00:00:00Z',
                },
                {
                    'not': {
                        'abs_before': '2021-02-01T00:00:00Z',
                    },
                },
            ],
        }

        # Case 5
        now = make_datetime(2020, 12, 31)
        self.assertEqual(
            (True, False, False, None, make_datetime(2021, 1, 1)),
            get_next_claim_time(predicate, now),
        )

        # Case 6
        now = make_datetime(2021, 1, 5)
        self.assertEqual(
            (False, False, False, make_datetime(2021, 2, 1), None),
            get_next_claim_time(predicate, now),
        )

        # Case 7
        now = make_datetime(2021, 2, 5)
        self.assertEqual(
            (True, False, False, None, None),
            get_next_claim_time(predicate, now),
        )

    def test_conflict_period_predicate(self):
        predicate = {
            'and': [
                {
                    'abs_before': '2021-01-01T00:00:00Z',
                },
                {
                    'not': {
                        'abs_before': '2021-02-01T00:00:00Z',
                    },
                },
            ],
        }

        # Case 11
        now = make_datetime(2020, 1, 1)
        self.assertEqual(
            (False, False, True, None, None),
            get_next_claim_time(predicate, now),
        )

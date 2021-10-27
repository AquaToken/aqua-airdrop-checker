from datetime import datetime
from typing import List, Optional, Tuple, Union

from dateutil.parser import parse as date_parse

from aqua_airdrop_checker.utils.time_periods import Period, intersect_periods, negate_periods, unite_periods


def is_unconditional_predicate(predicate: dict) -> bool:
    return 'unconditional' in predicate


def is_or_predicate(predicate: dict) -> bool:
    return 'or' in predicate


def is_and_predicate(predicate: dict) -> bool:
    return 'and' in predicate


def is_not_predicate(predicate: dict) -> bool:
    return 'not' in predicate


def is_abs_before_predicate(predicate: dict) -> bool:
    return 'abs_before' in predicate


def parse_predicate(predicate: dict) -> List[Period]:
    """
    Parse predicate dictionary to sorted list of periods.

    :param predicate:
    :return:
    """
    if is_unconditional_predicate(predicate):
        return [
            Period(None, None),
        ]

    if is_abs_before_predicate(predicate):
        return [
            Period(None, date_parse(predicate['abs_before'])),
        ]

    if is_or_predicate(predicate):
        return unite_periods(
            parse_predicate(predicate['or'][0]),
            parse_predicate(predicate['or'][1]),
        )

    if is_and_predicate(predicate):
        return intersect_periods(
            parse_predicate(predicate['and'][0]),
            parse_predicate(predicate['and'][1]),
        )

    if is_not_predicate(predicate):
        return negate_periods(
            parse_predicate(predicate['not']),
        )


def get_next_claim_time(
    predicate: dict, now: Union[datetime, str],
) -> Tuple[bool, bool, bool, Optional[datetime], Optional[datetime]]:
    """
    Look up the closest time of claim balance based on predicate.
    Return a tuple of (can_claim_now, expired, conflict, period_start, period_end),
    where period_start and period_end are borders of closest time period of claim.

    :param predicate: Claimable balance predicate.
    :param now: Current time.
    :return: (can_claim_now, expired, conflict, period_start, period_end)
    """
    if isinstance(now, str):
        now = date_parse(now)

    periods_list = parse_predicate(predicate)

    if len(periods_list) == 0:
        # Conflict time periods.
        return (
            False,
            False,
            True,
            None,
            None,
        )

    for period in periods_list:
        if period.end < now:
            continue

        if period.start <= now <= period.end == Period.get_max_value():
            # If all time limit stay in the past we don't show them.
            return (
                True,
                False,
                False,
                None,
                None,
            )

        if period.start <= now <= period.end:
            return (
                True,
                False,
                False,
                period.get_valuable_start(),
                period.get_valuable_end(),
            )

        if now < period.start:
            return (
                False,
                False,
                False,
                period.get_valuable_start(),
                period.get_valuable_end(),
            )

    # Expired.
    return (
        False,
        True,
        False,
        periods_list[-1].get_valuable_start(),
        periods_list[-1].get_valuable_end(),
    )

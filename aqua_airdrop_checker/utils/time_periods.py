from datetime import datetime
from typing import List, Optional

import pytz


class Period:
    def __init__(self, start: Optional[datetime], end: Optional[datetime]):
        if start is None:
            self.start = self.get_min_value()
        else:
            self.start = start

        if end is None:
            self.end = self.get_max_value()
        else:
            self.end = end

    def __str__(self):
        return f'({self.start}, {self.end})'

    def __repr__(self):
        return f'Period({self.start}, {self.end})'

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def get_valuable_start(self):
        return self.start if self.start > self.get_min_value() else None

    def get_valuable_end(self):
        return self.end if self.end < self.get_max_value() else None

    @staticmethod
    def get_min_value() -> datetime:
        return pytz.utc.localize(datetime.min)

    @staticmethod
    def get_max_value() -> datetime:
        return pytz.utc.localize(datetime.max)


def unite_periods(period_list1: List[Period], period_list2: List[Period]) -> List[Period]:
    """
    Unite two periods lists.

    :param period_list1:
    :param period_list2:
    :return:
    """
    joined_list = period_list1 + period_list2
    joined_list.sort(key=lambda period: period.start)

    current_period = joined_list[0]
    result_list = []
    # Go through sorted union of periods and look for intersected periods. Unite them into new one.
    for new_period in joined_list[1:]:
        if current_period.end < new_period.start:
            # Periods do not intersect.
            result_list.append(current_period)
            current_period = new_period
            continue

        # Unite periods.
        current_period = Period(
            start=min(current_period.start, new_period.start),
            end=max(current_period.end, new_period.end),
        )

    result_list.append(current_period)
    return result_list


def intersect_periods(period_list1: List[Period], period_list2: List[Period]) -> List[Period]:
    """
    Intersect two sorted periods lists.

    :param period_list1:
    :param period_list2:
    :return:
    """
    index1 = 0
    index2 = 0
    result_list = []
    # Go through two lists in parallel. Look for period intersection.
    while index1 < len(period_list1) and index2 < len(period_list2):
        period1 = period_list1[index1]
        period2 = period_list2[index2]

        if period1.end < period2.start:
            # period1 ends before period2. Take next one.
            index1 += 1
            continue

        if period2.end < period1.start:
            # period2 ends before period1. Take next one.
            index2 += 1
            continue

        # Intersect periods.
        result_list.append(Period(
            start=max(period1.start, period2.start),
            end=min(period1.end, period2.end),
        ))

        if period1.end > period2.end:
            index2 += 1
        else:
            index1 += 1

    return result_list


def negate_periods(period_list: List[Period]) -> List[Period]:
    """
    Negate sorted periods list.

    :param period_list:
    :return:
    """
    result_list = []
    # Starts at minus infinite.
    previous_end = Period.get_min_value()
    # Go through list. Create new period base on the end of previous and start on current.
    for period in period_list:
        if period.start == Period.get_min_value():
            # Current period doesn't have start. Skip it.
            previous_end = period.end
            continue

        result_list.append(Period(
            start=previous_end,
            end=period.start,
        ))
        previous_end = period.end

    if previous_end != Period.get_max_value():
        # If last period has finite end then we add the remainder of time ray as last period.
        result_list.append(Period(
            start=previous_end,
            end=Period.get_max_value(),
        ))

    return result_list

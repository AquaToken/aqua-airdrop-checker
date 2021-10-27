from django.conf import settings
from django.utils import timezone

from stellar_sdk import Server

from aqua_airdrop_checker.airdrop.models import AirdropPayment
from aqua_airdrop_checker.utils.claimable_balances import parse_predicate


def process_operations_to_state(operations, destination):
    create_operation = next(op for op in operations if op['type'] == 'create_claimable_balance')
    claimant = next(filter(lambda c: c['destination'] == destination, create_operation['claimants']))

    [period] = parse_predicate(claimant['predicate'])

    if len(operations) > 1:
        claim_operation = next(filter(lambda o: o['type'] == 'claim_claimable_balance', operations))

        if claim_operation['source_account'] == destination:
            return {
                'state': AirdropPayment.STATE_CLAIMED,
                'start': period.start,
                'end': period.end,
            }
        else:
            return {
                'state': AirdropPayment.STATE_EXPIRED,
                'start': period.start,
                'end': period.end,
            }

    now = timezone.now()
    if period.end < now:
        return {
            'state': AirdropPayment.STATE_EXPIRED,
            'start': period.start,
            'end': period.end,
        }

    if period.start < now:
        return {
            'state': AirdropPayment.STATE_WAITING,
            'start': period.start,
            'end': period.end,
        }

    return {
        'state': AirdropPayment.STATE_COMING,
        'start': period.start,
        'end': period.end,
    }


def load_payment_state(destination, payment, horizon_server: Server):
    response = horizon_server.operations().for_claimable_balance(payment.balance_id).call()

    state = process_operations_to_state(response['_embedded']['records'], destination)

    payment.state = state['state']
    payment.start = state['start']
    payment.end = state['end']


def attach_payment_list_state(destination, payment_list):
    horizon_server = Server(settings.HORIZON_URL)
    for payment in payment_list:
        load_payment_state(destination, payment, horizon_server)

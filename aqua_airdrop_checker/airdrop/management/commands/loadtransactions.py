import asyncio

from django.conf import settings
from django.core.management import BaseCommand, CommandParser

from asgiref.sync import sync_to_async
from stellar_sdk import AiohttpClient, Server
from stellar_sdk.xdr import OperationResult, TransactionResult

from aqua_airdrop_checker.airdrop.models import AirdropAccount, AirdropPayment
from aqua_airdrop_checker.utils.claimable_balances import parse_predicate


class Command(BaseCommand):
    _horizon_server = None

    phase = None

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('file')
        parser.add_argument('--phase', type=int)

    def handle(self, *args, **options):
        self.phase = options['phase']
        transactions_file = options['file']

        with open(transactions_file, 'r') as f:
            transactions = [line.strip() for line in f.readlines()]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([
            self.process_transaction(transaction_hash)
            for transaction_hash in transactions
        ]))
        self.horizon_server.close()
        loop.close()

        self.stdout.write(f'Processed {len(transactions)} transactions.')

    def get_horizon_server(self):
        return Server(settings.HORIZON_URL, client=AiohttpClient())

    @property
    def horizon_server(self):
        if not self._horizon_server:
            self._horizon_server = self.get_horizon_server()

        return self._horizon_server

    async def process_transaction(self, transaction_hash):
        info_list = await self.load_transaction_info(transaction_hash)

        payment_count = await sync_to_async(self.save_airdrop_payment_info, thread_sensitive=True)(info_list)

        self.stdout.write(f'Saved transaction {transaction_hash}: {payment_count}')

    async def load_transaction_info(self, transaction_hash):
        response = await self.horizon_server.transactions().transaction(transaction_hash).call()
        transaction_result = TransactionResult.from_xdr(response['result_xdr'])
        if transaction_result.result.inner_result_pair:
            transaction_result = transaction_result.result.inner_result_pair.result

        response = await self.horizon_server.operations().for_transaction(transaction_hash).limit(200).call()
        operations = response['_embedded']['records']

        return [
            {
                'transaction_id': transaction_hash,
                **self.parse_horizon_response(operation, transaction_result.result.results[index]),
            }
            for index, operation in enumerate(operations)
            if operation['type'] == 'create_claimable_balance'
        ]

    def parse_horizon_response(self, operation: dict, operation_result: OperationResult):
        # Zeros are used to encode the balance_id version.
        balance_id = '00000000' + operation_result.tr.create_claimable_balance_result.balance_id.v0.hash.hex()
        operation_id = operation['id']

        claimants = operation['claimants']
        # Main destination account for a claimable balance is selected based on time periods.
        claimants.sort(key=lambda c: parse_predicate(c['predicate'])[0].start)
        destination = claimants[0]['destination']

        return {
            'destination': destination,
            'operation_id': operation_id,
            'balance_id': balance_id,
        }

    def save_airdrop_payment_info(self, info_list):
        airdrop_accounts = (AirdropAccount.objects.filter(public_key__in=[info['destination'] for info in info_list])
                            .only('id', 'public_key'))
        destination_map = {
            account.public_key: account.id for account in airdrop_accounts
        }

        payments = [
            AirdropPayment(
                account_id=destination_map[info['destination']],
                phase=self.phase,
                balance_id=info['balance_id'],
                transaction_id=info['transaction_id'],
                operation_id=info['operation_id'],
            )
            for info in info_list
            if info['destination'] in destination_map
        ]

        AirdropPayment.objects.bulk_create(payments)

        return len(payments)

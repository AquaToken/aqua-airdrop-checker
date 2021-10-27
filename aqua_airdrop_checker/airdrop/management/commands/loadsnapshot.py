from django.core.management import BaseCommand, CommandParser

from dateutil.parser import parse

from aqua_airdrop_checker.airdrop.models import AirdropAccount


class Command(BaseCommand):
    BATCH_SIZE = 1000

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('snapshot')

    def handle(self, *args, **options):
        snapshot = options['snapshot']

        self.stdout.write(f'Parsing {snapshot}...')

        account_list = []

        with open(snapshot, 'r') as snapshot:
            for index, line in enumerate(snapshot.readlines()):
                self.stdout.write(f'Read account {index}.')

                (
                    public_key, horizon_id, trades_count,
                    lobstr_domain, stellarterm_domain, stellarx_domain, created_at,
                ) = line.strip().split(',')

                account = AirdropAccount(
                    public_key=public_key,
                    horizon_id=int(horizon_id),
                    trades_count=int(trades_count),
                    lobstr_domain=len(lobstr_domain) > 0,
                    stellarterm_domain=len(stellarterm_domain) > 0,
                    stellarx_domain=len(stellarx_domain) > 0,
                    created_at=parse(created_at),
                )

                account.boost = 1
                account.boost *= 2 if account.has_trades_count_boost() else 1
                account.boost *= 2 if account.has_product_usage_boost() else 1
                account.boost *= 2 if account.has_account_age_boost() else 1

                account_list.append(account)

                if len(account_list) >= self.BATCH_SIZE:
                    AirdropAccount.objects.bulk_create(account_list)
                    account_list = []

            AirdropAccount.objects.bulk_create(account_list)

        self.stdout.write(f'Parsed {index+1} objects.')

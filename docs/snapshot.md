Create snapshot
================


Synchronized Horizon instance is required to make a snapshot. Horizon database is used to load the relevant data. You can use [copy command](https://postgrespro.com/docs/postgresql/9.5/app-psql#app-psql-meta-commands-copy) to save data to a file for your further needs.

1. Collect the IDs of the accounts that made trades before the set date (2021-01-01):
   ```sql
   SELECT "base_account_id", "counter_account_id" FROM "history_trades" WHERE "ledger_closed_at" < '2021/01/01T00:00:00Z'
   ```
   This selection allows you to identify all unique accounts and the number of trades made by each of these accounts.


2. Map horizon history IDs to public keys using data from history_accounts table. To filter by data from the previous step, create a temporary table and load unique IDs:
   ```sql
   CREATE TEMPORARY TABLE "account_ids" ("account_id" integer)
   \copy account_ids(account_id) FROM 'unique_account_history_id.csv' WITH CSV
   ```
   Collect unique account IDs
   ```sql
   SELECT "address" FROM "account_ids" INNER JOIN "history_accounts" ON "account_id" = "id"
   ```


3. Identify accounts that had a home domain property set. Select all SetOptions operations (type = 5) with a home domain specified:
   ```sql
   SELECT "source_account" FROM "history_operations" WHERE "type" = 5 and "details" @> '{"home_domain": "<home_domain>"}'::jsonb
   ```


4. Identify the creation date for an account. Repeat this request for every unique account identified at the second step:
   ```sql
   SELECT hl.closed_at, ho.details->>'account' FROM history_operations ho LEFT JOIN history_transactions ht ON ho.transaction_id = ht.id LEFT JOIN history_ledgers hl ON ht.ledger_sequence = hl.sequence JOIN history_operation_participants hop ON ho.id = hop.history_operation_id LEFT JOIN history_accounts ha ON ha.id = hop.history_account_id WHERE ho.type = 0 AND ha.address = '<public_key>' ORDER BY ho.id LIMIT 1
   ```

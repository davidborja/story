from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from template.models import Template
from transaction.models import Transaction
from account.models import Account
from accountType.models import AccountType
from user.models import User
from django.db import models
from django.db.models import Sum
import csv
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = "Send emails to users based on a template"

    def add_arguments(self, parser):
        # files/test.csv
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to CSV file containing the financial information",
        )

    def handle(self, *args, **options):
        datetime_now = datetime.now()
        date_now = datetime_now.date()
        dict_date = {}
        new_date = date_now

        while new_date.year > date_now.year - 1:
            date_string = new_date.strftime("%B")
            interval_date_begin = date(new_date.year, new_date.month, 1)
            interval_date_end = (
                interval_date_begin + relativedelta(months=1)
            ) - relativedelta(days=1)
            dict_date.update(
                {
                    date_string: {
                        "interval_date_begin": interval_date_begin,
                        "interval_date_end": interval_date_end,
                    }
                }
            )
            new_date = new_date - relativedelta(months=1)

        file_path = options["file_path"]

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                account_id = int(row[0])
                date_account = row[1]
                transaction = row[2]

                if transaction[0] == "+":
                    transaction_type = "credit"
                elif transaction[0] == "-":
                    transaction_type = "debit"

                account_type = AccountType.objects.get(type=transaction_type)
                date_object = datetime.strptime(date_account, "%d/%m/%Y")
                formatted_date = date_object.strftime("%Y-%m-%d")

                transaction = Transaction(
                    amount=transaction[1:], movement_date=formatted_date
                )
                transaction.save()
                account_obj = Account.objects
                account = account_obj.get(pk=account_id, account_type=account_type)
                account.transaction.add(transaction)
                account.save()
                print(f"{account_id} {date_account} {transaction}")

        users_information = []
        account_credit = AccountType.objects.get(type="credit")
        account_debit = AccountType.objects.get(type="debit")

        for user in User.objects.all():
            user_date_information = {}
            full_name = f"{user.name} {user.last_name}"
            email = user.email
            user_account_credit = Account.objects.filter(
                user=user, account_type=account_credit
            )
            user_account_debit = Account.objects.filter(
                user=user, account_type=account_debit
            )

            total_amount_credit = 0
            total_amount_debit = 0

            if len(user_account_credit) > 0:
                transactions = user_account_credit[0].transaction.all()
                for key, value in dict_date.items():
                    transaction_count = transactions.filter(
                        movement_date__range=(
                            value["interval_date_begin"],
                            value["interval_date_end"],
                        )
                    ).count()
                    total_amount_credit_by_month = transactions.filter(
                        movement_date__range=[
                            value["interval_date_begin"],
                            value["interval_date_end"],
                        ]
                    ).aggregate(total_amount=Sum("amount"))["total_amount"]

                    if total_amount_credit_by_month is None:
                        total_amount_credit_by_month = 0

                    if transaction_count == 0:
                        credit_amount_transactions = 0
                    else:
                        credit_amount_transactions = float(
                            total_amount_credit_by_month
                        ) / float(transaction_count)

                    user_date_information.update(
                        {
                            f"credit_amount_transactions_{key}": credit_amount_transactions
                        }
                    )
                    if "count_transactions_{key}" in user_date_information:
                        user_date_information["count_transactions_{key}"] = (
                            user_date_information["count_transactions_{key}"]
                            + transaction_count
                        )
                    else:
                        user_date_information.update(
                            {f"count_transactions_{key}": transaction_count}
                        )

                total_amount_credit = transactions.aggregate(
                    total_amount=models.Sum("amount")
                )["total_amount"]

            if len(user_account_debit) > 0:
                transactions = user_account_debit[0].transaction.all()
                for key, value in dict_date.items():
                    transaction_count = transactions.filter(
                        movement_date__range=(
                            value["interval_date_begin"],
                            value["interval_date_end"],
                        )
                    ).count()
                    total_amount_debit_by_month = transactions.filter(
                        movement_date__range=[
                            value["interval_date_begin"],
                            value["interval_date_end"],
                        ]
                    ).aggregate(total_amount=Sum("amount"))["total_amount"]

                    if total_amount_debit_by_month is None:
                        total_amount_debit_by_month = 0

                    if transaction_count == 0:
                        debit_amount_transactions = 0
                    else:
                        debit_amount_transactions = float(
                            total_amount_debit_by_month
                        ) / float(transaction_count)

                    user_date_information.update(
                        {f"debit_amount_transactions_{key}": debit_amount_transactions}
                    )

                    if "count_transactions_{key}" in user_date_information:
                        user_date_information["count_transactions_{key}"] = (
                            user_date_information["count_transactions_{key}"]
                            + transaction_count
                        )
                    else:
                        user_date_information.update(
                            {f"count_transactions_{key}": transaction_count}
                        )

                total_amount_debit = transactions.aggregate(
                    total_amount=models.Sum("amount")
                )["total_amount"]

            total_balance = float(total_amount_debit - total_amount_credit)

            user_data = {
                "full_name": full_name,
                "email": email,
                "total_balance": total_balance,
                "transactions": user_date_information,
            }
            users_information.append(user_data)

        # Send emails
        for user in users_information:
            email_template = Template.objects.get(pk=1)
            subject = email_template.subject
            # html = email_template.html
            # html = html.replace("#full_name#", user.get('full_name'))
            # html = html.replace("#totalBalance#", str(user.get('total_balance')))
            html = str(user)
            send_mail(
                subject,
                html,
                "borjacazalesdavid@gmail.com",
                [user.get("email")],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Successfully sent emails"))

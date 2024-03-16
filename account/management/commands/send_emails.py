from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from template.models import Template
from transaction.models import Transaction
from account.models import Account
from accountType.models import AccountType
from user.models import User
from django.db import models
import csv
from datetime import datetime


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
        file_path = options["file_path"]

        email_template = Template.objects.get(pk=1)
        subject = email_template.subject
        html = email_template.html

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                account_id = int(row[0])
                date = row[1]
                transaction = row[2]

                if transaction[0] == "+":
                    transaction_type = "credit"
                elif transaction[0] == "-":
                    transaction_type = "debit"

                account_type = AccountType.objects.get(type=transaction_type)
                date_object = datetime.strptime(date, "%d/%m/%Y")
                formatted_date = date_object.strftime("%Y-%m-%d")

                transaction = Transaction(
                    amount=transaction[1:], movement_date=formatted_date
                )
                transaction.save()
                account_obj = Account.objects
                account = account_obj.get(pk=account_id, account_type=account_type)
                account.transaction.add(transaction)
                account.save()
                print(f"{account_id} {date} {transaction}")

        recipients = ["freestimulation@gmail.com"]

        user_information = []
        account_credit = AccountType.objects.get(type="credit")
        account_debit = AccountType.objects.get(type="debit")

        for user in User.objects.all():
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
                total_amount_credit = transactions.aggregate(
                    total_amount=models.Sum("amount")
                )["total_amount"]

            if len(user_account_debit) > 0:
                transactions = user_account_debit[0].transaction.all()
                total_amount_debit = transactions.aggregate(
                    total_amount=models.Sum("amount")
                )["total_amount"]

            total_balance = total_amount_debit - total_amount_credit

            user_data = {
                "full_name": full_name,
                "email": email,
                "total_balance": total_balance,
            }
            user_information.append(user_data)

        print(user_information)

        # Send emails
        for recipient in recipients:
            send_mail(
                subject,
                html,
                "borjacazalesdavid@gmail.com",
                [recipient],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Successfully sent emails"))

from sqlalchemy import func, and_
from datetime import datetime, date
from application.extensions import db
from sqlalchemy import extract

from .. account import Account
from .. books_of_accounts.receipt import Receipt, ReceiptDetail
from .. books_of_accounts.sales import Sales, SalesDetail
from .. books_of_accounts.disbursement import Disbursement, DisbursementDetail
from .. books_of_accounts.accounts_payable import AccountsPayable, AccountsPayableDetail


def get_account_balances_up_to(target_date_str):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    # Combine results into a dictionary
    account_totals = {}

    books = [
        (Receipt, ReceiptDetail),
    ]
    
    for Obj, ObjDetail in books:
        # Sum from ReceiptDetail
        query = (
            db.session.query(
                ObjDetail.account_id,
                func.sum(ObjDetail.debit - ObjDetail.credit).label('balance')
            )
            .join(Obj)
            .filter(Obj.record_date <= target_date_str)
            .group_by(ObjDetail.account_id)
        ).all()
        
        # Combine sales results
        for account_id, balance in query:
            account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    # Sum from SalesDetail
    sales_query = (
        db.session.query(
            SalesDetail.account_id,
            func.sum(SalesDetail.debit - SalesDetail.credit).label('balance')
        )
        .join(Sales)
        .filter(Sales.record_date <= target_date_str)
        .group_by(SalesDetail.account_id)
    ).all()

    # Sum from DisbursementDetail
    disbursement_query = (
        db.session.query(
            DisbursementDetail.account_id,
            func.sum(DisbursementDetail.debit - DisbursementDetail.credit).label('balance')
        )
        .join(Disbursement)
        .filter(Disbursement.record_date <= target_date_str)
        .group_by(DisbursementDetail.account_id)
    ).all()




    # Combine sales results
    for account_id, balance in sales_query:
        account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    # Combine disbursement results
    for account_id, balance in disbursement_query:
        account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    # Convert account_id to account title
    result = {}
    for account_id, balance in account_totals.items():
        account = Account.query.get(account_id)
        if account:
            result[account.account_title] = round(balance, 2)

    return result


def get_account_balances_in_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # ReceiptDetails within date range
    receipt_query = (
        db.session.query(
            ReceiptDetail.account_id,
            func.sum(ReceiptDetail.debit - ReceiptDetail.credit).label('balance')
        )
        .join(Receipt)
        .filter(and_(
            Receipt.record_date >= start_date_str,
            Receipt.record_date <= end_date_str
        ))
        .group_by(ReceiptDetail.account_id)
    ).all()

    # SalesDetails within date range
    sales_query = (
        db.session.query(
            SalesDetail.account_id,
            func.sum(SalesDetail.debit - SalesDetail.credit).label('balance')
        )
        .join(Sales)
        .filter(and_(
            Sales.record_date >= start_date_str,
            Sales.record_date <= end_date_str
        ))
        .group_by(SalesDetail.account_id)
    ).all()

    # DisbursementDetails within date range
    disbursement_query = (
        db.session.query(
            DisbursementDetail.account_id,
            func.sum(DisbursementDetail.debit - DisbursementDetail.credit).label('balance')
        )
        .join(Disbursement)
        .filter(and_(
            Disbursement.record_date >= start_date_str,
            Disbursement.record_date <= end_date_str
        ))
        .group_by(DisbursementDetail.account_id)
    ).all()

    # Merge balances from both queries
    account_totals = {}

    for account_id, balance in receipt_query:
        account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    for account_id, balance in sales_query:
        account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    for account_id, balance in disbursement_query:
        account_totals[account_id] = account_totals.get(account_id, 0) + (balance or 0)

    # Resolve account titles and return summary
    result = {}
    for account_id, balance in account_totals.items():
        account = Account.query.get(account_id)
        if account:
            result[account.account_title] = round(balance, 2)

    return result


def get_account_balance_summary(today=None):
    if today is None:
        today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    # First day of current month
    first_day_month = today.replace(day=1)
    first_day_month_str = first_day_month.strftime("%Y-%m-%d")

    # Dec 31 of last year
    dec_31_last_year = date(today.year - 1, 12, 31)
    dec_31_last_year_str = dec_31_last_year.strftime("%Y-%m-%d")

    # Balances
    mtd = get_account_balances_in_range(first_day_month_str, today_str)
    last_year_end = get_account_balances_up_to(dec_31_last_year_str)
    total = get_account_balances_up_to(today_str)

    # Merge account titles
    all_titles = set(mtd.keys()) | set(last_year_end.keys()) | set(total.keys())

    combined = {}
    for title in all_titles:
        combined[title] = {
            'MTD': round(mtd.get(title, 0), 2),
            'Last Year End': round(last_year_end.get(title, 0), 2),
            'Total': round(total.get(title, 0), 2)
        }

    return combined

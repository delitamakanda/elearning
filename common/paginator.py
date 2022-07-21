from django.core.paginator import Paginator
from django.utils.functional import cached_property
from django.db import connection, transaction, OperationalError

class TimeLimitedPaginator(Paginator):

    """
    Paginator that enforces a timeout on the count operation.
    If the operations times out, a fake bogus value will be returned is returned instead
    """
    
    @cached_property
    def count(self):
        """
        set timeout to in a db transaction to prevent it from affecting other transactions.
        """
        try:
            with transaction.atomic(), connection.cursor() as cursor:
                cursor.execute('SET LOCAL statement_timeout TO 200;')
                return super().count
        except OperationalError:
            return 9999999999
            

class DumbPaginator(Paginator):
    """
    Paginator that does count the rows of a given table
    """
    @cached_property
    def count(self):
        return 9999999999

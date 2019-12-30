"""
Provides the manager for the invoice management models
"""

from django.db import models


class InvoiceDetailManager(models.Manager):
    """
    Custom Manager for handling InvoiceDetail model queries.
    """
    def get_queryset(self):
        query_set = super(InvoiceDetailManager, self).get_queryset()
        return query_set.select_related('seller',
                                        'buyer',
                                        'seller__address',
                                        'buyer__address')

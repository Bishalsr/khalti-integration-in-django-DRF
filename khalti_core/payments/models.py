from django.db import models
import uuid


class Payment(models.Model):

    STATUS_CHOICES = [
        ("Initiated", "Initiated"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Expired", "Expired"),
        ("Failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order_id = models.CharField(max_length=200, unique=True)
    pidx = models.CharField(max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField()  # in paisa
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Initiated")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purchase_order_id} - {self.status}"

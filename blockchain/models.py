from django.db import models
from django.contrib.auth.models import User

# BlockchainTransaction: 
class BlockchainTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=255)  # Ethereum transaction hash
    details = models.TextField()  
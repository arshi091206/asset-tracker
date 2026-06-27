from django.db import models

# Create your models here.
class Alert(models.Model):
    ASSET_CHOICES=[
        ("stock","Stock"),
        ("crypto","Crypto"),
        ("gold","Gold"),
        ("forex","Forex"),
    ]
    CONDITION_CHOICES=[
        ("below","Below"),
        ("above","Above"),
    ]
    ticker=models.CharField(max_length=20)
    asset_type=models.CharField(max_length=20, choices=ASSET_CHOICES)
    condition=models.CharField(max_length=10, choices=CONDITION_CHOICES)
    target_price=models.DecimalField(max_digits=10,decimal_places=2)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
    
    
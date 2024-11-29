from typing import Any
from django.db import models

# Create your models here.
class PageVisit(models.Model):
    # db -> Table
    # id -> hidden -> priKey -> autofield -> 1, 2, 3 ...n
    path = models.TextField(null=True, blank=True) # column
    timestamp = models.DateTimeField(auto_now_add=True) # column
    
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
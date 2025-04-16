from django.db import models

class Todo(models.Model):
    task = models.CharField(max_length = 180)
    completed = models.BooleanField(default = False, blank = True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)

    def __str__(self):
        return self.task
from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill  # 👈 import the Skill model

class Swap(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_swaps')  # Skill giver
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_swaps')  # Skill receiver
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # The skill to be swapped
    message = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} swaps {self.skill.title} to {self.receiver.username}"

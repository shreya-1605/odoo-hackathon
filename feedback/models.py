from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill  # Avoid circular import

class Feedback(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s feedback on {self.skill.title}"

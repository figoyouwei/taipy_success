import uuid
from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's default User model

# NOTE: add Answer model
class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)  # The question that was answered
    selected_choice = models.ForeignKey('Choice', on_delete=models.CASCADE)  # The selected choice
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the answer

    def __str__(self):
        return f"selected {self.selected_choice.symbol} for {self.question.text}"


class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Creative', '创新型企业'),
        ('Specialized', '专精特新'),
        ('LittleGiant', '专精特新小巨人'),
    ]

    identifier = models.CharField(max_length=32, unique=True, null=True, blank=True)  # Temporarily allow null values
    text = models.CharField(max_length=255)  # The question text
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Creative')  # Category field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set the date when the question is created

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = uuid.uuid4().hex  # Generate a random unique string
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.text

    # NOTE: via ForeignKey -> related_name
    def get_choices(self) -> list:
        """Return all related Choice instances as a list."""
        return list(self.choices.all())  # Convert QuerySet to list

    def get_selected_choice(self, symbol_no: str):
        """Store or update the selected choice based on symbol number."""
        try:
            selected_choice = self.choices.get(symbol_no=symbol_no)
            return selected_choice
        except Choice.DoesNotExist:
            return None


class Choice(models.Model):
    SYMBOL_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
        
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)  # Link to the Question
    symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES, default='A')  # Symbol for the choice (A, B, C, D, E)
    symbol_no = models.IntegerField(default=1)  # Symbol number
    text = models.CharField(max_length=255, default='Please ask a question')  # The choice text
    score = models.IntegerField(default=0)  # Score associated with the choice

    def __str__(self):
        return f"{self.symbol}: {self.text} with Score: {self.score}"

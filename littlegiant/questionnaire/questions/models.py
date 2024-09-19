import uuid
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User  # Assuming you are using Django's default User model

# ------------------------------
# Client without using Django native User
# ------------------------------

class Client(models.Model):
    name = models.CharField(max_length=255)  # Full name of the user
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Company name of the user

    def __str__(self):
        return f"{self.name} from {self.company_name}"

# ------------------------------
# Answer
# ------------------------------

from django.core.exceptions import ObjectDoesNotExist

def get_default_client():
    first_client = Client.objects.first()  # Get the first Client object
    if first_client:
        return first_client.id  # Return the id of the first Client
    raise ValueError("No Client exists in the database.")  # Raise an error if no clients exist

class Answer(models.Model):
    client = models.ForeignKey(
            Client, 
            on_delete=models.CASCADE, 
            default=get_default_client  # Use the function to set the default value
        )
    question = models.ForeignKey('Question', on_delete=models.CASCADE)  # The question that was answered
    selected_choice = models.ForeignKey('Choice', on_delete=models.CASCADE)  # The selected choice
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the answer

    def __str__(self):
        return f"{self.client.name}: selected {self.selected_choice.symbol} for {self.question.text}"

# ------------------------------
# Question
# ------------------------------

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Creative', '创新型企业'),
        ('Specialized', '专精特新'),
        ('LittleGiant', '专精特新小巨人'),
        ('Test', '测试问题')
    ]

    identifier = models.CharField(max_length=32, unique=True, null=True, blank=True)  # Temporarily allow null values
    text = models.CharField(max_length=255)  # The question text
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Creative')  # Category field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set the date when the question is created
    display_order = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = uuid.uuid4().hex  # Generate a random unique string
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return f"Question: {self.text}"

    # NOTE: via ForeignKey -> related_name
    def get_choices(self) -> list:
        """Return all related Choice instances as a list."""
        return list(self.choices.all())  # Convert QuerySet to list

    def get_choice_by_symbol(self, symbol: str):
        """Return single choice by symbol."""
        try:
            selected_choice = self.choices.get(symbol=symbol)
            return selected_choice
        except Choice.DoesNotExist:
            return None

# ------------------------------
# Choice
# ------------------------------

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
    text = models.CharField(max_length=255, default='Please ask a question')  # The choice text
    score = models.IntegerField(default=0)  # Score associated with the choice

    class Meta:
        unique_together = ('question', 'symbol')  # Unique constraint on question and symbol
        
    def __str__(self):
        return f"{self.symbol}: {self.text} with Score: {self.score}"

# ------------------------------
# UserProfile using Django native User
# ------------------------------

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the default User model
#     name = models.CharField(max_length=255)  # Full name of the user
#     company_name = models.CharField(max_length=255, blank=True, null=True)  # Company name of the user

#     def __str__(self):
#         return f"{self.user.username}'s profile"

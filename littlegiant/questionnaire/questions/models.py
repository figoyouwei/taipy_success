from django.db import models

class Question(models.Model):
    CATEGORY_CHOICES = [
            ('Creative', '创新型企业'),
            ('Specialized', '专精特新'),
            ('LittleGiant', '专精特新小巨人'),
        ]

    text = models.CharField(max_length=255)  # The question text
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='geography')  # Category field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set the date when the question is created

    def __str__(self):
        return self.text  # This will display the question text in the admin panel

    def get_choices(self) -> list:
            """Return all related choices as a list."""
            return list(self.choices.all())  # Convert QuerySet to list

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
    symbol_no = models.IntegerField(default=1)  # symbol_no
    text = models.CharField(max_length=255, default='Please ask a question')  # The choice text
    score = models.IntegerField(default=0)  # Score associated with the choice

    def __str__(self):
        return f"{self.symbol}: {self.text} with Score: {self.score}"

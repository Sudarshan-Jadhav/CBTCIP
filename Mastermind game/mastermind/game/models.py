from django.db import models
import random

class Game(models.Model):
    COLORS = [('R', 'Red'), ('G', 'Green'), ('B', 'Blue'), ('Y', 'Yellow'), ('O', 'Orange'), ('P', 'Purple')]
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = ''.join(random.choice('RGBYOP') for _ in range(4))
        self.save()

    def check_guess(self, guess):
        result = {'correct': 0, 'wrong_position': 0}
        temp_code = list(self.code)

        # First pass: check correct positions
        for i in range(4):
            if guess[i] == temp_code[i]:
                result['correct'] += 1
                temp_code[i] = None

        # Second pass: check wrong positions
        for i in range(4):
            if guess[i] in temp_code and guess[i] != self.code[i]:
                result['wrong_position'] += 1
                temp_code[temp_code.index(guess[i])] = None

        return result

class Attempt(models.Model):
    game = models.ForeignKey(Game, related_name='attempts', on_delete=models.CASCADE)
    guess = models.CharField(max_length=4)
    correct = models.IntegerField()
    wrong_position = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

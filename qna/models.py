from accounts.models import User
from django.db import models
from .base import BaseModel
import random


class Poll(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='polls')
    text = models.TextField()
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.votes.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.votes.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = random.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class Choice(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,related_name="choice")
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.votes.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE,related_name='votes')

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'inflationbias'
    players_per_group = 3
    num_rounds = 15
    maxpayoff = 40
    inflation_target = 3.5
    new_target = 5
    instructions_template = 'inflationbias/instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for g in self.get_groups():
                p1 = g.get_player_by_id(1)
                p1.participant.vars['treatment'] = random.choice(['shock', 'reform', 'no_reform', 'mid_reform'])


class Group(BaseGroup):
    inflation_mean = models.DecimalField(max_digits=9, decimal_places=2)
    actual_inflation = models.DecimalField(max_digits=9, decimal_places=2)
    deficit = models.DecimalField(max_digits=9, decimal_places=2)
    alpha = models.DecimalField(max_digits=9, decimal_places=2)
    def_fin = models.DecimalField(max_digits=9, decimal_places=2)
    treatment = models.StringField()


class Player(BasePlayer):
    name = models.StringField(label="The nickname you chose for the class:")
    age = models.IntegerField(label="Your Age:")
    country = models.StringField(label="Where are you from?")
    gender = models.IntegerField(
        label="Gender:",
        choices=[
            [1, 'Male'],
            [2, 'Female'],
        ]
    )
    experience = models.IntegerField(
        label="Have you ever experienced annual inflation greater than 10%?",
        choices=[
            [1, 'Yes'],
            [0, 'No'],
            ]
        )
    economics = models.IntegerField(
        label="Do you have previous training in Economics?",
        choices=[
            [1, 'Yes'],
            [0, 'No'],
        ]
    )

    inflation = models.DecimalField(max_digits=9, decimal_places=2)

    comments = models.LongStringField(label="What was your general strategy? Do you want to add some comments?")


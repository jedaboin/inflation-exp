import random

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from statistics import mean


class Initial(Page):
    form_model = 'player'
    form_fields = ['name', 'age', 'country', 'gender', 'experience', 'economics']

    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Prediction(Page):
    form_model = 'player'
    form_fields = ['inflation']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        p1 = self.group.get_player_by_id(1)
        group.treatment = p1.participant.vars['treatment']
        inflation = [p.inflation for p in players]
        group.inflation_mean = mean(inflation)

        if self.round_number == 1:
            group.deficit = random.gauss(4, 1)
            group.alpha = random.uniform(0, 1)
            group.def_fin = group.alpha * group.deficit
            group.actual_inflation = float(group.inflation_mean) + float(group.def_fin)

        if 5 >= self.round_number >= 2:
            group.deficit = random.gauss(4, 1)

            if self.group.in_round(self.round_number - 1).actual_inflation >= 25:
                group.alpha = random.uniform(2, 5)
            else:
                group.alpha = random.uniform(0, 1)

            group.def_fin = group.alpha*group.deficit
            group.actual_inflation = float(group.inflation_mean)+float(group.def_fin)

        if self.round_number >= 8 and group.treatment == 'reform':
            group.deficit = random.gauss(-1, 1)
            group.alpha = 0
            group.def_fin = group.alpha*group.deficit
            if self.group.in_round(self.round_number - 1).actual_inflation >= Constants.new_target:
                group.actual_inflation = float(0.85)*float(group.inflation_mean)+float(group.def_fin)
            else:
                group.actual_inflation = float(group.inflation_mean)+float(group.def_fin)

        if self.round_number >= 8 and group.treatment == 'shock':
            group.deficit = random.gauss(6, 1)

            if group.inflation_mean >= 20:
                group.alpha = random.uniform(2, 5)
            else:
                group.alpha = random.uniform(0.5, 1)

            group.def_fin = group.alpha*group.deficit
            group.actual_inflation = float(group.inflation_mean)+float(group.def_fin)

        if self.round_number >= 8 and group.treatment == 'no_reform':
            group.deficit = random.gauss(4, 1)

            if self.group.in_round(self.round_number - 1).actual_inflation >= 25:
                group.alpha = random.uniform(2, 5)
            else:
                group.alpha = random.uniform(0.5, 1)

            group.def_fin = group.alpha * group.deficit
            group.actual_inflation = float(group.inflation_mean) + float(group.def_fin)

        if self.round_number >= 8 and group.treatment == 'mid_reform':
            group.deficit = random.gauss(-1, 1)
            group.alpha = 0
            group.def_fin = group.alpha*group.deficit
            if self.group.in_round(self.round_number - 1).actual_inflation >= Constants.new_target:
                group.actual_inflation = float(0.85)*float(group.inflation_mean)+float(group.def_fin)
            else:
                group.actual_inflation = float(group.inflation_mean)+float(group.def_fin)

        for p in players:
            p.payoff = float(Constants.maxpayoff)-((group.actual_inflation-float(p.inflation))**2)


class ReformIMF(Page):
    def is_displayed(self):
        p1 = self.group.get_player_by_id(1)
        self.group.treatment = p1.participant.vars['treatment']
        return self.round_number == 8 and self.group.treatment == 'reform'


class Shock(Page):
    def is_displayed(self):
        p1 = self.group.get_player_by_id(1)
        self.group.treatment = p1.participant.vars['treatment']
        return self.round_number == 8 and self.group.treatment == 'shock'


class MidReform(Page):
    def is_displayed(self):
        p1 = self.group.get_player_by_id(1)
        self.group.treatment = p1.participant.vars['treatment']
        return self.round_number == 8 and self.group.treatment == 'mid_reform'


class Results(Page):
    pass


class Comments(Page):
    def is_displayed(self):
        return self.round_number == 15

    form_model = 'player'
    form_fields = ['comments']


class ThankYou(Page):
    def is_displayed(self):
        return self.round_number == 15


page_sequence = [
    Initial,
    Instructions,
    ReformIMF,
    Shock,
    MidReform,
    Prediction,
    ResultsWaitPage,
    Results,
    Comments,
    ThankYou
]

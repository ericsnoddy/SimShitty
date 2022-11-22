# reqs
import pygame as pg

# local
from .settings import RESOURCES, COSTS


class ResourceManager:
    def __init__(self):

        # resources
        self.resources = RESOURCES
        self.costs = COSTS
        

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost


    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]: 
                affordable = False
        return affordable

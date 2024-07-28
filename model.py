from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class Discriminator(Agent):
    def __init__(self, unique_id, model, color, ba):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.model = model
        self.color = color

    def step(self):
        pass


class SegregationModel(Model):
    def __init__(self, width, height, N, pRed, ba):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.pop = N
        self.schedule = RandomActivation(self)
        for i in range(int(self.pop*pRed)):
            discriminator = Discriminator(i, self, "red", ba)
            self.schedule.add(discriminator)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(discriminator, (x, y))
        for i in range(int(self.pop*(1-pRed))):
            discriminator = Discriminator(i+self.pop*pRed, self, "blue", ba)
            self.schedule.add(discriminator)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(discriminator, (x, y))
        self.datacollector = DataCollector()

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

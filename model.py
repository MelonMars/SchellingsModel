from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class Discriminator(Agent):
    def __init__(self, unique_id, model, color, ba, seed):
        super().__init__(unique_id, model)
        self.random.seed(seed)
        self.unique_id = unique_id
        self.model = model
        self.color = color
        self.ba = ba
        self.b = 0

    def step(self):
        B = 0
        N = 0
        neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for neighbour in neighbours:
            if neighbour.color == self.color:
                B += 1
            N += 1
        if N > 0:
            if self.ba > B/N:
                width = self.model.grid.width
                height = self.model.grid.height
                vacantSpaces = [(x, y) for x in range(width) for y in range(height) if self.model.grid.is_cell_empty((x, y))]
                suitableSpaces = []
                if vacantSpaces:
                    for space in vacantSpaces:
                        vacantNeighbours = self.model.grid.get_neighbors(space, moore=True, include_center=False)
                        bVacant = sum(1 for neighbour in vacantNeighbours if neighbour.color == self.color)
                        nVacant = len(vacantNeighbours)
                        if nVacant > 0 and bVacant/nVacant < self.ba:
                            suitableSpaces.append(space)
                if suitableSpaces:
                    self.model.grid.move_agent(self, self.random.choice(suitableSpaces))
        if N > 0:
            self.b = B/N


class SegregationModel(Model):
    def __init__(self, width, height, N, pRed, baRed, baBlue, seed):
        super().__init__()
        self.random.seed(seed)
        self.grid = MultiGrid(width, height, True)
        self.pop = N
        self.schedule = RandomActivation(self)
        index = 0
        for i in range(int(self.pop*pRed)):
            discriminator = Discriminator(i, self, "red", baRed, seed+index)
            self.schedule.add(discriminator)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(discriminator, (x, y))
            index += 1
        for i in range(int(self.pop*(1-pRed))):
            discriminator = Discriminator(i+self.pop*pRed, self, "blue", baBlue, seed+index)
            self.schedule.add(discriminator)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(discriminator, (x, y))
            index += 1
        self.datacollector = DataCollector(
            model_reporters={
                "redAvgNeighbours": lambda m: sum([a.b for a in m.schedule.agents if a.color == "red"])/len([a for a in m.schedule.agents if a.color == "red"]),
                "blueAvgNeighbours": lambda m: sum([a.b for a in m.schedule.agents if a.color == "blue"])/len([a for a in m.schedule.agents if a.color == "blue"]),
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

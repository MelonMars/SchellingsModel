from model import SegregationModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.visualization.modules import ChartModule


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": agent.color,
                 "tooltip": f"{agent.ba}",
                 "r": 1}
    return portrayal


width, height, canvasWidth, canvasHeight = 50, 50, 500, 500
grid = CanvasGrid(agent_portrayal, width, height, canvasWidth, canvasHeight)

bChart = ChartModule(
    [{"Label": "redAvgNeighbours", "Color": "red"},
     {"Label": "blueAvgNeighbours", "Color": "blue"}]
)

server = ModularServer(
    SegregationModel,
    [grid, bChart],
    "Segregation Model",
    {
        "width": width,
        "height": height,
        "N": Slider("Agents", 10, 10, width*height, 50),
        "pRed": Slider("Amount of red agents (percent)", 0.5, 0, 1, 0.1),
        "baRed": Slider("Red Tolerance (0 is the most tolerance)", 0.5, 0, 1, 0.1),
        "baBlue": Slider("Blue Tolerance (0 is the most tolerance)", 0.5, 0, 1, 0.1),
        "seed": Slider("Random Seed", 42, 0, 600, 1)
    }
)


def resetServerParams(serv):
    grid_width = serv.parameter_values["width"]
    grid_height = serv.parameter_values["height"]
    grid.width = grid_width
    grid.height = grid_height
    grid.portrayal_method = agent_portrayal


server.reset_server_parameters = resetServerParams

if __name__ == "__main__":
    server.port = 8521
    server.launch()

from model import SegregationModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": agent.color,
                 "tooltip": f"{agent.ba}",
                 "r": 0.5}
    return portrayal


width, height, canvasWidth, canvasHeight = 50, 50, 500, 500
grid = CanvasGrid(agent_portrayal, width, height, canvasWidth, canvasHeight)

server = ModularServer(
    SegregationModel,
    [grid],
    "Segregation Model",
    {
        "width": width,
        "height": height,
        "N": Slider("Agents", 10, 10, width*height, 50),
        "pRed": Slider("Amount of red agents (percent)", 0.5, 0, 1, 0.1),
        "ba": Slider("BA", 0.5, 0, 1, 0.1)
    }
)


def resetServerParams(server):
    grid_width = server.parameter_values["width"]
    grid_height = server.parameter_values["height"]
    grid.width = grid_width
    grid.height = grid_height
    grid.portrayal_method = agent_portrayal


server.reset_server_parameters = resetServerParams

if __name__ == "__main__":
    server.port = 8521
    server.launch()
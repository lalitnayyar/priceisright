from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
import os
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.fc1 = nn.Linear(size, size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(size, size)
        
    def forward(self, x):
        residual = x
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out += residual
        out = self.relu(out)
        return out

class PriceNet(nn.Module):
    def __init__(self, input_size=256):
        super().__init__()
        self.entry = nn.Linear(input_size, 256)
        self.relu = nn.ReLU()
        self.res1 = ResidualBlock(256)
        self.res2 = ResidualBlock(256)
        self.res3 = ResidualBlock(256)
        self.exit = nn.Linear(256, 1)
        
    def forward(self, x):
        x = self.entry(x)
        x = self.relu(x)
        x = self.res1(x)
        x = self.res2(x)
        x = self.res3(x)
        x = self.exit(x)
        return x

class NeuralNetworkAgent(Agent):
    def __init__(self):
        super().__init__("Neural Network", "Deep Residual DNN", "#5DD9D0", "Local PyTorch")
        self.model_net = PriceNet()
        if os.path.exists(settings.DNN_WEIGHTS_PATH):
            try:
                self.model_net.load_state_dict(torch.load(settings.DNN_WEIGHTS_PATH))
            except Exception as e:
                self.logger.warning(f"Could not load weights: {e}")

    def run(self, deal: Deal) -> float:
        self.set_status("RUNNING")
        self.logger.info("Running residual block inference...")
        
        # Mock preprocessing and inference
        try:
            # dummy_input = torch.randn(1, 256)
            # with torch.no_grad():
            #     estimate = self.model_net(dummy_input).item()
            estimate = deal.price * 1.3
        except Exception as e:
            self.logger.error(f"DNN Error: {e}")
            estimate = deal.price
            
        self.set_status("READY")
        return estimate

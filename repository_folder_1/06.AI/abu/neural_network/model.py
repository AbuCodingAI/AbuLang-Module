"""Neural network model for chess position evaluation"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualBlock(nn.Module):
    """Residual block with two convolutional layers"""
    
    def __init__(self, num_filters: int):
        super().__init__()
        self.conv1 = nn.Conv2d(num_filters, num_filters, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_filters)
        self.conv2 = nn.Conv2d(num_filters, num_filters, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_filters)
    
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        out = F.relu(out)
        return out


class ChessNet(nn.Module):
    """Neural network for chess position evaluation"""
    
    def __init__(self, num_residual_blocks: int = 5, num_filters: int = 128):
        """
        Initialize ChessNet
        
        Args:
            num_residual_blocks: Number of residual blocks (default: 5)
            num_filters: Number of filters in convolutional layers (default: 128)
        """
        super().__init__()
        
        self.num_residual_blocks = num_residual_blocks
        self.num_filters = num_filters
        
        # Initial convolutional layer
        self.conv_input = nn.Conv2d(14, num_filters, kernel_size=3, padding=1)
        self.bn_input = nn.BatchNorm2d(num_filters)
        
        # Residual blocks
        self.residual_blocks = nn.ModuleList([
            ResidualBlock(num_filters) for _ in range(num_residual_blocks)
        ])
        
        # Policy head (move prediction)
        self.policy_conv = nn.Conv2d(num_filters, 32, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(32)
        self.policy_fc = nn.Linear(32 * 8 * 8, 4096)
        
        # Value head (position evaluation)
        self.value_conv = nn.Conv2d(num_filters, 32, kernel_size=1)
        self.value_bn = nn.BatchNorm2d(32)
        self.value_fc1 = nn.Linear(32 * 8 * 8, 256)
        self.value_fc2 = nn.Linear(256, 1)
    
    def forward(self, x):
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch_size, 14, 8, 8)
        
        Returns:
            Tuple of (policy_logits, value)
            - policy_logits: (batch_size, 4096) - move probabilities
            - value: (batch_size, 1) - position evaluation (-1 to +1)
        """
        # Initial convolution
        x = F.relu(self.bn_input(self.conv_input(x)))
        
        # Residual blocks
        for block in self.residual_blocks:
            x = block(x)
        
        # Policy head
        policy = F.relu(self.policy_bn(self.policy_conv(x)))
        policy = policy.reshape(policy.size(0), -1)
        policy_logits = self.policy_fc(policy)
        
        # Value head
        value = F.relu(self.value_bn(self.value_conv(x)))
        value = value.reshape(value.size(0), -1)
        value = F.relu(self.value_fc1(value))
        value = torch.tanh(self.value_fc2(value))
        
        return policy_logits, value

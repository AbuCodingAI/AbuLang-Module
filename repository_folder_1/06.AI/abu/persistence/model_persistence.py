"""Model persistence for saving and loading neural network models"""

import torch
import os
import json
from typing import Tuple, Dict, Any
from abu.neural_network import ChessNet


class ModelPersistence:
    """Handles model save/load operations"""
    
    @staticmethod
    def save_model(model: ChessNet, filepath: str, metadata: Dict[str, Any] = None):
        """
        Save model weights and metadata to disk
        
        Args:
            model: ChessNet model to save
            filepath: Path to save the model (without extension)
            metadata: Optional metadata dictionary
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        # Prepare save data
        save_data = {
            'model_state_dict': model.state_dict(),
            'num_residual_blocks': model.num_residual_blocks,
            'num_filters': model.num_filters,
            'metadata': metadata or {}
        }
        
        # Save model
        torch.save(save_data, f"{filepath}.pth")
        
        # Save metadata as JSON for easy inspection
        if metadata:
            with open(f"{filepath}_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
    
    @staticmethod
    def load_model(filepath: str, device: str = 'cpu') -> Tuple[ChessNet, Dict[str, Any]]:
        """
        Load model weights and metadata from disk
        
        Args:
            filepath: Path to the saved model (without extension)
            device: Device to load model to ('cpu' or 'cuda')
        
        Returns:
            Tuple of (model, metadata)
        """
        # Check if file exists
        model_path = f"{filepath}.pth"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load saved data
        save_data = torch.load(model_path, map_location=device)
        
        # Create model with saved architecture
        model = ChessNet(
            num_residual_blocks=save_data['num_residual_blocks'],
            num_filters=save_data['num_filters']
        )
        
        # Load weights
        model.load_state_dict(save_data['model_state_dict'])
        model.to(device)
        
        # Get metadata
        metadata = save_data.get('metadata', {})
        
        return model, metadata
    
    @staticmethod
    def model_exists(filepath: str) -> bool:
        """
        Check if a model file exists
        
        Args:
            filepath: Path to check (without extension)
        
        Returns:
            True if model exists, False otherwise
        """
        return os.path.exists(f"{filepath}.pth")

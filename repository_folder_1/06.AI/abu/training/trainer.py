"""Trainer for neural network model with regularization to prevent overfitting"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import List, Tuple
from tqdm import tqdm

from abu.neural_network import ChessNet
from abu.training.collector import TrainingExample, GameRecord


class Trainer:
    """Trains the neural network with proper regularization"""
    
    def __init__(self, model: ChessNet, learning_rate: float = 0.001, 
                 weight_decay: float = 1e-4, device: str = 'cpu'):
        """
        Initialize trainer
        
        Args:
            model: ChessNet model to train
            learning_rate: Learning rate for optimizer
            weight_decay: L2 regularization strength (prevents overfitting)
            device: Device to train on ('cpu' or 'cuda')
        """
        self.model = model.to(device)
        self.device = device
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        
        # Optimizer with weight decay for regularization
        self.optimizer = optim.Adam(
            model.parameters(), 
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler for better convergence
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=5
        )
        
        # Loss functions
        self.policy_loss_fn = nn.CrossEntropyLoss()
        self.value_loss_fn = nn.MSELoss()
        
        # Training history
        self.train_losses = []
        self.val_losses = []
    
    def train_on_games(self, training_data: List[TrainingExample], 
                      epochs: int = 10, batch_size: int = 32,
                      validation_split: float = 0.1,
                      dropout_rate: float = 0.0) -> dict:
        """
        Train on game data with validation split to monitor overfitting
        
        Args:
            training_data: List of TrainingExample instances
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Fraction of data to use for validation
            dropout_rate: Dropout rate during training (0.0 = no dropout)
        
        Returns:
            Dictionary with training history
        """
        if len(training_data) == 0:
            raise ValueError("No training data provided")
        
        # Split into train and validation
        np.random.shuffle(training_data)
        val_size = int(len(training_data) * validation_split)
        val_data = training_data[:val_size]
        train_data = training_data[val_size:]
        
        print(f"Training on {len(train_data)} examples, validating on {val_size} examples")
        
        for epoch in range(epochs):
            # Training phase
            self.model.train()
            train_loss = self._train_epoch(train_data, batch_size)
            self.train_losses.append(train_loss)
            
            # Validation phase
            self.model.eval()
            val_loss = self._validate(val_data, batch_size)
            self.val_losses.append(val_loss)
            
            # Update learning rate based on validation loss
            self.scheduler.step(val_loss)
            
            print(f"Epoch {epoch+1}/{epochs} - "
                  f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            
            # Early stopping if overfitting detected
            if len(self.val_losses) > 5:
                recent_val = self.val_losses[-5:]
                if all(recent_val[i] >= recent_val[i-1] for i in range(1, len(recent_val))):
                    print("Early stopping: validation loss increasing")
                    break
        
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'final_train_loss': self.train_losses[-1],
            'final_val_loss': self.val_losses[-1]
        }
    
    def _train_epoch(self, train_data: List[TrainingExample], batch_size: int) -> float:
        """Train for one epoch"""
        total_loss = 0.0
        num_batches = 0
        
        # Shuffle training data
        np.random.shuffle(train_data)
        
        for i in range(0, len(train_data), batch_size):
            batch = train_data[i:i+batch_size]
            loss = self.train_step(batch)
            total_loss += loss
            num_batches += 1
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def _validate(self, val_data: List[TrainingExample], batch_size: int) -> float:
        """Validate on validation set"""
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for i in range(0, len(val_data), batch_size):
                batch = val_data[i:i+batch_size]
                loss = self._compute_loss(batch)
                total_loss += loss
                num_batches += 1
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def train_step(self, batch: List[TrainingExample]) -> float:
        """
        Single training step
        
        Args:
            batch: List of TrainingExample instances
        
        Returns:
            Loss value
        """
        self.optimizer.zero_grad()
        loss = self._compute_loss(batch)
        
        # Backward pass
        loss_tensor = torch.tensor(loss, requires_grad=True)
        loss_tensor.backward()
        
        # Gradient clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        return loss
    
    def _compute_loss(self, batch: List[TrainingExample]) -> float:
        """Compute loss for a batch"""
        # Prepare batch tensors
        board_tensors = []
        policy_targets = []
        value_targets = []
        
        for example in batch:
            board_tensors.append(example.board_tensor)
            policy_targets.append(example.policy_target)
            value_targets.append(example.value_target)
        
        # Convert to torch tensors
        boards = torch.FloatTensor(np.array(board_tensors)).to(self.device)
        boards = boards.permute(0, 3, 1, 2)  # (batch, 14, 8, 8)
        
        policies = torch.FloatTensor(np.array(policy_targets)).to(self.device)
        values = torch.FloatTensor(np.array(value_targets)).unsqueeze(1).to(self.device)
        
        # Forward pass
        policy_logits, value_pred = self.model(boards)
        
        # Compute losses
        # Policy loss: cross-entropy between predicted and target distributions
        policy_loss = self.policy_loss_fn(policy_logits, policies.argmax(dim=1))
        
        # Value loss: MSE between predicted and target values
        value_loss = self.value_loss_fn(value_pred, values)
        
        # Combined loss
        total_loss = policy_loss + value_loss
        
        return total_loss.item()
    
    def save_checkpoint(self, filepath: str, epoch: int, metadata: dict = None):
        """Save training checkpoint"""
        from abu.persistence import ModelPersistence
        
        checkpoint_metadata = {
            'epoch': epoch,
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'learning_rate': self.learning_rate,
            'weight_decay': self.weight_decay
        }
        
        if metadata:
            checkpoint_metadata.update(metadata)
        
        ModelPersistence.save_model(self.model, filepath, checkpoint_metadata)

"""
Autoencoder Model for Behavioral Anomaly Detection

This module implements a PyTorch-based autoencoder neural network 
designed to learn normal behavioral patterns and detect anomalies
through reconstruction error.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BehavioralAutoencoder(nn.Module):
    """
    Deep Autoencoder for learning baseline behavioral patterns.
    
    Architecture:
        - Input Layer: 9 behavioral features
        - Encoder: 9 -> 6 -> 3 (bottleneck)
        - Decoder: 3 -> 6 -> 9 (reconstruction)
    
    The bottleneck layer compresses behavioral patterns into a 
    3-dimensional latent space, forcing the model to learn 
    meaningful representations of normal behavior.
    """
    
    def __init__(self, input_dim: int = 9, hidden_dim: int = 6, latent_dim: int = 3):
        """
        Initialize the autoencoder architecture.
        
        Args:
            input_dim: Number of input features (default: 9)
            hidden_dim: Size of hidden layer (default: 6)
            latent_dim: Size of latent/bottleneck layer (default: 3)
        """
        super(BehavioralAutoencoder, self).__init__()
        
        # Encoder layers
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, latent_dim),
            nn.ReLU()
        )
        
        # Decoder layers
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()  # Output in [0, 1] range for normalized features
        )
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through encoder and decoder.
        
        Args:
            x: Input tensor of behavioral features
            
        Returns:
            Reconstructed behavioral features
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode input to latent representation.
        
        Args:
            x: Input tensor of behavioral features
            
        Returns:
            Latent representation
        """
        return self.encoder(x)
    
    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """
        Decode latent representation to output.
        
        Args:
            z: Latent representation
            
        Returns:
            Reconstructed behavioral features
        """
        return self.decoder(z)


class AutoencoderTrainer:
    """
    Trainer class for the Behavioral Autoencoder.
    
    Handles training loop, validation, and model persistence.
    """
    
    def __init__(
        self, 
        model: BehavioralAutoencoder,
        learning_rate: float = 0.001,
        device: str = 'cpu'
    ):
        """
        Initialize the trainer.
        
        Args:
            model: Autoencoder model instance
            learning_rate: Learning rate for optimization
            device: Device for training ('cpu' or 'cuda')
        """
        self.model = model.to(device)
        self.device = device
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.training_losses = []
        
    def train_epoch(
        self, 
        data: np.ndarray
    ) -> float:
        """
        Train for one epoch.
        
        Args:
            data: Training data (numpy array)
            
        Returns:
            Average loss for the epoch
        """
        self.model.train()
        
        # Convert to tensor
        x = torch.FloatTensor(data).to(self.device)
        
        # Forward pass
        self.optimizer.zero_grad()
        reconstruction = self.model(x)
        loss = self.criterion(reconstruction, x)
        
        # Backward pass
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def train(
        self, 
        training_data: np.ndarray,
        epochs: int = 50,
        batch_size: int = 32,
        verbose: bool = True
    ) -> list:
        """
        Train the autoencoder on baseline behavioral data.
        
        Args:
            training_data: Baseline behavioral data (N samples x 9 features)
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Whether to print training progress
            
        Returns:
            List of training losses per epoch
        """
        n_samples = training_data.shape[0]
        
        for epoch in range(epochs):
            epoch_losses = []
            
            # Mini-batch training
            for i in range(0, n_samples, batch_size):
                batch = training_data[i:i+batch_size]
                loss = self.train_epoch(batch)
                epoch_losses.append(loss)
            
            avg_loss = np.mean(epoch_losses)
            self.training_losses.append(avg_loss)
            
            if verbose and (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")
        
        return self.training_losses
    
    def compute_reconstruction_error(
        self, 
        data: np.ndarray
    ) -> np.ndarray:
        """
        Compute reconstruction error for input data.
        
        Args:
            data: Input behavioral data
            
        Returns:
            Reconstruction errors (MSE per sample)
        """
        self.model.eval()
        
        with torch.no_grad():
            x = torch.FloatTensor(data).to(self.device)
            reconstruction = self.model(x)
            
            # Compute MSE per sample
            errors = torch.mean((x - reconstruction) ** 2, dim=1)
            
        return errors.cpu().numpy()
    
    def save_model(self, path: str):
        """
        Save model state to disk.
        
        Args:
            path: File path to save the model
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'training_losses': self.training_losses
        }, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """
        Load model state from disk.
        
        Args:
            path: File path to load the model from
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.training_losses = checkpoint.get('training_losses', [])
        logger.info(f"Model loaded from {path}")


def create_pretrained_model(
    baseline_data: Optional[np.ndarray] = None,
    input_dim: int = 9
) -> Tuple[BehavioralAutoencoder, Optional[AutoencoderTrainer]]:
    """
    Factory function to create and optionally pre-train an autoencoder.
    
    Args:
        baseline_data: Optional baseline data for pre-training
        input_dim: Dimension of input features
        
    Returns:
        Tuple of (model, trainer). Trainer is None if no baseline data provided.
    """
    model = BehavioralAutoencoder(input_dim=input_dim)
    
    if baseline_data is not None:
        trainer = AutoencoderTrainer(model)
        trainer.train(baseline_data, epochs=50, verbose=False)
        return model, trainer
    
    return model, None

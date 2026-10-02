# -*- coding:utf-8 -*-
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


class PolicyNet(nn.Module):
    """Actor network for PPO"""
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.softmax(self.fc3(x), dim=-1)


class ValueNet(nn.Module):
    """Critic network for PPO"""
    def __init__(self, state_dim, hidden_dim):
        super(ValueNet, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


class TrajectoryBuffer:
    """Buffer for storing trajectories for PPO"""
    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []
        self.log_probs = []

    def add(self, state, action, reward, next_state, done, log_prob):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_states.append(next_state)
        self.dones.append(done)
        self.log_probs.append(log_prob)

    def get(self):
        return (self.states, self.actions, self.rewards, 
                self.next_states, self.dones, self.log_probs)

    def clear(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []
        self.log_probs = []

    def size(self):
        return len(self.states)


class PPO:
    """PPO Agent"""
    def __init__(self, state_dim, hidden_dim, action_dim, actor_lr, critic_lr, 
                 gamma, lmbda, epochs, eps_clip, device):
        self.actor = PolicyNet(state_dim, hidden_dim, action_dim).to(device)
        self.critic = ValueNet(state_dim, hidden_dim).to(device)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=critic_lr)
        
        self.gamma = gamma
        self.lmbda = lmbda  # GAE lambda
        self.epochs = epochs  # PPO update epochs
        self.eps_clip = eps_clip  # Clipping parameter
        self.device = device

    def take_action(self, state, k_paths_range=None):
        """Sample action from policy"""
        state = torch.tensor(state, dtype=torch.float).to(self.device)
        probs = self.actor(state)
        
        # Mask invalid actions if k_paths_range is provided
        if k_paths_range is not None:
            mask = torch.zeros_like(probs)
            mask[k_paths_range[0]:k_paths_range[1]] = 1
            probs = probs * mask
            probs = probs / probs.sum()  # Renormalize
        
        action_dist = Categorical(probs)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)
        
        return action.item(), log_prob.item()

    def compute_advantage(self, gamma, lmbda, td_delta):
        """Compute GAE advantage"""
        td_delta = td_delta.detach().numpy()
        advantage_list = []
        advantage = 0.0
        for delta in td_delta[::-1]:
            advantage = gamma * lmbda * advantage + delta
            advantage_list.append(advantage)
        advantage_list.reverse()
        return torch.tensor(advantage_list, dtype=torch.float)

    def update(self, trajectory_buffer):
        """Update policy and value network using PPO"""
        states, actions, rewards, next_states, dones, old_log_probs = trajectory_buffer.get()
        
        # Convert to tensors
        states = torch.tensor(np.array(states), dtype=torch.float).to(self.device)
        actions = torch.tensor(actions, dtype=torch.int64).view(-1, 1).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float).view(-1, 1).to(self.device)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float).view(-1, 1).to(self.device)
        old_log_probs = torch.tensor(old_log_probs, dtype=torch.float).view(-1, 1).to(self.device)
        
        # Compute TD target and advantage
        td_target = rewards + self.gamma * self.critic(next_states) * (1 - dones)
        td_delta = td_target - self.critic(states)
        advantage = self.compute_advantage(self.gamma, self.lmbda, td_delta.cpu()).to(self.device)
        
        # Normalize advantage
        advantage = (advantage - advantage.mean()) / (advantage.std() + 1e-8)
        
        # PPO update
        for _ in range(self.epochs):
            # Compute current log probs
            probs = self.actor(states)
            action_dists = Categorical(probs)
            current_log_probs = action_dists.log_prob(actions.squeeze()).view(-1, 1)
            
            # Compute ratio
            ratio = torch.exp(current_log_probs - old_log_probs)
            
            # Compute surrogate loss
            surr1 = ratio * advantage
            surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * advantage
            actor_loss = -torch.mean(torch.min(surr1, surr2))
            
            # Compute value loss
            critic_loss = torch.mean(F.mse_loss(self.critic(states), td_target.detach()))
            
            # Update actor
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.actor.parameters(), 0.5)
            self.actor_optimizer.step()
            
            # Update critic
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.critic.parameters(), 0.5)
            self.critic_optimizer.step()

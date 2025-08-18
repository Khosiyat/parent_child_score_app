import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

interface Reward {
  id: number;
  name: string;
  cost: number;
  description: string;
}

interface ScoreTransaction {
  id: number;
  points: number;
  description: string;
  created_at: string;
}

const ChildDashboard: React.FC = () => {
  const [scoreBalance, setScoreBalance] = useState<number>(0);
  const [transactions, setTransactions] = useState<ScoreTransaction[]>([]);
  const [rewards, setRewards] = useState<Reward[]>([]);
  const [selectedRewardId, setSelectedRewardId] = useState<number | null>(null);

  useEffect(() => {
    fetchScore();
    fetchTransactions();
    fetchRewards();
  }, []);

  const fetchScore = () => {
    axiosInstance.get('children/')
      .then(res => {
        if (res.data.length > 0) {
          setScoreBalance(res.data[0].score_balance);
        }
      })
      .catch(() => alert('Failed to fetch score'));
  };

  const fetchTransactions = () => {
    axiosInstance.get('score-transactions/')
      .then(res => setTransactions(res.data))
      .catch(() => alert('Failed to fetch transactions'));
  };

  const fetchRewards = () => {
    axiosInstance.get('rewards/')
      .then(res => setRewards(res.data))
      .catch(() => alert('Failed to fetch rewards'));
  };

  const handleRequestReward = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRewardId) return alert('Select a reward to request');

    try {
      await axiosInstance.post('reward-requests/create/', { reward: selectedRewardId });
      alert('Reward requested! Waiting for parent approval.');
    } catch (e: any) {
      alert(e.response?.data.detail || 'Failed to request reward');
    }
  };

  const handleRedeemReward = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRewardId) return alert('Select a reward to redeem');

    try {
      await axiosInstance.post('rewards/redeem/', { reward_id: selectedRewardId });
      alert('Reward redeemed!');
      fetchScore();
      fetchTransactions();
    } catch (e: any) {
      alert(e.response?.data

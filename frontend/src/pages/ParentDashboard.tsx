import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

interface Child {
  id: number;
  user: { username: string };
  score_balance: number;
}

interface Reward {
  id: number;
  name: string;
  cost: number;
  description: string;
}

interface RewardRequest {
  id: number;
  child_name: string;
  reward_name: string;
  requested_at: string;
}

const ParentDashboard: React.FC = () => {
  const [children, setChildren] = useState<Child[]>([]);
  const [selectedChildId, setSelectedChildId] = useState<number | null>(null);
  const [points, setPoints] = useState<number>(0);
  const [description, setDescription] = useState('');
  const [rewards, setRewards] = useState<Reward[]>([]);
  const [rewardRequests, setRewardRequests] = useState<RewardRequest[]>([]);

  useEffect(() => {
    fetchChildren();
    fetchRewards();
    fetchRewardRequests();
  }, []);

  const fetchChildren = () => {
    axiosInstance.get('children/')
      .then(res => setChildren(res.data))
      .catch(() => alert('Failed to fetch children'));
  };

  const fetchRewards = () => {
    axiosInstance.get('rewards/')
      .then(res => setRewards(res.data))
      .catch(() => alert('Failed to fetch rewards'));
  };

  const fetchRewardRequests = () => {
    axiosInstance.get('reward-requests/')
      .then(res => setRewardRequests(res.data))
      .catch(() => alert('Failed to fetch reward requests'));
  };

  const handleAddSubtractPoints = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChildId || !description) return alert('Please select child and add description');

    try {
      await axiosInstance.post('score-transactions/', {
        child: selectedChildId,
        points,
        description,
      });
      alert('Score updated');
      fetchChildren();
    } catch {
      alert('Failed to update score');
    }
  };

  const approveRequest = async (id: number) => {
    try {
      await axiosInstance.post(`reward-requests/${id}/approve/`);
      alert('Request approved');
      fetchChildren();
      fetchRewardRequests();
    } catch (e: any) {
      alert(e.response?.data.detail || 'Failed to approve request');
    }
  };

  return (
    <div>
      <h2>Parent Dashboard</h2>

      <h3>Your Children</h3>
      <ul>
        {children.map(child => (
          <li key={child.id}>
            {child.user.username} - Score: {child.score_balance}
          </li>
        ))}
      </ul>

      <h3>Add/Subtract Score</h3>
      <form onSubmit={handleAddSubtractPoints}>
        <select value={selectedChildId ?? ''} onChange={e => setSelectedChildId(Number(e.target.value))} required>
          <option value="" disabled>Select Child</option>
          {children.map(child => (
            <option key={child.id} value={child.id}>{child.user.username}</option>
          ))}
        </select>
        <input
          type="number"
          value={points}
          onChange={e => setPoints(Number(e.target.value))}
          placeholder="Points (+/-)"
          required
        />
        <input
          type="text"
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Description"
          required
        />
        <button type="submit">Submit</button>
      </form>

      <h3>Pending Reward Requests</h3>
      <ul>
        {rewardRequests.map(req => (
          <li key={req.id}>
            {req.child_name} requested {req.reward_name} at {new Date(req.requested_at).toLocaleString()}
            <button onClick={() => approveRequest(req.id)}>Approve</button>
          </li>
        ))}
      </ul>

      <h3>Reward Catalog</h3>
      <ul>
        {rewards.map(r => (
          <li key={r.id}>{r.name} - Cost: {r.cost} points - {r.description}</li>
        ))}
      </ul>
    </div>
  );
};

export default ParentDashboard;

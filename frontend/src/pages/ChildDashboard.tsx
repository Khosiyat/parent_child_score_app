import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

interface ScoreTransaction {
  id: number;
  points: number;
  description: string;
  created_at: string;
}

const ChildDashboard: React.FC = () => {
  const [scoreBalance, setScoreBalance] = useState<number>(0);
  const [transactions, setTransactions] = useState<ScoreTransaction[]>([]);

  useEffect(() => {
    axiosInstance.get('children/')
      .then(res => {
        if (res.data.length > 0) {
          setScoreBalance(res.data[0].score_balance);
        }
      })
      .catch(() => alert('Failed to fetch score'));

    axiosInstance.get('score-transactions/')
      .then(res => setTransactions(res.data))
      .catch(() => alert('Failed to fetch transactions'));
  }, []);

  return (
    <div>
      <h2>Child Dashboard</h2>
      <p>Score Balance: {scoreBalance}</p>

      <h3>Transactions</h3>
      <ul>
        {transactions.map(tx => (
          <li key={tx.id}>
            {tx.description}: {tx.points > 0 ? '+' : ''}{tx.points} points ({new Date(tx.created_at).toLocaleString()})
          </li>
        ))}
      </ul>
      {/* Add reward redemption UI here */}
    </div>
  );
};

export default ChildDashboard;

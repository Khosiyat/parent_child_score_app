// import React, { useEffect, useState } from 'react';
// import axiosInstance from '../api/axiosInstance';

// interface ScoreTransaction {
//   id: number;
//   points: number;
//   description: string;
//   created_at: string;
// }

// const ChildDashboard: React.FC = () => {
//   const [scoreBalance, setScoreBalance] = useState<number>(0);
//   const [transactions, setTransactions] = useState<ScoreTransaction[]>([]);

//   useEffect(() => {
//     axiosInstance.get('children/')
//       .then(res => {
//         if (res.data.length > 0) {
//           setScoreBalance(res.data[0].score_balance);
//         }
//       })
//       .catch(() => alert('Failed to fetch score'));

//     axiosInstance.get('score-transactions/')
//       .then(res => setTransactions(res.data))
//       .catch(() => alert('Failed to fetch transactions'));
//   }, []);

//   return (
//     <div>
//       <h2>Child Dashboard</h2>
//       <p>Score Balance: {scoreBalance}</p>

//       <h3>Transactions</h3>
//       <ul>
//         {transactions.map(tx => (
//           <li key={tx.id}>
//             {tx.description}: {tx.points > 0 ? '+' : ''}{tx.points} points ({new Date(tx.created_at).toLocaleString()})
//           </li>
//         ))}
//       </ul>
//       {/* Add reward redemption UI here */}
//     </div>
//   );
// };

// export default ChildDashboard;

import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

interface ScoreTransaction {
  id: number;
  points: number;
  description: string;
  created_at: string;
}

interface Reward {
  id: number;
  name: string;
  cost: number;
  description: string;
}

const ChildDashboard: React.FC = () => {
  const [scoreBalance, setScoreBalance] = useState<number>(0);
  const [transactions, setTransactions] = useState<ScoreTransaction[]>([]);
  const [rewards, setRewards] = useState<Reward[]>([]);
  const [selectedRewardId, setSelectedRewardId] = useState<number | null>(null);

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

    axiosInstance.get('rewards/')
      .then(res => setRewards(res.data))
      .catch(() => alert('Failed to fetch rewards'));
  }, []);

  const handleRedeemReward = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRewardId) return alert('Select a reward');

    try {
      await axiosInstance.post('rewards/redeem/', { reward_id: selectedRewardId });
      alert('Reward redeemed!');
      // Refresh score balance and transactions
      const childrenRes = await axiosInstance.get('children/');
      if (childrenRes.data.length > 0) setScoreBalance(childrenRes.data[0].score_balance);

      const txRes = await axiosInstance.get('score-transactions/');
      setTransactions(txRes.data);
    } catch (error: any) {
      alert(error.response?.data.detail || 'Failed to redeem reward');
    }
  };

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

      <h3>Redeem Reward</h3>
      <form onSubmit={handleRedeemReward}>
        <select
          value={selectedRewardId ??

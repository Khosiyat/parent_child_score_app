// import React, { useEffect, useState } from 'react';
// import axiosInstance from '../api/axiosInstance';

// interface Child {
//   id: number;
//   user: {
//     username: string;
//   };
//   score_balance: number;
// }

// const ParentDashboard: React.FC = () => {
//   const [children, setChildren] = useState<Child[]>([]);

//   useEffect(() => {
//     axiosInstance.get('children/')
//       .then(res => setChildren(res.data))
//       .catch(() => alert('Failed to fetch children'));
//   }, []);

//   return (
//     <div>
//       <h2>Parent Dashboard</h2>
//       <h3>Your Children</h3>
//       <ul>
//         {children.map(child => (
//           <li key={child.id}>
//             {child.user.username} - Score: {child.score_balance}
//           </li>
//         ))}
//       </ul>
//       {/* You can add forms here for adding/subtracting points, redeeming rewards */}
//     </div>
//   );
// };

// export default ParentDashboard;


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

const ParentDashboard: React.FC = () => {
  const [children, setChildren] = useState<Child[]>([]);
  const [selectedChildId, setSelectedChildId] = useState<number | null>(null);
  const [points, setPoints] = useState<number>(0);
  const [description, setDescription] = useState('');
  const [rewards, setRewards] = useState<Reward[]>([]);
  const [redeemPoints, setRedeemPoints] = useState<number>(0);
  const [redeemDescription, setRedeemDescription] = useState('');
  const [selectedRewardId, setSelectedRewardId] = useState<number | null>(null);

  useEffect(() => {
    axiosInstance.get('children/')
      .then(res => setChildren(res.data))
      .catch(() => alert('Failed to fetch children'));

    axiosInstance.get('rewards/')
      .then(res => setRewards(res.data))
      .catch(() => alert('Failed to fetch rewards'));
  }, []);

  const handleAddSubtractPoints = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChildId) return alert('Select a child');
    if (!description) return alert('Enter a description');

    try {
      await axiosInstance.post('score-transactions/', {
        child: selectedChildId,
        points,
        description,
      });
      alert('Score updated');
      // Refresh children scores
      const res = await axiosInstance.get('children/');
      setChildren(res.data);
    } catch {
      alert('Failed to update score');
    }
  };

  const handleRedeemReward = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChildId) return alert('Select a child');
    if (!selectedRewardId) return alert('Select a reward');

    // Note: Parents can redeem rewards on behalf of child if you want,
    // or skip this form in parent and leave it for child only.

    alert('Reward redemption via parent not implemented yet.');
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

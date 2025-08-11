import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

interface Child {
  id: number;
  user: {
    username: string;
  };
  score_balance: number;
}

const ParentDashboard: React.FC = () => {
  const [children, setChildren] = useState<Child[]>([]);

  useEffect(() => {
    axiosInstance.get('children/')
      .then(res => setChildren(res.data))
      .catch(() => alert('Failed to fetch children'));
  }, []);

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
      {/* You can add forms here for adding/subtracting points, redeeming rewards */}
    </div>
  );
};

export default ParentDashboard;

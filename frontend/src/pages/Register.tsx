import React, { useState } from 'react';
import axiosInstance from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'parent' | 'child'>('parent');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axiosInstance.post('api/register/', { username, password, role });
      alert('Registration successful, please login.');
      navigate('/login');
    } catch (error) {
      alert('Registration failed!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      <select value={role} onChange={e => setRole(e.target.value as 'parent' | 'child')}>
        <option value="parent">Parent</option>
        <option value="child">Child</option>
      </select>
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;

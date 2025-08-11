import React, { useState, useContext } from 'react';
import axiosInstance from '../api/axiosInstance';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext)!;
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('api/token/', { username, password });
      login(response.data.access, response.data.refresh);

      // Redirect based on role
      const role = JSON.parse(atob(response.data.access.split('.')[1])).role;
      if (role === 'parent') navigate('/parent-dashboard');
      else navigate('/child-dashboard');
    } catch (error) {
      alert('Login failed!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;

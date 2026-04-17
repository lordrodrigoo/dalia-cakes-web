import { useNavigate } from 'react-router-dom';
import Login from '../components/Login';

export default function LoginPage() {
  const navigate = useNavigate();
  const handleLogin = () => {
    navigate('/');
  };
  return <Login onLogin={handleLogin} />;
}

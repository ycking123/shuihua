import React, { useState } from 'react';
import { User, Lock, ArrowRight, Loader2 } from 'lucide-react';

interface LoginViewProps {
  onLoginSuccess: (token: string, username: string) => void;
}

const LoginView: React.FC<LoginViewProps> = ({ onLoginSuccess }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const endpoint = isRegistering ? '/api/auth/register' : '/api/auth/login';
    const payload = { username, password };

    try {
      // API is proxied via Vite config (target: http://47.121.138.58:8000)
      // Or use VITE_API_URL if defined
      // const baseUrl = import.meta.env.VITE_API_URL || ''; 
      
      // Dynamic backend URL strategy
      const getBackendUrl = () => {
          // Always use relative path (Vite proxy) in development mode (npm run dev)
          // This works for both localhost and server (47.121.138.58:3000)
          if (import.meta.env.DEV) {
               return ''; 
          }
          // In production build, default to port 8000 on same host
          return import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;
      };
      
      const baseUrl = getBackendUrl();
      const fetchUrl = `${baseUrl}${endpoint}`;
      console.log(`Attempting login to: ${fetchUrl}`);

      const response = await fetch(fetchUrl, {
        method: 'POST',
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const text = await response.text();
      let data;
      try {
        data = text ? JSON.parse(text) : {};
      } catch (e) {
        console.error('Failed to parse JSON:', text);
        throw new Error(`Server error (${response.status}): ${text.substring(0, 100) || 'Empty response'}`);
      }

      if (!response.ok) {
        throw new Error(data.detail || `Error ${response.status}: ${text}`);
      }

      // Login/Register success
      onLoginSuccess(data.access_token, data.username);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Connection error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-900 transition-colors duration-500 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute -top-[30%] -right-[10%] w-[70%] h-[70%] rounded-full bg-blue-400/20 blur-3xl" />
        <div className="absolute -bottom-[20%] -left-[10%] w-[60%] h-[60%] rounded-full bg-indigo-500/20 blur-3xl" />
      </div>

      <div className="z-10 w-full max-w-md p-8 bg-white/80 dark:bg-black/40 backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-2">
            水华精灵
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm tracking-widest uppercase">
            Strategic Insight Hub V4
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              用户名
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User size={18} className="text-slate-400" />
              </div>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                placeholder="请输入用户名"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              密码
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock size={18} className="text-slate-400" />
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                placeholder="请输入密码"
                required
              />
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex items-center justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
          >
            {isLoading ? (
              <Loader2 className="animate-spin mr-2" size={18} />
            ) : (
              <>
                {isRegistering ? '注册并登录' : '登 录'}
                <ArrowRight className="ml-2" size={18} />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-slate-500 dark:text-slate-400">
            {isRegistering ? '已有账号？' : '还没有账号？'}
            <button
              onClick={() => setIsRegistering(!isRegistering)}
              className="ml-1 font-medium text-blue-600 hover:text-blue-500 focus:outline-none transition-colors"
            >
              {isRegistering ? '直接登录' : '立即注册'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginView;



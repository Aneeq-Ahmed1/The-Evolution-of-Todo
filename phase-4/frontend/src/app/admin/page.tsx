"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '../../lib/api';

interface User {
  id: number;
  email: string;
  created_at: string;
  is_active: boolean;
}

export default function AdminPanel() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [adminEmail, setAdminEmail] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [resetUserId, setResetUserId] = useState<number | null>(null);
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');

    try {
      const response = await apiClient.admin.login({
        email: adminEmail,
        password: adminPassword,
      });

      localStorage.setItem('admin_token', response.data.access_token);
      setIsLoggedIn(true);
      loadUsers();
    } catch (err: any) {
      setLoginError(err?.message || 'Invalid admin credentials');
      console.error(err);
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    try {
      const adminToken = localStorage.getItem('admin_token');
      if (!adminToken) {
        setIsLoggedIn(false);
        return;
      }

      const response = await apiClient.admin.getUsers(adminToken);
      setUsers(response.data);
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (userId: number) => {
    if (!newPassword || newPassword.length < 6) {
      setMessage('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    try {
      const adminToken = localStorage.getItem('admin_token');
      if (!adminToken) {
        setIsLoggedIn(false);
        return;
      }

      const response = await apiClient.admin.resetPassword(userId, newPassword, adminToken);
      setMessage(`✓ ${response.data.message}`);
      setResetUserId(null);
      setNewPassword('');
      setTimeout(() => setMessage(''), 5000);
    } catch (err: any) {
      setMessage(`✕ ${err?.message || 'Error resetting password'}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number, userEmail: string) => {
    if (!confirm(`Are you sure you want to delete user ${userEmail}?\n\nThis will PERMANENTLY delete all their tasks as well.`)) {
      return;
    }

    setLoading(true);
    try {
      const adminToken = localStorage.getItem('admin_token');
      if (!adminToken) {
        setIsLoggedIn(false);
        return;
      }

      await apiClient.admin.deleteUser(userId, adminToken);
      setMessage(`✓ User ${userEmail} and all associated tasks deleted successfully`);
      loadUsers();
      setTimeout(() => setMessage(''), 5000);
    } catch (err: any) {
      setMessage(`✕ ${err?.message || 'Error deleting user'}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setIsLoggedIn(false);
    setUsers([]);
  };

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      setIsLoggedIn(true);
      loadUsers();
    }
  }, []);

  // Login Form
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center py-12 px-4" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="max-w-md w-full">
          <Link href="/" className="inline-flex items-center text-sm mb-4 hover:underline" style={{ color: '#6e7780' }}>
            ← Back to Home
          </Link>

          <div className="bg-white rounded p-6" style={{ border: '1px solid #e0e4e9' }}>
            <div className="mb-6">
              <h2 className="text-2xl font-semibold mb-1" style={{ color: '#232a31' }}>
                Admin Login
              </h2>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Sign in to access admin panel
              </p>
            </div>

            <form onSubmit={handleAdminLogin} className="space-y-4">
              {loginError && (
                <div className="p-3 rounded" style={{ backgroundColor: '#fee', border: '1px solid #fcc' }}>
                  <p className="text-sm" style={{ color: '#c00' }}>{loginError}</p>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
                  Admin Email
                </label>
                <input
                  type="email"
                  required
                  value={adminEmail}
                  onChange={(e) => setAdminEmail(e.target.value)}
                  className="w-full px-3 py-2.5 rounded text-sm"
                  style={{ border: '1px solid #e0e4e9', backgroundColor: '#ffffff', color: '#232a31' }}
                  placeholder="admin@taskflow.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
                  Admin Password
                </label>
                <input
                  type="password"
                  required
                  value={adminPassword}
                  onChange={(e) => setAdminPassword(e.target.value)}
                  className="w-full px-3 py-2.5 rounded text-sm"
                  style={{ border: '1px solid #e0e4e9', backgroundColor: '#ffffff', color: '#232a31' }}
                  placeholder="Enter admin password"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded font-medium text-sm"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
              >
                Sign In as Admin
              </button>
            </form>

            <div className="mt-4 p-3 rounded" style={{ backgroundColor: '#f0f3f5' }}>
              <p className="text-xs" style={{ color: '#6e7780' }}>
                <strong>Default Admin Credentials:</strong><br />
                Email: admin@taskflow.com<br />
                Password: Admin@12345
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Admin Panel
  return (
    <div className="min-h-screen font-sans" style={{ backgroundColor: '#f5f8fa' }}>
      {/* Navigation */}
      <nav className="bg-white border-b sticky top-0 z-10" style={{ borderColor: '#e0e4e9', height: '57px' }}>
        <div className="max-w-7xl mx-auto px-4 h-full flex justify-between items-center">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold tracking-tight" style={{ color: '#7e1fff' }}>Yahoo! <span className="font-normal" style={{ color: '#232a31' }}>TaskFlow Admin</span></h1>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/" className="hidden sm:block text-sm font-medium px-3 py-2 rounded hover:bg-gray-50 transition-colors" style={{ color: '#6e7780' }}>
              View Site
            </Link>
            <button
              onClick={handleLogout}
              className="text-sm font-semibold px-4 py-1.5 rounded-full border transition-all"
              style={{ backgroundColor: '#ffffff', color: '#7e1fff', borderColor: '#7e1fff' }}
            >
              Log Out
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4 border-b pb-6" style={{ borderColor: '#e0e4e9' }}>
            <div>
              <h1 className="text-3xl font-bold mb-2" style={{ color: '#232a31' }}>
                System Administration
              </h1>
              <p className="text-base" style={{ color: '#6e7780' }}>
                Monitor user accounts, security resets, and platform statistics.
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={loadUsers}
                disabled={loading}
                className="inline-flex items-center px-4 py-2 rounded-lg text-sm font-semibold transition-all shadow-sm"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
              >
                {loading ? 'Refreshing...' : 'Refresh List'}
              </button>
            </div>
          </div>

          {/* Status Notifications */}
          {message && (
            <div className={`mb-6 p-4 rounded-xl flex items-center gap-3 animate-fade-in ${message.includes('✓') ? 'bg-green-50 border-green-100' : 'bg-red-50 border-red-100'}`} style={{ border: '1px solid' }}>
              <span className="text-lg">{message.includes('✓') ? '✅' : '⚠️'}</span>
              <p className="text-sm font-medium" style={{ color: message.includes('✓') ? '#065f46' : '#991b1b' }}>{message.replace(/[✓✕]/g, '').trim()}</p>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Users Table Column */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl shadow-sm overflow-hidden" style={{ border: '1px solid #e0e4e9' }}>
                <div className="p-5 border-b flex justify-between items-center bg-gray-50/50" style={{ borderColor: '#e0e4e9' }}>
                  <h2 className="text-lg font-bold" style={{ color: '#232a31' }}>
                    Registered Users
                  </h2>
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider" style={{ backgroundColor: '#f0f3f5', color: '#6e7780' }}>
                    {users.length} Total
                  </span>
                </div>

                {loading && users.length === 0 ? (
                  <div className="p-20 text-center">
                    <div className="animate-spin rounded-full h-10 w-10 border-b-2 mx-auto mb-4" style={{ borderColor: '#7e1fff' }}></div>
                    <p className="text-sm font-medium" style={{ color: '#828a93' }}>Fetching system data...</p>
                  </div>
                ) : users.length === 0 ? (
                  <div className="p-20 text-center">
                    <p className="text-base font-medium" style={{ color: '#828a93' }}>No user accounts discovered in the database.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="bg-gray-50/50 border-b text-xs font-bold uppercase tracking-wider" style={{ borderColor: '#e0e4e9', color: '#828a93' }}>
                          <th className="px-6 py-4 text-left">User Identity</th>
                          <th className="px-6 py-4 text-left hidden md:table-cell">Account Status</th>
                          <th className="px-6 py-4 text-right">Administrative Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y" style={{ borderColor: '#e0e4e9' }}>
                        {users.map((user) => (
                          <tr key={user.id} className="hover:bg-gray-50/30 transition-colors group">
                            <td className="px-6 py-5">
                              <div className="flex items-center">
                                <div className="h-10 w-10 rounded-full flex items-center justify-center text-lg font-bold mr-3 uppercase shrink-0" style={{ backgroundColor: '#f0f3f5', color: '#7e1fff' }}>
                                  {user.email.charAt(0)}
                                </div>
                                <div className="min-w-0">
                                  <div className="text-sm font-bold truncate" style={{ color: '#232a31' }}>{user.email}</div>
                                  <div className="text-xs" style={{ color: '#828a93' }}>ID: {user.id} • Joined {new Date(user.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-5 hidden md:table-cell">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold ${user.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                                <span className={`h-1.5 w-1.5 rounded-full mr-1.5 ${user.is_active ? 'bg-green-500' : 'bg-gray-400'}`}></span>
                                {user.is_active ? 'Active' : 'Offline'}
                              </span>
                            </td>
                            <td className="px-6 py-5 text-right">
                              <div className="flex items-center justify-end gap-2">
                                <button
                                  onClick={() => {
                                    setResetUserId(resetUserId === user.id ? null : user.id);
                                    setNewPassword('');
                                  }}
                                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors text-sm font-semibold"
                                  title="Reset Password"
                                  style={{ color: '#7e1fff' }}
                                >
                                  Reset
                                </button>
                                <button
                                  onClick={() => handleDeleteUser(user.id, user.email)}
                                  className="p-2 rounded-lg hover:bg-red-50 transition-colors text-sm font-semibold"
                                  title="Delete User"
                                  style={{ color: '#ef4444' }}
                                >
                                  Delete
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>

            {/* Sidebar Column */}
            <div className="space-y-6">
              {/* Reset Password Card (Responsive Popover Style on Mobile, Sidebar on Desktop) */}
              {resetUserId && (
                <div className="bg-white rounded-2xl shadow-md p-6 border-2 animate-scale-in" style={{ borderColor: '#7e1fff' }}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold" style={{ color: '#232a31' }}>Security Reset</h3>
                    <button onClick={() => setResetUserId(null)} className="text-gray-400 hover:text-gray-600">✕</button>
                  </div>
                  <p className="text-sm mb-4" style={{ color: '#6e7780' }}>
                    Update credentials for:<br/>
                    <strong style={{ color: '#232a31' }}>{users.find(u => u.id === resetUserId)?.email}</strong>
                  </p>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-bold uppercase tracking-wider mb-1.5" style={{ color: '#828a93' }}>New Password</label>
                      <input
                        type="password"
                        autoFocus
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        placeholder="Min. 6 characters"
                        className="w-full px-4 py-2.5 rounded-xl text-sm border focus:ring-2 outline-none transition-all"
                        style={{ borderColor: '#e0e4e9' }}
                      />
                    </div>
                    <button
                      onClick={() => handleResetPassword(resetUserId)}
                      disabled={loading}
                      className="w-full py-2.5 rounded-xl font-bold text-sm shadow-sm hover:opacity-90 transition-opacity"
                      style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
                    >
                      {loading ? 'Processing...' : 'Confirm Update'}
                    </button>
                  </div>
                </div>
              )}

              {/* Stats Card */}
              <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #e0e4e9' }}>
                <h3 className="text-sm font-bold uppercase tracking-widest mb-4" style={{ color: '#828a93' }}>System Health</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium" style={{ color: '#6e7780' }}>Active DB Connections</span>
                    <span className="text-sm font-bold" style={{ color: '#232a31' }}>Healthy</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium" style={{ color: '#6e7780' }}>API Latency</span>
                    <span className="text-sm font-bold text-green-600">32ms</span>
                  </div>
                  <div className="pt-2 border-t" style={{ borderColor: '#f0f3f5' }}>
                    <p className="text-xs leading-relaxed" style={{ color: '#828a93' }}>
                      All systems operational. Scheduled maintenance in 14 hours.
                    </p>
                  </div>
                </div>
              </div>

              {/* Guidelines Card */}
              <div className="bg-gray-900 rounded-3xl p-6 text-white overflow-hidden relative">
                <div className="relative z-10">
                  <h3 className="font-bold text-lg mb-2">Admin Security</h3>
                  <p className="text-sm text-gray-400 leading-relaxed mb-4">
                    Deleting a user is permanent. All tasks, history, and preferences associated with the account will be wiped from the Neon PostgreSQL cluster.
                  </p>
                  <ul className="text-xs space-y-2 text-gray-300 font-medium">
                    <li className="flex items-center gap-2"><span className="text-purple-400">●</span> Verify identity before resets</li>
                    <li className="flex items-center gap-2"><span className="text-purple-400">●</span> Backup logs if required</li>
                    <li className="flex items-center gap-2"><span className="text-purple-400">●</span> Use strong master keys</li>
                  </ul>
                </div>
                {/* Decorative purple blur */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/20 blur-3xl rounded-full translate-x-10 -translate-y-10"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

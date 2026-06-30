const API_BASE = '/api';

async function apiRequest(path, options = {}, withAuth = true) {
  const headers = options.headers || {};
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }
  if (withAuth) {
    const token = localStorage.getItem('portfolio_token');
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Permintaan gagal diproses');
  }
  return data;
}

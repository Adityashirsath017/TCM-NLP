import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Fetch all predefined photo posts with comment counts.
 */
export const fetchPosts = async () => {
  const response = await apiClient.get('/api/posts');
  return response.data;
};

/**
 * Fetch approved comments for a specific post.
 * @param {number} postId
 */
export const fetchPostComments = async (postId) => {
  const response = await apiClient.get(`/api/posts/${postId}/comments`);
  return response.data;
};

/**
 * Submit a comment to the ML toxicity detection backend.
 * Non-toxic comments get saved and approved; toxic comments get blocked.
 * @param {number} postId
 * @param {string} comment
 */
export const submitComment = async (postId, comment) => {
  const response = await apiClient.post('/api/comments', {
    post_id: postId,
    comment,
  });
  return response.data;
};

/**
 * Run ML toxicity prediction directly on a text comment.
 * @param {string} comment
 */
export const predictComment = async (comment) => {
  const response = await apiClient.post('/api/predict', {
    comment,
  });
  return response.data;
};

/**
 * Health check for backend and ML model readiness.
 */
export const checkHealth = async () => {
  const response = await apiClient.get('/api/health');
  return response.data;
};

export default apiClient;

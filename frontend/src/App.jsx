import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Feed from './components/Feed';
import CommentModal from './components/CommentModal';
import { fetchPosts, fetchPostComments, submitComment } from './services/api';

export default function App() {
  const [posts, setPosts] = useState([]);
  const [loadingPosts, setLoadingPosts] = useState(true);
  const [postsError, setPostsError] = useState(null);

  // Selected post and modal state
  const [selectedPost, setSelectedPost] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [comments, setComments] = useState([]);
  const [loadingComments, setLoadingComments] = useState(false);

  // Comment submission state
  const [commentText, setCommentText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [toxicAlert, setToxicAlert] = useState(false);
  const [toxicCount, setToxicCount] = useState(0);
  const [safeCount, setSafeCount] = useState(0);
  const [lastPrediction, setLastPrediction] = useState(null);
  const [successMessage, setSuccessMessage] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Initial load of posts
  const loadPosts = useCallback(async () => {
    try {
      setLoadingPosts(true);
      setPostsError(null);
      const data = await fetchPosts();
      setPosts(data);
    } catch (err) {
      console.error('Failed to load posts:', err);
      setPostsError('Unable to load posts. Please check your connection.');
    } finally {
      setLoadingPosts(false);
    }
  }, []);

  useEffect(() => {
    loadPosts();
  }, [loadPosts]);

  // Open comments for a specific post
  const handleOpenComments = async (post) => {
    setSelectedPost(post);
    setIsModalOpen(true);
    setComments([]);
    setCommentText('');
    setToxicAlert(false);
    setSuccessMessage(false);
    setErrorMessage('');

    try {
      setLoadingComments(true);
      const postComments = await fetchPostComments(post.id);
      setComments(postComments);
    } catch (err) {
      console.error('Failed to load comments:', err);
      setErrorMessage('Unable to load comments for this post.');
    } finally {
      setLoadingComments(false);
    }
  };

  // Close comments modal
  const handleCloseComments = () => {
    setIsModalOpen(false);
    setSelectedPost(null);
    setToxicAlert(false);
    setSuccessMessage(false);
    setErrorMessage('');
  };

  // Submit comment handler with real-time AI toxicity check
  const handleSubmitComment = async (e) => {
    if (e) e.preventDefault();

    const trimmed = commentText.trim();
    if (!trimmed) {
      setErrorMessage('Please enter a comment.');
      return;
    }

    if (trimmed.length > 500) {
      setErrorMessage('Comment is too long. Maximum 500 characters.');
      return;
    }

    if (!selectedPost) return;

    setIsAnalyzing(true);
    setToxicAlert(false);
    setSuccessMessage(false);
    setErrorMessage('');

    try {
      const result = await submitComment(selectedPost.id, trimmed);

      const predictionInfo = {
        text: trimmed,
        prediction: result.prediction || (result.toxic ? 'Toxic' : 'Non-Toxic'),
        toxic_probability: result.toxic_probability ?? result.probability ?? 0,
        threshold: result.threshold || 0.20,
        model: result.model || 'ToxicGuard-MuRIL'
      };
      setLastPrediction(predictionInfo);

      if (result.toxic || result.status === 'blocked') {
        // Toxic comment blocked!
        setToxicCount((prev) => prev + 1);
        setToxicAlert(true);
      } else if (result.comment) {
        // Non-toxic comment approved!
        // Immediately add to visible comments list
        setComments((prev) => [...prev, result.comment]);
        setSafeCount((prev) => prev + 1);

        // Increment post comment count in state
        setPosts((prevPosts) =>
          prevPosts.map((p) =>
            p.id === selectedPost.id
              ? { ...p, comment_count: p.comment_count + 1 }
              : p
          )
        );

        // Show success feedback
        setSuccessMessage(true);
        setCommentText('');

        setTimeout(() => {
          setSuccessMessage(false);
        }, 4000);
      }
    } catch (err) {
      console.error('Comment submission error:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        setErrorMessage(typeof err.response.data.detail === 'string' ? err.response.data.detail : (err.response.data.detail?.error || 'Unable to post comment.'));
      } else if (err.response && err.response.data && err.response.data.error) {
        setErrorMessage(err.response.data.error);
      } else {
        setErrorMessage('⚠️ Unable to analyze comment. Please try again.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="app-container">
      <Header />

      <Feed
        posts={posts}
        loading={loadingPosts}
        error={postsError}
        onOpenComments={handleOpenComments}
        onRetry={loadPosts}
      />

      <CommentModal
        isOpen={isModalOpen}
        onClose={handleCloseComments}
        post={selectedPost}
        comments={comments}
        loadingComments={loadingComments}
        commentText={commentText}
        setCommentText={setCommentText}
        onSubmitComment={handleSubmitComment}
        isAnalyzing={isAnalyzing}
        toxicAlert={toxicAlert}
        setToxicAlert={setToxicAlert}
        toxicCount={toxicCount}
        safeCount={safeCount}
        lastPrediction={lastPrediction}
        successMessage={successMessage}
        errorMessage={errorMessage}
        setErrorMessage={setErrorMessage}
      />
    </div>
  );
}

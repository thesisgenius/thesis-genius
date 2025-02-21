import React, { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import '../styles/Forum.css';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

const Forum = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const [loading, setLoading] = useState(true);

  // Fetch all forum posts on component load
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await apiClient.get('/forum/posts');
        setPosts(response.data.posts);
      } catch (error) {
        console.error('Failed to fetch posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  // Handle input changes for creating a new post
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewPost({ ...newPost, [name]: value });
  };

  // Handle submission of a new post
  const handleCreatePost = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/forum/posts', newPost);
      setPosts((prevPosts) => [response.data.post, ...prevPosts]); // Add the new post to the list
      setNewPost({ title: '', content: '' }); // Reset the form
    } catch (error) {
      console.error('Failed to create post:', error);
    }
  };

  if (loading) {
    return <p>Loading posts...</p>;
  }

  return (
    <div>
      <h2 className='font-bold text-2xl'>ThesisGenius Forum</h2>
      <p className='text-gray-700 mt-2'>
        This is the forum page. Here you can create a new post and view all the
        posts.
      </p>

      <div className='mt-8 grid gap-8 lg:grid-cols-2'>
        <div>
          <h3 className='font-bold text-xl'>Create a Post</h3>
          <form onSubmit={handleCreatePost} className='mt-4'>
            <Label htmlFor='title'>Title</Label>
            <Input
              id='title'
              type='text'
              className='mt-1'
              placeholder='Enter post title'
              value={newPost.title}
              onChange={handleInputChange}
              required
            />
            <Label htmlFor='content' className='mt-3'>
              Content
            </Label>
            <Textarea
              id='content'
              placeholder='Enter post content'
              className='mt-1'
              value={newPost.content}
              onChange={handleInputChange}
              required
            />

            <Button type='submit' className='mt-3'>
              Create Post
            </Button>
          </form>
        </div>

        {/* Forum Posts */}
        <div className=''>
          <h2 className='font-bold text-xl'>All Posts</h2>
          <div className='border w-full h-full rounded p-6 mt-6'>
            {posts.length === 0 ? (
              <p>No posts available.</p>
            ) : (
              posts.map((post) => (
                <div key={post.id} className='post'>
                  <h3>{post.title}</h3>
                  <p>{post.content}</p>
                  <small>
                    Posted on: {new Date(post.created_at).toLocaleString()}
                  </small>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Forum;

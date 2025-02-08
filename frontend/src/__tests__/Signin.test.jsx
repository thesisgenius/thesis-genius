import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SignIn from '../pages/SignIn';
import apiClient from '../services/apiClient';

// Mock the apiClient
jest.mock('../services/apiClient', () => ({
  post: jest.fn()
}));

describe('SignIn Component', () => {
  beforeEach(() => {
    // Mock localStorage.setItem
    Storage.prototype.setItem = jest.fn();
  });

  test('renders SignIn form', () => {
    render(
      <BrowserRouter>
        <SignIn />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('handles input changes', () => {
    render(
      <BrowserRouter>
        <SignIn />
      </BrowserRouter>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(emailInput, { target: { value: 'john.doetest@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(emailInput.value).toBe('john.doetest@example.com');
    expect(passwordInput.value).toBe('password123');
  });

  test('handles form submission', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { token: 'fake-token' } });

    render(
      <BrowserRouter>
        <SignIn />
      </BrowserRouter>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: 'john.doetest@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/signin', {
        email: 'john.doetest@example.com',
        password: 'password123',
      });

      expect(localStorage.setItem).toHaveBeenCalledWith('token', 'fake-token');
    });
  });
});
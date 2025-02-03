import { TextEncoder, TextDecoder } from 'util';
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Signup from '../pages/SignUp';
import apiClient from '../services/apiClient';

// Mock the apiClient
jest.mock('../services/apiClient', () => ({
  post: jest.fn()
}));

describe('Signup Component', () => {
  test('renders Signup form', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByText(/sign up/i)).toBeInTheDocument();
  });

  test('handles input changes', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );

    const firstNameInput = screen.getByLabelText(/first name/i);
    const lastNameInput = screen.getByLabelText(/last name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(firstNameInput, { target: { value: 'John' } });
    fireEvent.change(lastNameInput, { target: { value: 'Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john.doetest@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(firstNameInput.value).toBe('John');
    expect(lastNameInput.value).toBe('Doe');
    expect(emailInput.value).toBe('john.doetest@example.com');
    expect(passwordInput.value).toBe('password123');
  });

  test('handles form submission', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { success: true } });
    apiClient.post.mockResolvedValueOnce({ data: { token: 'fake-token' } });

    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );

    const firstNameInput = screen.getByLabelText(/first name/i);
    const lastNameInput = screen.getByLabelText(/last name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByText(/sign up/i);

    fireEvent.change(firstNameInput, { target: { value: 'John' } });
    fireEvent.change(lastNameInput, { target: { value: 'Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john.doetest@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    fireEvent.click(submitButton);

    expect(apiClient.post).toHaveBeenCalledWith('/auth/register', {
      first_name: 'John',
      last_name: 'Doe',
      email: 'john.doetest@example.com',
      password: 'password123',
    });

    expect(apiClient.post).toHaveBeenCalledWith('/auth/signin', {
      email: 'john.doetest@example.com',
      password: 'password123',
    });
  });
});
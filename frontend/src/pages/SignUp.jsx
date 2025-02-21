import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authAPI from '../services/authEndpoint'; // Use authAPI for authentication-related actions
import useRedirectIfAuthenticated from '../hooks/useRedirectIfAuthenticated';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Link } from 'react-router-dom';

export default function RegisterPage() {
  useRedirectIfAuthenticated(); // Redirect if already authenticated

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    institution: '',
  });
  const [loading, setLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const navigate = useNavigate();

  // Handle input changes for the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Password Validation Logic
  const validatePassword = (password) => {
    // Ensure password has at least 8 characters, one uppercase, one number, and one special character
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(password);
  };

  // Handle form submission
  const handleSignup = async (e) => {
    e.preventDefault();
    const errors = {};

    // Validate inputs
    if (!formData.first_name) errors.first_name = 'First name is required.';
    if (!formData.last_name) errors.last_name = 'Last name is required.';
    if (!formData.email) errors.email = 'Email is required.';
    if (!formData.password) {
      errors.password = 'Password is required.';
    } else if (!validatePassword(formData.password)) {
      errors.password =
        'Password must contain at least 8 characters, one uppercase letter, one number, and one special character.';
    }
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match.';
    }
    if (!formData.institution) errors.institution = 'Institution is required.';

    // If errors exist, set them and stop form submission
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setLoading(true);
    try {
      // Register the user through authAPI.register
      const response = await authAPI.register(formData);
      if (response.success) {
        // Automatically sign in the user after registration using authAPI.signIn
        const signInResponse = await authAPI.signIn({
          email: formData.email,
          password: formData.password,
        });

        const { token } = signInResponse;
        localStorage.setItem('token', token); // Save the token
        alert('Signup successful! Redirecting to dashboard...');
        navigate('/dashboard'); // Redirect to the dashboard
      } else {
        alert(response.message || 'Signup failed. Please try again.');
      }
    } catch (error) {
      console.error('Signup failed:', error);
      alert('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='flex w-full justify-center px-4 py-12 md:py-16 lg:py-24'>
      <Card className='mx-auto max-w-md'>
        <CardHeader>
          <CardTitle className='text-2xl tracking-normal'>
            Register to ThesisGenius
          </CardTitle>
          <CardDescription>Create an account to get started</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSignup}>
            <div className='grid gap-4'>
              <div className='grid grid-cols-2 gap-4'>
                <div className='grid gap-2'>
                  <Label htmlFor='first_name'>First Name</Label>
                  <Input
                    name='first_name'
                    value={formData.first_name}
                    onChange={handleInputChange}
                    id='first_name'
                    type='text'
                    placeholder='Peter'
                    required
                  />
                  <span className='text-sm text-red-500'>
                    {formErrors.first_name}
                  </span>
                </div>

                <div className='grid gap-2'>
                  <Label htmlFor='last_name'>Last Name</Label>
                  <Input
                    value={formData.last_name}
                    onChange={handleInputChange}
                    name='last_name'
                    id='last_name'
                    type='text'
                    placeholder='Parker'
                    required
                  />
                  <span className='text-sm text-red-500'>
                    {formErrors.last_name}
                  </span>
                </div>
              </div>
              <div className='grid gap-2'>
                <Label htmlFor='email'>Email</Label>
                <Input
                  id='email'
                  type='email'
                  name='email'
                  placeholder='peterparker@example.com'
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
                <span className='text-sm text-red-500'>{formErrors.email}</span>
              </div>
              <div className='grid gap-2'>
                <Label htmlFor='password'>Password</Label>
                <Input
                  id='password'
                  name='password'
                  type='password'
                  placeholder='••••••••'
                  required
                  minLength={8}
                  value={formData.password}
                  onChange={handleInputChange}
                />
                <span className='text-sm text-red-500'>
                  {formErrors.password}
                </span>
              </div>
              <div className='grid gap-2'>
                <Label htmlFor='confirmPassword'>Confirm Password</Label>
                <Input
                  id='confirmPassword'
                  type='password'
                  name='confirmPassword'
                  placeholder='••••••••'
                  required
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  minLength={8}
                />
                <span className='text-sm text-red-500'>
                  {formErrors.confirmPassword}
                </span>
              </div>
              <div className='grid gap-2'>
                <Label htmlFor='institution'>Institution</Label>
                <Input
                  id='institution'
                  type='text'
                  name='institution'
                  value={formData.institution}
                  onChange={handleInputChange}
                  placeholder='Cambridge University'
                  required
                />
                <span className='text-sm text-red-500'>
                  {formErrors.institution}
                </span>
              </div>

              <Button type='submit' className='w-full' disabled={loading}>
                {loading ? 'Signing Up...' : 'Sign Up'}
              </Button>
              <div className='relative'>
                <div className='absolute inset-0 flex items-center'>
                  <span className='w-full border-t' />
                </div>
                <div className='relative flex justify-center text-xs uppercase'>
                  <span className='bg-background px-2 text-muted-foreground'>
                    Or continue with
                  </span>
                </div>
              </div>
              <div className='grid grid-cols-2 gap-4'>
                <Button variant='outline' className='w-full'>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    width={200}
                    height={200}
                    fill='currentColor'
                    stroke='currentColor'
                    strokeWidth={0}
                    className='h-5 w-5'
                    viewBox='0 0 48 48'
                  >
                    <path
                      fill='#FFC107'
                      stroke='none'
                      d='M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z'
                    />
                    <path
                      fill='#FF3D00'
                      stroke='none'
                      d='m6.306 14.691 6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z'
                    />
                    <path
                      fill='#4CAF50'
                      stroke='none'
                      d='M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z'
                    />
                    <path
                      fill='#1976D2'
                      stroke='none'
                      d='M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z'
                    />
                  </svg>
                  Google
                </Button>
                <Button variant='outline' className='w-full'>
                  <svg viewBox='0 0 438.549 438.549' className='h-5 w-5'>
                    <path
                      fill='currentColor'
                      d='M409.132 114.573c-19.608-33.596-46.205-60.194-79.798-79.8-33.598-19.607-70.277-29.408-110.063-29.408-39.781 0-76.472 9.804-110.063 29.408-33.596 19.605-60.192 46.204-79.8 79.8C9.803 148.168 0 184.854 0 224.63c0 47.78 13.94 90.745 41.827 128.906 27.884 38.164 63.906 64.572 108.063 79.227 5.14.954 8.945.283 11.419-1.996 2.475-2.282 3.711-5.14 3.711-8.562 0-.571-.049-5.708-.144-15.417a2549.81 2549.81 0 01-.144-25.406l-6.567 1.136c-4.187.767-9.469 1.092-15.846 1-6.374-.089-12.991-.757-19.842-1.999-6.854-1.231-13.229-4.086-19.13-8.559-5.898-4.473-10.085-10.328-12.56-17.556l-2.855-6.57c-1.903-4.374-4.899-9.233-8.992-14.559-4.093-5.331-8.232-8.945-12.419-10.848l-1.999-1.431c-1.332-.951-2.568-2.098-3.711-3.429-1.142-1.331-1.997-2.663-2.568-3.997-.572-1.335-.098-2.43 1.427-3.289 1.525-.859 4.281-1.276 8.28-1.276l5.708.853c3.807.763 8.516 3.042 14.133 6.851 5.614 3.806 10.229 8.754 13.846 14.842 4.38 7.806 9.657 13.754 15.846 17.847 6.184 4.093 12.419 6.136 18.699 6.136 6.28 0 11.704-.476 16.274-1.423 4.565-.952 8.848-2.383 12.847-4.285 1.713-12.758 6.377-22.559 13.988-29.41-10.848-1.14-20.601-2.857-29.264-5.14-8.658-2.286-17.605-5.996-26.835-11.14-9.235-5.137-16.896-11.516-22.985-19.126-6.09-7.614-11.088-17.61-14.987-29.979-3.901-12.374-5.852-26.648-5.852-42.826 0-23.035 7.52-42.637 22.557-58.817-7.044-17.318-6.379-36.732 1.997-58.24 5.52-1.715 13.706-.428 24.554 3.853 10.85 4.283 18.794 7.952 23.84 10.994 5.046 3.041 9.089 5.618 12.135 7.708 17.705-4.947 35.976-7.421 54.818-7.421s37.117 2.474 54.823 7.421l10.849-6.849c7.419-4.57 16.18-8.758 26.262-12.565 10.088-3.805 17.802-4.853 23.134-3.138 8.562 21.509 9.325 40.922 2.279 58.24 15.036 16.18 22.559 35.787 22.559 58.817 0 16.178-1.958 30.497-5.853 42.966-3.9 12.471-8.941 22.457-15.125 29.979-6.191 7.521-13.901 13.85-23.131 18.986-9.232 5.14-18.182 8.85-26.84 11.136-8.662 2.286-18.415 4.004-29.263 5.146 9.894 8.562 14.842 22.077 14.842 40.539v60.237c0 3.422 1.19 6.279 3.572 8.562 2.379 2.279 6.136 2.95 11.276 1.995 44.163-14.653 80.185-41.062 108.068-79.226 27.88-38.161 41.825-81.126 41.825-128.906-.01-39.771-9.818-76.454-29.414-110.049z'
                    ></path>
                  </svg>
                  GitHub
                </Button>
              </div>
            </div>
          </form>
          <div className='mt-4 text-center text-sm'>
            Already have an account?{' '}
            <Link to='/signin' className='underline'>
              Sign in
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

import { Link, useNavigate } from 'react-router-dom';

import Logo from '/owl.png';
import { Button } from './ui/button';

import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu } from 'lucide-react';

import { useAuth } from '../context/AuthContext';

export default function NewHeader() {
  const { user, signOut, refreshUser } = useAuth(); // Include refreshUser
  const navigate = useNavigate();

  // Handle Logout
  const handleLogout = () => {
    signOut(); // Log the user out
    navigate('/'); // Redirect to home after logout
  };

  // Manual User Refresh Button
  const handleRefresh = async () => {
    await refreshUser(); // Explicit action for the user to refresh their auth state/profile
  };

  return (
    <header className='bg-gray-800 py-3 px-4 lg:!px-8'>
      <nav className='flex justify-between items-center'>
        <Link to='/' className='inline-flex gap-2 items-center'>
          <img className='h-12 w-auto' src={Logo} alt='logo' />
          <div>
            <h1 className='font-bold text-2xl text-sky-300'>ThesisGenius</h1>
            <p className='italic text-white'>write smart, write less</p>
          </div>
        </Link>

        <Sheet>
          <SheetTrigger className='lg:hidden'>
            <Menu className='text-white' />
          </SheetTrigger>
          <SheetContent className='flex flex-col pt-16'>
            <Button variant='link'>
              <Link to='/about'>About</Link>
            </Button>
            <Button variant='link'>
              <Link to='/app/title'>Dashboard</Link>
            </Button>
            <Button variant='link'>
              <Link to='https://resources.nu.edu/Chatpage'>Forum</Link>
            </Button>
            {user ? (
              <>
                <Button variant='link' onClick={handleRefresh}>
                  Refresh Profile
                </Button>
                <Button variant='link' onClick={handleLogout}>
                  Log out
                </Button>
              </>
            ) : (
              <>
                <Button variant='link'>
                  <Link to='/signin'>Sign in</Link>
                </Button>
                <Button variant='link'>
                  <Link to='/signup'>Register</Link>
                </Button>
              </>
            )}
          </SheetContent>
        </Sheet>

        <div className='gap-4 hidden lg:flex'>
          <Button variant='link'>
            <Link className='text-white' to='/about'>
              About
            </Link>
          </Button>
          <Button variant='link'>
            <Link className='text-white' to='/app/title'>
              Dashboard
            </Link>
          </Button>
          <Button variant='link'>
            <Link className='text-white' to='https://resources.nu.edu/Chatpage'>
              Forum
            </Link>
          </Button>
        </div>

        {user ? (
          <div className='hidden lg:flex gap-4'>
            <Button onClick={handleRefresh} variant='outline'>
              Refresh Profile
            </Button>

            <Button onClick={handleLogout} variant='destructive'>
              Log out
            </Button>
          </div>
        ) : (
          <div className='hidden lg:flex gap-4'>
            <Button asChild>
              <Link to='signin'>Sign In</Link>
            </Button>
            <Button variant='outline' asChild>
              <Link to='signup'>Register</Link>
            </Button>
          </div>
        )}
      </nav>
    </header>
  );
}

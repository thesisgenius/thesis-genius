import { AppSidebar } from '@/components/app-sidebar';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar';
import { Link, Outlet } from 'react-router-dom';

import { Printer } from 'lucide-react';

export default function Page() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className='flex justify-between sticky top-0 bg-background h-16 shrink-0 items-center gap-2 border-b px-4'>
          <SidebarTrigger className='-ml-1' />

          <div className='flex gap-4 items-center'>
            <Button
              onClick={() => window.print()}
              variant='outline'
              size='icon'
              className='rounded-full'
            >
              <Printer />
            </Button>

            <Link to='profile'>
              <Avatar className='w-8 h-8'>
                <AvatarImage src='https://img.freepik.com/free-vector/businessman-character-avatar-isolated_24877-60111.jpg?t=st=1740139365~exp=1740142965~hmac=0a8643f076a7891418a117d4329c305e5c82c5deca2c64a2280ba1603a53efac&w=1480' />
                <AvatarFallback>A</AvatarFallback>
              </Avatar>
            </Link>
          </div>
        </header>
        <div className='flex flex-1 flex-col gap-4 p-4'>
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export default function ProfilePage() {
  return (
    <div className='container mx-auto px-4 py-8'>
      <h1 className='text-4xl font-bold mb-8'>Your Profile</h1>
      <div className='flex flex-col md:flex-row gap-8'>
        <Card className='w-full md:w-1/3'>
          <CardHeader>
            <CardTitle>Profile Picture</CardTitle>
          </CardHeader>
          <CardContent className='flex flex-col items-center'>
            <Avatar className='w-32 h-32'>
              <AvatarImage
                src='/placeholder-avatar.jpg'
                alt='Profile picture'
              />
              <AvatarFallback>PP</AvatarFallback>
            </Avatar>
            <Button className='mt-4'>Change Picture</Button>
          </CardContent>
        </Card>
        <Card className='w-full md:w-2/3'>
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>Update your personal details</CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div className='grid grid-cols-2 gap-4'>
              <div className='space-y-2'>
                <label htmlFor='first-name'>First Name</label>
                <Input id='first-name' defaultValue='Peter' />
              </div>
              <div className='space-y-2'>
                <label htmlFor='last-name'>Last Name</label>
                <Input id='last-name' defaultValue='Parker' />
              </div>
            </div>
            <div className='space-y-2'>
              <label htmlFor='email'>Email</label>
              <Input
                id='email'
                type='email'
                defaultValue='peter.parker@gmail.com'
              />
            </div>
            <div className='space-y-2'>
              <label htmlFor='institution'>Institution</label>
              <Input id='institution' defaultValue='Cambridge University' />
            </div>
          </CardContent>
          <CardFooter>
            <Button>Save Changes</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

import { Button } from '@/components/ui/button';
import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    BookOpen,
    Users,
    MessageSquare,
    Lightbulb,
    ArrowRight,
    GraduationCap,
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <main className='flex flex-col min-h-screen'>
            {/* Hero Section */}

            {/* Bg gradient */}
            <section className='w-full py-12 md:py-24 lg:py-32 xl:py-48'>
                <div className='absolute inset-0 -z-10 h-full w-full bg-white bg-[linear-gradient(to_right,#f0f0f0_1px,transparent_1px),linear-gradient(to_bottom,#f0f0f0_1px,transparent_1px)] bg-[size:6rem_4rem]'>
                    <div className='absolute bottom-0 left-0 right-0 top-0 bg-[radial-gradient(circle_500px_at_50%_200px,#C9EBFF,transparent)]'></div>
                </div>

                <div className='container px-4 md:px-6'>
                    <div className='flex flex-col items-center space-y-4 text-center'>
                        <div className='space-y-4'>
                            <h1 className='text-3xl font-bold sm:text-4xl md:text-5xl lg:text-6xl/none'>
                                Write Your Thesis with Confidence
                            </h1>
                            <p className='mx-auto max-w-[700px] text-muted-foreground md:text-xl !leading-relaxed'>
                                The all-in-one platform for writing, managing, and discussing
                                your academic thesis. Join a community of scholars and make your
                                research journey easier.
                            </p>
                        </div>
                        <div className='space-x-6 mt-5'>
                            <Button size='lg' className='h-11 px-8' asChild>
                                <Link to='/signup'>
                                    Get Started
                                    <ArrowRight className='ml-2 h-4 w-4' />
                                </Link>
                            </Button>
                            <Button asChild variant='outline' size='lg' className='h-11 px-8'>
                                <Link to='/about'>Learn More</Link>
                            </Button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className='w-full py-12 md:py-24 lg:py-32'>
                <div className='container px-4 md:px-6'>
                    <div className='grid gap-10 sm:grid-cols-2 lg:grid-cols-3'>
                        <Card>
                            <CardHeader>
                                <BookOpen className='h-10 w-10 text-primary mb-4' />
                                <CardTitle className='tracking-normal'>
                                    Smart Writing Tools
                                </CardTitle>
                                <CardDescription className='mt-2'>
                                    Advanced editor with citation management, formatting tools,
                                    and real-time collaboration features.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                        <Card>
                            <CardHeader>
                                <Users className='h-10 w-10 text-primary mb-4' />
                                <CardTitle className='tracking-normal'>
                                    Academic Community
                                </CardTitle>
                                <CardDescription className='mt-2'>
                                    Connect with fellow researchers, share insights, and get
                                    valuable feedback on your work.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                        <Card>
                            <CardHeader>
                                <MessageSquare className='h-10 w-10 text-primary mb-4' />
                                <CardTitle className='tracking-normal'>
                                    Expert Discussions
                                </CardTitle>
                                <CardDescription className='mt-2'>
                                    Engage in meaningful academic discussions and receive guidance
                                    from experienced scholars.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className='w-full py-12 md:py-24 lg:py-24 bg-primary/5'>
                <div className='container px-4 md:px-6'>
                    <div className='grid gap-10 sm:grid-cols-2 lg:grid-cols-4'>
                        <div className='flex flex-col items-center space-y-2'>
                            <h3 className='text-3xl font-bold'>10k+</h3>
                            <p className='text-muted-foreground'>Active Users</p>
                        </div>
                        <div className='flex flex-col items-center space-y-2'>
                            <h3 className='text-3xl font-bold'>5k+</h3>
                            <p className='text-muted-foreground'>Completed Theses</p>
                        </div>
                        <div className='flex flex-col items-center space-y-2'>
                            <h3 className='text-3xl font-bold'>100+</h3>
                            <p className='text-muted-foreground'>Universities</p>
                        </div>
                        <div className='flex flex-col items-center space-y-2'>
                            <h3 className='text-3xl font-bold'>50k+</h3>
                            <p className='text-muted-foreground'>Discussions</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className='w-full py-12 md:py-24 lg:py-32'>
                <div className='container px-4 md:px-6'>
                    <div className='flex flex-col items-center justify-center space-y-4 text-center'>
                        <div className='space-y-2'>
                            <h2 className='text-3xl font-bold sm:text-5xl'>How It Works</h2>
                            <p className='max-w-[900px] text-muted-foreground md:text-xl mt-2'>
                                Get started with Thesis Genius in three simple steps
                            </p>
                        </div>
                        <div className='grid gap-16 sm:grid-cols-3 pt-8'>
                            <div className='flex flex-col items-center space-y-4'>
                                <div className='rounded-full bg-primary/10 p-4'>
                                    <GraduationCap className='h-8 w-8 text-primary' />
                                </div>
                                <h3 className='text-xl font-bold'>Create Account</h3>
                                <p className='text-muted-foreground text-center'>
                                    Sign up and set up your academic profile
                                </p>
                            </div>
                            <div className='flex flex-col items-center space-y-4'>
                                <div className='rounded-full bg-primary/10 p-4'>
                                    <BookOpen className='h-8 w-8 text-primary' />
                                </div>
                                <h3 className='text-xl font-bold'>Start Writing</h3>
                                <p className='text-muted-foreground text-center'>
                                    Use our powerful tools to write your thesis
                                </p>
                            </div>
                            <div className='flex flex-col items-center space-y-4'>
                                <div className='rounded-full bg-primary/10 p-4'>
                                    <Lightbulb className='h-8 w-8 text-primary' />
                                </div>
                                <h3 className='text-xl font-bold'>Get Feedback</h3>
                                <p className='text-muted-foreground text-center'>
                                    Collaborate and receive expert insights
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className='w-full py-12 md:py-24 lg:py-32 bg-primary/5'>
                <div className='container px-4 md:px-6'>
                    <div className='flex flex-col items-center justify-center space-y-4 text-center'>
                        <div className='space-y-2'>
                            <h2 className='text-3xl font-bold sm:text-4xl md:text-5xl'>
                                Ready to Start Your Thesis Journey?
                            </h2>
                            <p className='mx-auto max-w-[600px] text-muted-foreground md:text-xl !leading-relaxed'>
                                Join thousands of researchers who are already using Thesis
                                Genius to write better theses.
                            </p>
                        </div>
                        <div className='space-x-4'>
                            <Button size='lg' className='h-11 px-8' asChild>
                                <Link to='/signup'>
                                    Get Started Now
                                    <ArrowRight className='ml-2 h-4 w-4' />
                                </Link>
                            </Button>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    );
};

export default Home;

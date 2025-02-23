import React, { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import './../styles/Thesis.css';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

const Thesis = () => {
    const [theses, setTheses] = useState([]);
    const [newThesis, setNewThesis] = useState({
        title: '',
        abstract: '',
        status: 'Draft',
        content: '',
    });
    const [loading, setLoading] = useState(true);

    // Fetch all theses on component load
    useEffect(() => {
        const fetchTheses = async () => {
            try {
                const response = await apiClient.get('/thesis/theses');
                setTheses(response.data.theses);
            } catch (error) {
                console.error('Failed to fetch theses:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchTheses();
    }, []);

    // Handle input changes for creating or editing a thesis
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewThesis({ ...newThesis, [name]: value });
    };

    // Handle submission of a new thesis
    const handleCreateThesis = async (e) => {
        e.preventDefault();
        try {
            const response = await apiClient.post('/thesis/new', newThesis);
            setTheses((prevTheses) => [response.data.thesis, ...prevTheses]); // Add the new thesis to the list
            setNewThesis({ title: '', abstract: '', status: 'Draft' }); // Reset the form
        } catch (error) {
            console.error('Failed to create thesis:', error);
        }
    };

    // Handle deletion of a thesis
    const handleDeleteThesis = async (id) => {
        try {
            await apiClient.delete(`/thesis/${id}`);
            setTheses((prevTheses) =>
                prevTheses.filter((thesis) => thesis.id !== id)
            ); // Remove the deleted thesis
        } catch (error) {
            console.error('Failed to delete thesis:', error);
        }
    };

    if (loading) {
        return <p>Loading theses...</p>;
    }

    return (
        <div>
            <h2 className='font-bold text-2xl'>Thesis Management</h2>
            <p className='text-gray-700 mt-2'>
                This is the Thesis Management page. Here you can manage your theses.
            </p>

            <div className='mt-8 grid gap-8 lg:grid-cols-2'>
                <div>
                    <h3 className='font-bold text-xl'>Create a Thesis</h3>
                    <form onSubmit={handleCreateThesis} className='mt-4'>
                        <Label htmlFor='title'>Title</Label>
                        <Input
                            id='title'
                            type='text'
                            className='mt-1'
                            placeholder='Enter a thesis title'
                            value={newThesis.title}
                            onChange={handleInputChange}
                            required
                        />
                        <Label htmlFor='abstract' className='mt-3'>
                            Abstract
                        </Label>
                        <Textarea
                            id='abstract'
                            placeholder='Enter post abstract'
                            className='mt-1'
                            value={newThesis.abstract}
                            onChange={handleInputChange}
                            required
                        />

                        <Label htmlFor='status' className='mt-3'>
                            Status
                        </Label>
                        <Select
                            name='status'
                            value={newThesis.status}
                            onChange={handleInputChange}
                        >
                            <SelectTrigger className='w-[180px]'>
                                <SelectValue placeholder='Theme' />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value='Draft'>Draft</SelectItem>
                                <SelectItem value='Approved'>Approved</SelectItem>
                                <SelectItem value='Rejected'>Rejected</SelectItem>
                            </SelectContent>
                        </Select>

                        <Button type='submit' className='mt-3'>
                            Create Thesis
                        </Button>
                    </form>
                </div>

                {/* Forum Posts */}
                <div className=''>
                    <h2 className='font-bold text-xl'>Theses</h2>
                    <div className='border w-full h-full rounded p-6 mt-6'>
                        {theses.length === 0 ? (
                            <p>No theses available.</p>
                        ) : (
                            theses.map((thesis) => (
                                <div key={thesis.id} className='thesis'>
                                    <h3>{thesis.title}</h3>
                                    <p>{thesis.abstract}</p>
                                    <small>{thesis.status}</small>
                                    <small>
                                        Posted on: {new Date(post.created_at).toLocaleString()}
                                    </small>

                                    <button onClick={() => handleDeleteThesis(thesis.id)}>
                                        Delete
                                    </button>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Thesis;

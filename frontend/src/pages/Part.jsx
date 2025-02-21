import { useState } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import FadingBanner from '../components/FadingBanner';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/Button';
import { Link } from 'react-router-dom';

const Part = ({ headerText, textAreaPlaceholder }) => {
  const [text, setText] = useState('');

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className='container'>
      <div className='col-md-12'>
        <h3 className='font-bold text-2xl'>{headerText}</h3>
        <p className='mt-2 text-gray-700'>
          An attached example:{' '}
          <a
            className='text-blue-500 underline'
            href='https://apastyle.apa.org/instructional-aids/abstract-keywords-guide.pdf'
            target='_blank'
          >
            Example
          </a>
        </p>
        <p className='mt-1'>
          Relevant APA Rules:{' '}
          <a
            className='text-blue-500 underline'
            href='https://apastyle.apa.org/style-grammar-guidelines'
            target='_blank'
          >
            Link
          </a>
        </p>

        <div className='mt-6 flex flex-col lg:flex-row gap-6'>
          <Textarea
            placeholder={textAreaPlaceholder}
            value={text}
            onChange={handleTextChange}
            className='min-h-60 lg:min-h-96'
          />

          <Textarea
            placeholder='This is a read only textarea. You will see the preview of the text you entered.'
            className='cursor-not-allowed focus-visible:ring-green-500 min-h-60 lg:min-h-96'
            value={text}
            readOnly
          />
        </div>
      </div>

      <Button asChild className='mt-6'>
        <Link to='#'>Continue</Link>
      </Button>

      <div className='row'>
        <FadingBanner />
      </div>
      {/* <div className='col-md-2'>
        <Link to='/dash' className='btn btn-primary mb-3'>
          Back to Dashboard
        </Link>
      </div> */}
    </div>
  );
};

export default Part;

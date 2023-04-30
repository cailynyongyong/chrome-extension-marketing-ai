import React from 'react';
import { useState } from 'react';
import './Newtab.css';

const Newtab = () => {
  const [website, setWebsite] = useState('');
  const [response, setResponse] = useState([]);
  const [loading, setLoading] = useState(Boolean);
  const [product, setProduct] = useState('');
  const [apikey, setAPIKey] = useState('');

  async function fetchData() {
    const response = await fetch('http://127.0.0.1:8000/');
    const jsonData = await response.json();
    console.log('data is: ', jsonData);
  }

  async function textInput() {
    const data = { api: apikey, webName: website, prodName: product };
    const response = await fetch('http://127.0.0.1:8000/website', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const jsonData = await response.json();
    setResponse(jsonData);
    console.log('result from server: ', jsonData);
  }

  async function handleSubmit() {
    console.log('submitted!');
    setLoading(true);

    await fetchData();
    await textInput();
    console.log('test2');
    setLoading(false);
  }

  return (
    <div className="App">
      <header className="App-header">
        <div class="mt-12 inset-x-0 top-0 gap-x-4">
          <input
            required
            name="API"
            type="password"
            class="min-w-0 flex-auto text-sm rounded-md border-0 bg-white/5 px-5 py-1.5 text-slate-700 shadow-sm ring-1 ring-inset ring-slate-600 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6"
            placeholder="Your OpenAI API Key"
            onChange={(e) => setAPIKey(e.target.value)}
          />
        </div>
        <div class="mt-3 inset-x-0 top-0 gap-x-4">
          <input
            required
            class="min-w-0 flex-auto text-sm rounded-md border-0 bg-white/5 px-5 py-1.5 text-slate-700 shadow-sm ring-1 ring-inset ring-slate-600 focus:ring-2 focus:ring-inset focus:ring-green-500 sm:text-sm sm:leading-6"
            placeholder="Product Name"
            onChange={(e) => setProduct(e.target.value)}
          />
        </div>
        <div class="mt-3 inset-x-0 top-0 gap-x-4">
          <input
            required
            class="min-w-0 flex-auto text-sm rounded-md border-0 bg-white/5 px-5 py-1.5 text-slate-700 shadow-sm ring-1 ring-inset ring-slate-600 focus:ring-2 focus:ring-inset focus:ring-green-500 sm:text-sm sm:leading-6"
            placeholder="Enter website"
            onChange={(e) => setWebsite(e.target.value)}
          />
        </div>
        <div class="mt-3 inset-x-0 top-0 gap-x-4">
          <button
            className={`bg-green-500 text-white text-sm font-semibold rounded-lg px-3 py-2 ${
              loading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Generate Tweet'}
          </button>
        </div>
        <div class="mt-8 max-w-md gap-x-4">
          <h6 class="mt-2 text-md font-bold text-slate-500 sm:text-md">
            Response from AI
          </h6>
          <div class="p-4">
            <textarea
              id="message"
              name="message"
              rows="10"
              value={response.message}
              class="resize-none border text-sm rounded-md w-full py-2 px-3 text-gray-700 leading-tight ring-1 ring-inset ring-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
            ></textarea>
          </div>
        </div>
      </header>
    </div>
  );
};

export default Newtab;

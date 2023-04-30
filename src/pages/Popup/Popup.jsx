import React from 'react';
import logo from '../../assets/img/e7ad1921392c6cf96abb.png';
import './Popup.css';

const Popup = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo rounded-md" alt="logo" />
        <h2 class="mt-3 text-xl font-bold text-black sm:text-4xl">
          Marketing AI
        </h2>
        <h2 class="p-4 mt-2 text-sm text-center font-bold text-slate-700 sm:text-sm">
          The AI creates an advertising tweet. Simply paste the website and it
          will automatically generate posts for you!
        </h2>
        <div class="mt-4 flex max-w-md gap-x-4">
          <a
            href="/newtab.html"
            class="flex-none rounded-md bg-green-500 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-500"
          >
            Let's begin!
          </a>
        </div>
        <h2 class="mt-12 text-xs text-center text-slate-500 sm:text-sm">
          Generating the tweet may take to 2-3 minutes.
        </h2>
        <h2 class="text-xs text-center text-slate-400 sm:text-xs">
          Created by @cailynyongyong
        </h2>
      </header>
    </div>
  );
};

export default Popup;

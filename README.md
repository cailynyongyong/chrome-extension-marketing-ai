<img src="src/assets/img/e7ad1921392c6cf96abb.png" width="64"/>

# Chrome Extension for Marketing AI

## Features

This is a basic Chrome Extension that features a Langchain built AI that generates advertising tweets for you automatically.
This extension works as such:

- input your OpenAI API key
- product you wish to advertise
- relevant website about product

## Installing and Running

### Frontend:

1. Check if your [Node.js](https://nodejs.org/) version is >= **14**.
2. Clone this repository.
3. Change the package's `name`, `description`, and `repository` fields in `package.json`.
4. Change the name of your extension on `src/manifest.json`.
5. Run `npm install` to install the dependencies.
6. Run `npm start`
7. Load your extension on Chrome following:
   1. Access `chrome://extensions/`
   2. Check `Developer mode`
   3. Click on `Load unpacked extension`
   4. Select the `build` folder.
8. Happy hacking.

### Backend:

Backend is built with FastAPI server. You need to activate this in order to run the frontend.

```
python -m venv venv
source venv/bin/activate
pip install langchain
pip install openai
pip install faiss-cpu > /dev/null
pip install tiktoken
cd openai-backend
uvicorn app.main:app --reload

```

## Packing

After the development of your extension run the command

```
$ NODE_ENV=production npm run build
```

Now, the content of `build` folder will be the extension ready to be submitted to the Chrome Web Store. Just take a look at the [official guide](https://developer.chrome.com/webstore/publish) to more infos about publishing.

## Resources:

- [Webpack documentation](https://webpack.js.org/concepts/)
- [Chrome Extension documentation](https://developer.chrome.com/extensions/getstarted)

## Credits

### Frontend Chrome Extension Boilerplate

Please check the following resources if you want to know a more detailed explanation on how the frontend works.

- Michael Xieyang Liu | [Website](https://lxieyang.github.io)
- This boilerplate is largely derived from [lxieyang/chrome-extension-boilerplate-react](https://github.com/lxieyang/chrome-extension-boilerplate-react), which in turn is adapted from [samuelsimoes/chrome-extension-webpack-boilerplate](https://github.com/samuelsimoes/chrome-extension-webpack-boilerplate).

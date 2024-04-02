# Large Language Object - 2024 Edition

This is a simple template that combines OpenAI's Node.js SDK, a P5.js sketch, a serial connection to an Arduino, and Vite for code autorefresh.

### What it does:

- Enter a prompt in the text input field and it returns a response from GPT and displays it inside of the P5.js canvas
- Press 'c' to prompt GPT by asking for the color of the sky. It returns a hex color value that is used to fill a square.
- Press 's' to connect to serial port
    - Once connected, press 'h' to turn LED on, and 'l' to turn LED off 

## Arduino

Upload A_LLO to an Arduino and use pin 10 for LED feedback.

## Requirements

This template requires a recent version of Node.js, recommended version 16 or later.

Clone the repository with git or download the code from the repository as a zip file.

Then install the libraries:

    cd LLO
    npm install

## Start the dev environment

This template uses [Vite](https://vitejs.dev/) as a local development server. Start it with the following:

    npm run dev

By default, this starts a local server at http://localhost:5173/. Just copy/paste this URL into
a browser window to view the app. This will automatically update when you save changes to your code (that is, no manual refresh required!).

## OpenAI API Key

Remember to provide your OpenAI API key into `sketch.js`. Note that this is configured
for local development only, and this code should not be used on a production server.

## Credit and More Information

https://medium.spatialpixel.com/programming-natural-language-71075fb3d428
https://github.com/gohai/p5.webserial
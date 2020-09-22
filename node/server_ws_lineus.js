const WebSocket = require('ws');
const LineUs = require('@beardicus/line-us');
const bot = new LineUs();


function randomIntFromInterval(min, max) { // min and max included 
  return Math.floor(Math.random() * (max - min + 1) + min);
}

let instance = null;

bot.on('connected', async () => {
  instance = bot;
});


const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
    let o = {
      x: randomIntFromInterval(0, 200),
      y: randomIntFromInterval(0, 500)
    }
    console.log('>>', o);
    instance.moveTo(o);
    if (message === 'close') {
      wss.close()
    }
  });

  ws.send('something');
});
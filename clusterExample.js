const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;
// const sleep = require('sleep');

console.log('numCPUs', numCPUs);

if (!cluster.isWorker) {
  console.log(`Primary ${process.pid} is running`);

  // Fork workers.
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`worker ${worker.process.pid} died`);
  });
} else {
  // Workers can share any TCP connection
  // In this case it is an HTTP server
  http.createServer(async (req, res) => {
    console.log(`Worker ${process.pid} working`);
    await sleep(1000)
    res.writeHead(200);
    res.end('hello world\n');
  }).listen(8000);

  console.log(`Worker ${process.pid} started`);
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
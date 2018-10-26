
const express = require('express');
const app = express();

const child = require('child_process').execFile;
const executablePath = "./executable_script.sh";


function executeFile(parameters=[]) {
  child(executablePath, parameters, function(err, data) {
    if(err){
      console.error(err)
      console.log(err)
      return
    }
    console.log(data.toString())
  })
}


app.use(express.static('public'));

app.get('/', function(request, response) {

  let toot = null

  if(request.query.toot !== undefined) {
    toot = request.query.toot
  }

  const named_parameters_list = [toot=toot]
  executeFile(named_parameters_list)

  response.sendFile(__dirname + '/views/index.html');

});

const listener = app.listen(process.env.PORT, function() {
  console.log('Your app is listening on port ' + listener.address().port);
});



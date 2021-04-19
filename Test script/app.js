//api
const express = require('express');
const app = express();
app.use(express.json());
//schedule
const schedule = require('node-schedule');
//filestream
fs = require('fs');
//env variables
const dotenv = require('dotenv');
dotenv.config(); //add post middleware
//make api calls with axios
const axios = require('axios');

  app.get('/trackracesentiment/:laptime/:laps/:filename', async function (req, res) {

    const laptime = req.params.laptime;
    const laps = req.params.laps;
    const filename = req.params.filename;

    ScheduleInterval(laptime, laps, filename);

    res.send(`<h4>Program started with the following settings:</h4> 
              <h5>laptime in seconds: ${laptime}</h5> <h5>amount of laps: ${laps}</h5> 
              <h5>filename: ${filename}.txt</h5> 
              <p><i>The program will now track sentiment for the duration of the race.</i></p>`);
  });

  //App listen
const port = process.env.PORT || 3001;
app.listen(port, async() => {
  console.log(`Listening on port: ${port}`); 
});

async function ScheduleInterval(time, amount, filename) {

    let lapcount = 0;

    console.log("Scheduling on Interval started.");

    const job = schedule.scheduleJob(`${secondsToSecondsAndMinutesCron(time)} * * * *`, async function(fireDate){
        lapcount++;
        CallApiWithSubjects("Max Verstappen,Red Bull,Imola,Formula 1", filename + "_allTopics", lapcount, fireDate);
        CallApiWithSubjects("Max Verstappen,Red Bull", filename + "_maxOnly", lapcount, fireDate);
        console.log('This job was ran at ' + fireDate);
        if(lapcount == amount){
          job.cancel();
          console.log("Scheduling on Interval ended.");
        }
      });
  }

  function secondsToSecondsAndMinutesCron(value) {
    const sec = parseInt(value, 10); // convert value to number if it's string
    let hours   = Math.floor(sec / 3600); // get hours
    let minutes = Math.floor((sec - (hours * 3600)) / 60); // get minutes
    let seconds = sec - (hours * 3600) - (minutes * 60); //  get seconds
    return `${seconds > 0 ? ("*/" + seconds) : ("")} ${minutes > 0 ? ("*/" + minutes) : ("*")}`;
}

async function CallApiWithSubjects(subjects,filename, lapcount, fireDate) {
//"Max Verstappen"OR"Red Bull"OR"Imola"OR"Formula 1"
  await axios.get(`https://api.social-searcher.com/v2/search?q=${subjectsToQuery(subjects)}&network=twitter,facebook,reddit&limit=50&key=${process.env.user_key}&fields=sentiment,network,type,lang`)
  .then(res => {
//Save the API response
    fs.appendFile(`data/${filename}.txt`, `Lap ${lapcount} time: ${fireDate} \n 
Topics: ${subjects}
Positive: ${res.data?.posts.filter(x => x.sentiment == 'positive').length} 
Neutral: ${res.data?.posts.filter(x => x.sentiment == "neutral").length}
Negative: ${res.data?.posts.filter(x => x.sentiment == "negative").length}    \n\n`, function (err) {
      if (err) return console.log(err);
      console.log(`Sucessfully wrote to file: ${filename}, API success`);
    });
//Also save the RAW response of the API
    fs.appendFile(`data/RAW_${filename}.txt`, `Lap ${lapcount} time: ${fireDate} \n 
${JSON.stringify(res.data)}    \n\n`, function (err) {
                if (err) return console.log(err);
                console.log(`Sucessfully wrote to file: RAW_${filename}, API success`);
              });
  })
  .catch(err => {console.log(err);
//Still write to file but state something went wrong
    fs.appendFile(`data/${filename}.txt`, `Lap ${lapcount} time: ${fireDate} \nSomething went wrong with the API call. No data available \n\n`, function (err) {
      if (err) return console.log(err);
      console.log(`Sucessfully wrote to file: ${filename}, API failed`);
    });
    fs.appendFile(`data/RAW_${filename}.txt`, `Lap ${lapcount} time: ${fireDate} \nSomething went wrong with the API call. No data available \n\n`, function (err) {
      if (err) return console.log(err);
      console.log(`Sucessfully wrote to file: RAW_${filename}, API failed`);
    });
  });
}

function subjectsToQuery(subjects) {
  const splittedSubjects = subjects.split(',');
  let queryString = "";
  let subjectCount = 0;
  splittedSubjects.forEach(subject => {
    subjectCount++;

    if(subjectCount == splittedSubjects.length)
    {
      queryString += `"${subject}"`;
    }
    else {
      queryString += `"${subject}"OR`;
    }
  });

  return queryString;
}
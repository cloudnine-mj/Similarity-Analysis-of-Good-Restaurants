const express = require('express')
const app = express()
const sqlite3 = require('sqlite3').verbose();
const iconov = require("iconv-lite");
const { spawn } = require('child_process');
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.set('view engine', 'pug');
// css가 읽히지 않는 문제 해결
app.use(express.static(__dirname));

app.get('/', function (req, res) {
  res.render('index', { title: 'Hey', message: 'Hello there!'});
  });

app.post('/', (req, res, next) => {
    var pyData = spawn('python', ['py/ML.py',req.body.restaurant]);
    pyData.stdin.setEncoding = 'utf-8';
    pyData.stdout.on('data', function(data) { 
      var  contents  = iconov.decode(data,"EUC-KR").toString();
      var  arr1 = contents.replace(/'/gi, "");
      var  arr2 = arr1.replace(/,/gi, "");
      var  arr3 = arr2.replace(/]/gi, "");
      var  arr_res = arr3.split(" ");
      console.log(arr_res);
      res.render('res',{
       name1: arr_res[6],
       name2: arr_res[12],
       name3: arr_res[18],
       name4: arr_res[24],
       name5: arr_res[30],
       star1: arr_res[8],
       star2: arr_res[14],
       star3: arr_res[20],
       star4: arr_res[26],
       star5: arr_res[32],
       review1:arr_res[9],
       review2:arr_res[15],
       review3:arr_res[21],
       review4:arr_res[27],
       review5:arr_res[33],
       blog1:arr_res[10],
       blog2:arr_res[16],
       blog3:arr_res[22],
       blog4:arr_res[28],
       blog5:arr_res[34]
      });
     });
});

app.listen(4000, () => console.log('Application listening on port 4000!'))











  // open the database
    // let db = new sqlite3.Database('./restaurant.db');
    // let sql = `SELECT Name,star,review,blog 
    //  FROM restaurant`;

    // db.all(sql, [], (err, rows) => {
    // if (err) {
    //     throw err;
    // }
    // rows.forEach((row) => {
    //     console.log(row);
    // });
    // });
    // db.close();
'use strict';

//get the apikey from config.js
import 'config.js';

var druglist = [];
var devlist = [];

function displayHomepage()
{
    //get the latest medical news in the US through the newsapi
    var url = "http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=" + apikey;

    $.get(url, function( data ) {
        //display only the first 3 news items
        for (var i=0; i<3; i++)
        {
          $('#results').append(`<br>Author: ${data.articles[i]['author']}`);
          $('#results').append(`<br>Published At: ${data.articles[i]['publishedAt']}`);
          $('#results').append(`<br>Title: ${data.articles[i]['title']}`);
          $('#results').append(`<br><a href="${data.articles[i]['url']}">${data.articles[i]['description']}</a>`);
          $('#results').append(`<br><img src="${data.articles[i]['urlToImage']}">`);
        }
    })
    .fail(function() {
        $('#results').append(`<br><b><i>Error!</i></b>`);
      });

    //get the data for the graphs - recall enforcement reports for the last 10 years
    var d = new Date();                   //current date
    var current_year = d.getFullYear();   //get the current year
    var year = current_year - 10;         //search for the last 10 years
    var labels = [];

    for (var i = 0; i < 10; i++)
    {
      url = "https://api.fda.gov/drug/enforcement.json?search=report_date:[" + String(year) + "0101+TO+" + String(year) + "1231]&limit=1";
      $.get(url, function(data) {
        $("#drugs").append(`${data.meta.results.total}-`); 
      })
      .fail(function() {
        $("#drugs").append(`0-`); 
      });

      url = "https://api.fda.gov/device/enforcement.json?search=report_date:[" + String(year) + "0101+TO+" + String(year) + "1231]&limit=1";
      $.get(url, function(data) {
        $("#devs").append(`${data.meta.results.total}-`); 
      })
      .fail(function() {
        $("#devs").append(`0-`); 
      });
      labels[i] = year;
      year++;
    }

    new Chart(
      $('#drug-chart'),
      {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              data: [0,0,434,1377,1562,2021,1255,1073,1448,2183]
            }
          ]
        }
      }
    );
}
$(document).ready( displayHomepage );
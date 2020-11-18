'use strict';

const e = React.createElement;

class LikeButton extends React.Component 
{
    constructor(props) {
      super(props);
      this.state = { liked: false };
    }
  
    render() {
      if (this.state.liked) {
        return 'You liked this.';
      }
  
      return e(
        'button',
        { onClick: () => this.setState({ liked: true }) },
        'Like'
      );
    }
  }

function displayHomepage(jQuery)
{
    //get the latest medical news in the US through the newsapi
    var url = "http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=209a021c63b640db9763409e0fd96f38";
    const domContainer = document.querySelector('#results');
    $.get(url, function( data ) {
        console.log(data);
        //display only the first 5 news items
        var news_text = "<table>";
        for (var i=0; i<5; i++)
        {
            news_text = news_text + "<tr><td>Author: " + data.articles[i]['author'] + 
                "<br> Published At: " + data.articles[i]['publishedAt'] +
                "<br> Title: " + data.articles[i]['title'] +
                "<br><a href='" + data.articles[i]['url'] + "'>" + data.articles[i]['description'] + "</a></td>";
            news_text = news_text + "<td><img src='" + data.articles[i]['urlToImage'] + "'></td></tr>";
        }
        news_text = news_text + "</table>";
        ReactDOM.render(news_text, domContainer);

    })
    .fail(function() {
        $('#results').append(`<br><b><i>Error!</i></b>`);
      });
}
$(document).ready( displayHomepage );
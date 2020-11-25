'use strict';

function api_call(URL, proddesc)
{
    $.get(URL, function( data ) {

        $('#results').append(`<br><b><i> ${proddesc} </i></b>`);
            $('#results').append(`<br>Product Description: ${data.results[0]['product_description']}`);
            $('#results').append(`<br>Reason for recall:<i><b><span style="background-color: #ff8e3c"> ${data.results[0]['reason_for_recall']} </span></b></i>`);
            $('#results').append(`<br>Classification: ${data.results[0]['classification']}`);
        
            //display dates in the mm/dd/yyyy format
            var r_date = data.results[0]['recall_initiation_date'];
            r_date = r_date.substring(4,6) +'/' + r_date.substring(6,8) + '/' + r_date.substring(0,4);
            $('#results').append(`<br>Recall Initiation Date: ${r_date}`);
            
            var t_date = data.results[0]['termination_date'];
            //check if there is a termination date
            if (t_date)
                t_date = t_date.substring(4,6) +'/' + t_date.substring(6,8) + '/' + t_date.substring(0,4);
            else
                t_date = "";
            $('#results').append(`<br>Termination Date: ${t_date}`);
            $('#results').append(`<br>Voluntary Mandated: ${data.results[0]['voluntary_mandated']}`);
            $('#results').append(`<br>Status: ${data.results[0]['status']}`);
            $('#results').append(`<br>------------------------------------------------------------------`);
            //enable the email button
            $('#emailthis').prop('disabled', false);
    })
    .fail(function() {
        $('#results').append(`<br><b><i> ${proddesc} </i></b>`);
        $('#results').append(`<br><b><i>No results found at this time.</i></b>`);
        $('#results').append(`<br>------------------------------------------------------------------`);
      });
}
function apiQueryResults(evt) 
{
    evt.preventDefault();
    // get the users selection
    var qstr = $('#ddlist :selected').text().split("~");
    var qtype = $("input[name='qtype']:checked").val();
    var dname = $("#dname").val();
    
    $( "#results" ).empty();
    // build the query
    if (dname.length > 0 && (qtype == 'drug' || qtype == 'device'))
    {
        URL = 'https://api.fda.gov/' + qtype + '/enforcement.json?search=product_description:'+ dname + '&limit=1';
        api_call(URL, dname);
    }
    else if (qstr == "All")
    {
        var arr = new Array();
        $('#ddlist option').each(function(){
        arr.push($(this).text());
        });
        for (let i=1; i<arr.length; i++)
        {
            let tempstr = arr[i].split("~");
            URL = 'https://api.fda.gov/' + tempstr[0] + '/enforcement.json?search=product_description:'+ tempstr[1] + '&limit=1';
            api_call(URL, tempstr[1]);
        }
    }
    else
    {
        URL = 'https://api.fda.gov/' + qstr[0] + '/enforcement.json?search=product_description:'+ qstr[1] + '&limit=1';
        api_call(URL, qstr[1]);
    }
}   
$('#search').on('click', apiQueryResults);

function sendEmail(evt) 
{
    evt.preventDefault();

    
    let user_email = $("#useremail").text();
    let subject = "From MedAlert!";

    //get the text from #results on the page
    //note: the body is limited to 2000 chars
    var d = new Date(); // add the current date to the email body
    var email_body = d + "\n";    
    var body = $("#results").html();
    body = body.replace(/<br>/g, "\n");
    email_body = email_body + body;

    let mailurl = "mailto:" + user_email + ",?subject=" + encodeURIComponent(subject) + "&body="  + encodeURIComponent(email_body);;
    window.open(mailurl);
}
$("#emailthis").on("click", sendEmail);
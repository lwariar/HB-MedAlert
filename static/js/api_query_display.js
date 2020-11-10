'use strict';

function apiQueryResults(evt) 
{
    evt.preventDefault();

    // get the users selection
    var qstr = $('#ddlist :selected').text().split("~");
    // build the query
    URL = 'https://api.fda.gov/' + qstr[0] + '/enforcement.json?search=product_description:'+ qstr[1] + '&limit=1';
    
    //var email_body;

    $.get(URL, function( data ) {
        
        $('#results').append(`<br>Product Description: ${data.results[0]['product_description']}`);
        $('#results').append(`<br>Reason for recall:<i><b> ${data.results[0]['reason_for_recall']} </b></i>`);
        $('#results').append(`<br>Classification: ${data.results[0]['classification']}`);
        
        //display dates in the mm/dd/yyyy format
        var r_date = data.results[0]['recall_initiation_date'];
        r_date = r_date.substring(4,6) +'/' + r_date.substring(6,8) + '/' + r_date.substring(0,4);
        $('#results').append(`<br>Recall Initiation Date: ${r_date}`);
        var t_date = data.results[0]['termination_date'];
        t_date = t_date.substring(4,6) +'/' + t_date.substring(6,8) + '/' + t_date.substring(0,4);

        $('#results').append(`<br>Termination Date: ${t_date}`);
        $('#results').append(`<br>Voluntary Mandated: ${data.results[0]['voluntary_mandated']}`);
        $('#results').append(`<br>Status: ${data.results[0]['status']}`);

        //email_body = "Product Description: " + data.results[0]['product_description'] +
        //        "Reason for recall: " + data.results[0]['reason_for_recall'];
    });

    //let subject = "From MedAlert!";    
    //let mailurl = "mailto:lakshmiwariar@hotmail.com,?subject=" + subject + "&body="  + email_body;
    //window.open(mailurl);
}
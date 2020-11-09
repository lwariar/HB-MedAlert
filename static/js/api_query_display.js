'use strict';

function apiQueryResults(evt) 
{
    evt.preventDefault();

    URL = 'https://api.fda.gov/drug/enforcement.json?search=product_description:RANITIDINE&limit=1';

    //var email_body;

    $.get(URL, function( data ) {
        $('#results').append(`<br>Product Description: ${data.results[0]['product_description']}`);
        $('#results').append(`<br>Reason for recall: ${data.results[0]['reason_for_recall']}`);
        $('#results').append(`<br>Recall Initiation Date: ${data.results[0]['recall_initiation_date']}`);
        $('#results').append(`<br>Termination Date: ${data.results[0]['termination_date']}`);
        $('#results').append(`<br>Voluntary Mandated: ${data.results[0]['voluntary_mandated']}`);
        $('#results').append(`<br>Status: ${data.results[0]['status']}`);

        //email_body = "Product Description: " + data.results[0]['product_description'] +
        //        "Reason for recall: " + data.results[0]['reason_for_recall'];
    });

    //let subject = "From MedAlert!";    
    //let mailurl = "mailto:lakshmiwariar@hotmail.com,?subject=" + subject + "&body="  + email_body;
    //window.open(mailurl);
}
$('#search').on('click', apiQueryResults);
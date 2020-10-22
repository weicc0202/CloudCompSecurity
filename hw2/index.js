'use strict';
console.log('Loading hello world function');
 
exports.handler = async (event) => {
    let name = "you";
    let city = 'World';
    let time = 'day';
    let day = '';
    let responseCode = 200;
    console.log("request: " + JSON.stringify(event));
    
    // if (event.queryStringParameters && event.queryStringParameters.name) {
    //     console.log("Received name: " + event.queryStringParameters.name);
    //     name = event.queryStringParameters.name;
    // }
    
    // if (event.queryStringParameters && event.queryStringParameters.city) {
    //     console.log("Received city: " + event.queryStringParameters.city);
    //     city = event.queryStringParameters.city;
    // }
    
    if (event.body) {
        let body = JSON.parse(event.body)
        if (body.name) {
            console.log("Received name: " + body.name);
            name = body.name;
        }
        
        if (body.city) {
            console.log("Received city: " + body.city);
            city = body.city;
        }
    }
 
    var currentTime=new Date();
    let greeting = "";
//getHour() function will retrieve the hour from current time
    if(currentTime.getHours()<12)
        greeting = `Good Morning, ${name} of ${city}.`;
    else if(currentTime.getHours()<17)
        greeting = `Good Afternoon, ${name} of ${city}.`;
    else if(currentTime.getHours()<21)
        greeting = `Good Evening, ${name} of ${city}.`;
    else
        greeting = `Good Night, ${name} of ${city}.`;


    var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var images = ['https://i.imgur.com/4AiXzf8.jpeg','https://i.imgur.com/oPR4BiX.jpg',
                'https://i.imgur.com/Q6pAkWl.png', 'https://i.imgur.com/mQOnf6a.png',
                'https://i.imgur.com/frzJxbbb.jpg', 'https://i.imgur.com/4ZSOnSYb.jpg',
                'https://i.imgur.com/AuhIXtwb.jpg'];
    var imageUrl = images[currentTime.getDay()];
    day = days[ currentTime.getDay() ];
    greeting += ` Happy ${day}!`;
    
    let responseBody = {
        message: greeting,
        imageurl: imageUrl,
        input: event
    };
    
    // The output from a Lambda proxy integration must be 
    // in the following JSON object. The 'headers' property 
    // is for custom response headers in addition to standard 
    // ones. The 'body' property  must be a JSON string. For 
    // base64-encoded payload, you must also set the 'isBase64Encoded'
    // property to 'true'.
    let response = {
        statusCode: responseCode,
        headers: {
             "Access-Control-Allow-Headers" : "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*"
        },
        body: JSON.stringify(responseBody)
    };
    console.log("response: " + JSON.stringify(response))
    return response;
};
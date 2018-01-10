'use strict';

const AWS = require("aws-sdk");
const docClient = new AWS.DynamoDB.DocumentClient();
AWS.config.update({
  region: "us-west-2",
});


module.exports.space = (event, context, callback) => {

  let today = new Date();
  let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

  const table = "Space";

  const params = {
      TableName: table,
      Limit:20,
      FilterExpression:"#Location = :loc",
      ExpressionAttributeNames: {
          "#Location": "Location"
      },
      ExpressionAttributeValues: {
          ":loc" : event.queryStringParameters.locat
      }
  };

  docClient.scan(params, function (err, data) {
    if (err) {
      console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
      callback('[400] Bad Request: ' + JSON.stringify(err, null, 2));
    }
    else {
      console.log("Scan succeeded:", JSON.stringify(data, null, 2));
      const response = {
        statusCode: 200,
        body: JSON.stringify(data, null ,2),
      };
      callback(null, response);
    }
  });
};

module.exports.search = (event, context, callback) => {
    //const table = "carReport";

    const params = {
        TableName: "carReport",
        Limit:3,
        KeyConditionExpression:"#Lic = :LicValue and #time BETWEEN :from AND :to",
        ExpressionAttributeNames: {
            "#Lic":"License",
            "#time":"Time"
        },
        ExpressionAttributeValues: {
            ":LicValue": event.queryStringParameters.lic,
            ":from": "00:00:00" ,
            ":to": "23:59:59"
        },
        ScanIndexForward: false,
    };

    docClient.query(params, function (err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 4));
            callback('[400] Bad Request: ' + JSON.stringify(err, null, 4));
        } else {
            console.log("Scan succeeded:", JSON.stringify(data, null, 4));
            const response = {
                statusCode: 200,
                body: JSON.stringify(data, null ,4),
            };
            callback(null, response);
        }
    });
};

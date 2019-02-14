'use strict';

const elasticsearch = require('elasticsearch');


const esurl = "https://vpc-corp-jenkins-sqtj236u2noi6heyarotq74nv4.us-east-1.es.amazonaws.com"
const client = new elasticsearch.Client({
  host: esurl,
  log: 'trace'
})

const handler = (event, context) => {
  const time = new Date();
  console.log(`Your cron function "${context.functionName}" ran at ${time}`);

  client.cat.indices({h:["index"], s: ["index"]}).then((body) => {
    let indices = body.split("\n")
    let buildIndices = indices.filter((x) => x.startsWith("builds-"))
    let metricsIndices = indices.filter((x) => x.startsWith("metrics-"))
    let nodesIndices = indices.filter((x) => x.startsWith("nodes-"))

    
    const buildIndexKeep = buildIndices.pop()
    const metricsIndexKeep = metricsIndices.pop()
    const nodesIndexKeep = nodesIndices.pop()

    console.log("Indices to keep")
    console.log(buildIndexKeep, metricsIndexKeep, nodesIndexKeep)

    let allIndices = []
    allIndices = allIndices.concat(buildIndices)
    allIndices = allIndices.concat(metricsIndices)
    allIndices = allIndices.concat(nodesIndices)

    // client.indices.delete({
    //   index: allIndices
    // }).then(() => {
    //   console.log("done")
    // })
  })
};


module.exports.run = handler;
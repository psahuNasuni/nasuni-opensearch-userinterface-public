var data;
var result=[];
var volumes = [];
var services = [];
var rowIndex = 0;
var source;
var serviceName
var serviceList = ["ES","OS","KENDRA"]
var schedulerName = "kendra-tracker-ui"
var trackerDoc

function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//usage:
function trackerStart(){
    console.log(serviceList.length)
    for(i=0;i<serviceList.length;i++){
        serviceName=serviceList[i]
        console.log(serviceName)
        trackerDoc = schedulerName+"_tracker_"+serviceName+".json"
        readTextFile(trackerDoc, function(text){
            data = JSON.parse(text);
            console.log(data)
            result = Object.keys(data).map((key) => [Number(key), data[key]]);
            console.log(data.INTEGRATIONS);
            dataArr = result[0][1];
            console.log(dataArr)
            volumes = Object.keys(result[0][1])
            console.log(volumes)
            tableAppend(result,volumes);
        
        })
    }
}

function tableAppend(result,volumes) {
    console.log(result.length)
        volumes = Object.keys(result[0][1])
        volumes = [...new Set(volumes)]
        source = Object.values(result[0][1])
        console.log(source)
        // for(pair=0;pair<dataArr.length;pair++){}
        for(i=0;i<volumes.length;i++){
            var tbodyRef = document.getElementById("dataTable").getElementsByTagName("tbody")[0];
            var newRow = tbodyRef.insertRow();
            for(j=0;j<4;j++){
                var newCell = newRow.insertCell();
                
                if(j==1){
                    
                    var listServices = document.createTextNode(source[i]._source.service);
                    newCell.appendChild(listServices);
                } else if(j==2){
                    var listStatus = document.createTextNode(source[i]._NAC_activity.current_state);
                    newCell.appendChild(listStatus);
                } else if(j==3){
                    var listSchedule = document.createTextNode(source[i]._source.frequency);
                    newCell.appendChild(listSchedule);
                }else{
                    var a = document.createElement('a');
                    let button = document.createElement('button');
                    var link = document.createTextNode(source[i]._source.volume);
                    a.setAttribute("id","anchor");
                    button.appendChild(a)
                    a.appendChild(link)

                    if(source[i]._source.service==="KENDRA" || source[i]._source.service==="kendra"){
                        a.href=source[i]._source.kendra_url
                    }else if(source[i]._source.service==="ES" || source[i]._source.service==="OS"){
                        a.href=source[i]._source.default_url+"?q="+source[i]._source.volume
                    }
                
                    a.target = "_blank"
                    newCell.appendChild(a);
                }
                
            }
            
           

        }


    }
    
    
    




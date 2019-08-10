// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
function dash(data){
  var pusher = new Pusher('e3412dad9232d73e7e37', {
    cluster: 'mt1',
    encrypted: true
  });
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';
    var date = new Date();
    console.log(data);
     // messages

     if(data === 'messages') {
      update = document.getElementById("lstUpdate") 
      update.innerText = `Last actualitation: ${date.getFullYear()}/${date.getMonth()}/${date.getDay()} ${date.getHours()} ${date.getMinutes()} ${date.getSeconds()}`;    
      document.getElementById("messages").style.display = "";
      document.getElementById("sales").style.display = "none";
      document.getElementById("orders").style.display = "none";
      document.getElementById("marketing").style.display = "none";
       
    $.get("/selMessage", { dataType: 'json' }, 
    function( data, sucess ) {
      console.log(data);

      var countHappy = 0;
      var countNeutral = 0;
      var countBad = 0;
      
      for(var i = 0; i < data.length; ++i) {
        if(data[i][3] == 'Good') {
          countHappy++;
        }
        if(data[i][3] == 'Neutral') {
          countNeutral++;
        }
        if(data[i][3] == 'Bad') {
          countBad++;
        }
      }
      fields = [countHappy, countNeutral, countBad]
      console.log(fields)
      var happy = document.getElementById("noHappy") 
      var neutral = document.getElementById("noNeutral") 
      var bad = document.getElementById("noSad") 
      var total = document.getElementById("message-count")  

      happy.innerText = `${countHappy}`;
      neutral.innerText =  `${countNeutral}`;
      bad.innerText = `${countBad}`;    
      total.innerText = `${countBad + countHappy + countNeutral }`;    
      
      var ctxPI = document.getElementById("myPieChartInc").getContext('2d');
      var myPieChartPI = new Chart(ctxPI, {
        type: 'doughnut',
        data: {
          labels: ["Happy", "Neutral", "Sad"],
          datasets: [{
            data: fields,
            backgroundColor: ["#46BFBD", "#FDB45C", "#F7464A" ],
            hoverBackgroundColor: ["#5AD3D1", "#FFC870", "#FF5A5E" ]
          }]
        },
        options: {
        responsive: true
        }
    });
    var dataTable = $("#dataTableMessage").DataTable()
    
    for(var i = 0; i < data.length; ++i) {
      var icon = ''
      if(data[i][3] == 'Good') {
        icon = `<td align="center"><button type="button" class="btn btn-success"><i class="fa fa-smile-o"></i></button></td>`
      }
      if(data[i][3] == 'Neutral') {
        icon = `<td align="center"><button type="button" class="btn btn-warning"><i class="fa fa-meh-o"></i></button></td>`
      }
      if(data[i][3] == 'Bad') {
        icon = `<td align="center"><button type="button" class="btn btn-danger"><i class="fa fa-frown-o"></i></button></td>`
      }
      dataTable.row.add([
        data[i][0],
        data[i][1],
        data[i][2],
        icon,
      `${date.getFullYear()}/${date.getMonth()}/${date.getDay() - 1}`,
        data[i][4]
      ]).draw( false );	      
    }

    // Listen to 'message sent' event
    var messageChannel = pusher.subscribe('message');
    messageChannel.bind('send', function(data) {
      var message = document.getElementById('message-count')
    
      var date = new Date();
      var toAppend = document.createElement('a')
      toAppend.classList.add('list-group-item', 'list-group-item-action')
      toAppend.href = '#'
      document.getElementById('message-box').appendChild(toAppend)
      toAppend.innerHTML ='<div class="media">'+
                      '<img class="d-flex mr-3 rounded-circle" src="http://placehold.it/45x45" alt="">'+
                      '<div class="media-body">'+
                        `<strong>${data.name}</strong> posted a new message `+
                        `<em>${data.message}</em>.`+
                        `<div class="text-muted smaller">Today at ${date.getHours()} : ${date.getMinutes()}</div>`+
                      '</div>'+
                    '</div>'
      message.innerText = parseInt(message.innerText)+1
     
      var dataTable = $("#dataTableMessage").DataTable()
    
      var icon = ''
      var indice = 0
      if(data.clasificacion == 'Good') {
        indice = 0
        happy.innerText = parseInt(happy.innerText) + 1
        icon = `<td align="center"><button type="button" class="btn btn-success"><i class="fa fa-smile-o"></i></button></td>`
      }
      if(data.clasificacion == 'Neutral') {
        indice = 1
        neutral.innerText = parseInt(neutral.innerText) + 1
        icon = `<td align="center"><button type="button" class="btn btn-warning"><i class="fa fa-meh-o"></i></button></td>`
      }
      if(data.clasificacion == 'Bad') {
        indice = 2
        icon = `<td align="center"><button type="button" class="btn btn-danger"><i class="fa fa-frown-o"></i></button></td>`
        bad.innerText = parseInt(bad.innerText) + 1
      }
      
      myPieChartPI.data.datasets.forEach((dataset) => {
        dataset.data.fill(dataset.data[indice] + 1, indice, indice + 1);
      });
      myPieChartPI.update();
    
      dataTable.row.add([
        '#',
        data.name,
        data.message,
        icon,
        `${date.getFullYear()}/${date.getMonth()}/${date.getDay() - 1}`,
        data.telefono
      ]).draw( false );	       
    });
    });
    }
    if(data === 'sales') {
      update = document.getElementById("lstUpdate") 
      update.innerText = `Last actualitation: ${date.getFullYear()}/${date.getMonth()}/${date.getDay()} ${date.getHours()} ${date.getMinutes()} ${date.getSeconds()}`;    
      document.getElementById("messages").style.display = "none";
      document.getElementById("sales").style.display = "";
      document.getElementById("orders").style.display = "none";
      document.getElementById("marketing").style.display = "none";

      // -- Bar Chart Example
      var ctx = document.getElementById("myBarChart");
      var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        datasets: [{
        label: "Revenue",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: [5312, 6251, 7841, 6821, 7984, 1012],
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'week'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });

// Subscribe to poll trigger
var orderChannel = pusher.subscribe('order');
// Listen to 'order placed' event
orderChannel.bind('place', function(data) {
  myLineChart.data.datasets.forEach((dataset) => {
    dataset.data.fill(dataset.data[d.getDay() - 1] + parseInt(data.units), d.getDay() - 1, d.getDay());
  });

  myLineChart.update();
});

var customerChannel = pusher.subscribe('order');
customerChannel.bind('details', function(data) {
  var dataTable = $("#dataTable").DataTable()

var date = new Date();
dataTable.row.add([
    data.noTicket,
    data.cliente,
    data.cantidad,
    data.descripcion,
  data.importe,
  `${date.getFullYear()}/${date.getMonth()}/${date.getDay()}`,
  `<td><button type="button" class="btn btn-success"><i class="fa fa-whatsapp"></i></button></td>`
  ]).draw( false );	
});


    }

    if(data === 'orders') {
      update = document.getElementById("lstUpdate") 
      update.innerText = `Last actualitation: ${date.getFullYear()}/${date.getMonth()}/${date.getDay()} ${date.getHours()} ${date.getMinutes()} ${date.getSeconds()}`;    
      document.getElementById("messages").style.display = "none";
      document.getElementById("sales").style.display = "none";
      document.getElementById("orders").style.display = "";
      document.getElementById("marketing").style.display = "none";

      var ctxL = document.getElementById("myBarChartFi").getContext('2d');
      var myLineChart = new Chart(ctxL, {
        type: 'line',
        data: {
        labels: ["January", "February", "March", "April", "May", "June", "July", "August"],
        datasets: [{
          label: "RESTAURANT",
          data: [40101, 32986, 35034, 37841, 36202, 38201, 37921, 10121],
          backgroundColor: [
            'rgba(105, 0, 132, .2)',
          ],
          borderColor: [
            'rgba(200, 99, 132, .7)',
          ],
          borderWidth: 2
        },
        {
          label: "ONLINE",
          data: [4001, 3986, 3534, 2781, 3202, 3820, 3721, 1121],
          backgroundColor: [
            'rgba(0, 137, 132, .2)',
          ],
          borderColor: [
            'rgba(0, 10, 130, .7)',
          ],
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true
    }
  });




    }

    if(data === 'marketing') {
      update = document.getElementById("lstUpdate") 
      update.innerText = `Last actualitation: ${date.getFullYear()}/${date.getMonth()}/${date.getDay()} ${date.getHours()} ${date.getMinutes()} ${date.getSeconds()}`;    
      document.getElementById("messages").style.display = "none";
      document.getElementById("sales").style.display = "none";
      document.getElementById("orders").style.display = "none";
      document.getElementById("marketing").style.display = "";

      // -- Bar Chart Example
      var ctxP = document.getElementById("myPieChart").getContext('2d');
      var myPieChart = new Chart(ctxP, {
        type: 'pie',
        data: {
        labels: ["PANINI", "RED BULL", "FRENCH FRIES", "POUTINE", "SHAKE"],
          datasets: [{
          data: [822, 420, 121, 212, 112],
          backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
          hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
        }]
      },
      options: {
        responsive: true
      }
      });
    
      
    }
}

function sendWhats(name) {
  console.log('s');
  $.get( "/sendWhats", { name: name } )
  .done(function( data ) {
    alert( "Send Marketing: " );
  });
}

dash('messages');
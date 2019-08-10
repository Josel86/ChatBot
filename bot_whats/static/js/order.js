// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var d = new Date();

Pusher.logToConsole = true;

// Configure Pusher instance


// Subscribe to poll trigger
//var orderChannel = pusher.subscribe('order');

// Listen to 'order placed' event
//var order = document.getElementById('order-count')
//orderChannel.bind('place', function(data) {
//  myLineChart.data.datasets.forEach((dataset) => {
//    dataset.data.fill(dataset.data[d.getDay() - 1] + parseInt(data.units), d.getDay() - 1, d.getDay());
//  });
//  order.innerText = parseInt(order.innerText)+1
//});

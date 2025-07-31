const socket = io();

socket.on('sensor_data', function(data) {
    document.getElementById('x').innerText = data.x.toFixed(2);
    document.getElementById('y').innerText = data.y.toFixed(2);
    document.getElementById('z').innerText = data.z.toFixed(2);
})
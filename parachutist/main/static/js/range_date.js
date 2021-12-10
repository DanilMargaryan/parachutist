var arrival = document.getElementById("id_start_date")
var departure = document.getElementById("id_end_date")


function onChangeDate()
{
    departure.min=arrival.value
    arrival.max=departure.value
}


function padLeadingZeros(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}


var currentDate = new Date()
arrival.min=`${currentDate.getFullYear()}-${padLeadingZeros(currentDate.getMonth() + 1, 2)}-${padLeadingZeros(currentDate.getDate(), 2)}`

arrival.addEventListener('change', onChangeDate)
departure.addEventListener('change', onChangeDate)
onChangeDate()

var arrival = document.getElementById("arrival")
var departure = document.getElementById("departure")
var nights = document.getElementById("nights")
function onChangeDate(){
    departure.min=arrival.value
    arrival.max=departure.value
    
    if (arrival.value=="" || departure.value=="")
        return
    console.log(arrival.value)
    var arrivalDate=Date.parse(arrival.value)
    var departureDate=Date.parse(departure.value)

    const diffTime = Math.abs(departureDate - arrivalDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    nights.innerText= "Всего ночей: " + diffDays
}
function padLeadingZeros(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}
var currentDate = new Date()
arrival.min=`${currentDate.getFullYear()}-${padLeadingZeros(currentDate.getMonth() + 1, 2)}-${padLeadingZeros(currentDate.getDate(), 2)}`
console.log(arrival.min)

arrival.addEventListener('change',onChangeDate)
departure.addEventListener('change',onChangeDate)
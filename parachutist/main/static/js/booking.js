var arrival = document.getElementById("id_start_date")
var departure = document.getElementById("id_end_date")
var nights = document.getElementById("nights")
var rangeDateFormId = document.getElementById("RangeDateFormId")


function onChangeDate(){
    rangeDateFormId.submit()
    ShowNights();
}


function ShowNights()
{
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


$(function(){

    $('.rooms__slider').slick({
        arrows: false,
        dots:  true,
        // autoplay: true,
        // autoplaySpeed: 5000,
        speed: 900,
        fade: true
    });
});


var currentDate = new Date()
arrival.min=`${currentDate.getFullYear()}-${padLeadingZeros(currentDate.getMonth() + 1, 2)}-${padLeadingZeros(currentDate.getDate(), 2)}`
console.log(arrival.min)

arrival.addEventListener('change',onChangeDate)
departure.addEventListener('change',onChangeDate)
ShowNights()
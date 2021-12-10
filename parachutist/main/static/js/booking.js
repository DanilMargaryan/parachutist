var arrival = document.getElementById("id_start_date")
var departure = document.getElementById("id_end_date")
var nights = document.getElementById("nights")
var rangeDateFormId = document.getElementById("RangeDateFormId")
var FinalPrice = document.getElementById("FinalPrice")

var roomsSelected = {}

function onChangeDate(){
    rangeDateFormId.submit()
    ShowNights();
}

var diffDays

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
    diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

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


function ContinueOrder() {
    post({
        'rooms': JSON.stringify(roomsSelected),
    })
}

var Prices = {}

function OnChangeRoomCount(room_type, element, price)
{
    var count = parseInt(element.value)
    if (count == 0) {
        if (roomsSelected[room_type] !== undefined)
            delete roomsSelected[room_type]
    }
    else {
        roomsSelected[room_type] = count
    }
    var sumPrice = 0
    Prices[room_type] = price
    for (const key in roomsSelected) 
    {
        sumPrice += Prices[key] * diffDays * roomsSelected[key]
    }    
    document.getElementById("FinalPrice").innerText = "ИТОГ: "+ sumPrice +"₽"
}

var currentDate = new Date()
arrival.min=`${currentDate.getFullYear()}-${padLeadingZeros(currentDate.getMonth() + 1, 2)}-${padLeadingZeros(currentDate.getDate(), 2)}`
console.log(arrival.min)

arrival.addEventListener('change',onChangeDate)
departure.addEventListener('change',onChangeDate)
ShowNights()


function post(params) {
    const form = rangeDateFormId
  
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = key;
        hiddenField.value = params[key];
  
        form.appendChild(hiddenField);
      }
    }
  
    document.body.appendChild(form);
    form.submit();
  }
  
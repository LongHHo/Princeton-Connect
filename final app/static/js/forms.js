



function displayResults(userNetid, userName, userEmail, userPhone, userDescr, userCity) {
  document.getElementById("entryNetid").innerHTML = userNetid;
  document.getElementById("entryName").innerHTML = userName;
  document.getElementById("entryPhone").innerHTML = userPhone;
  document.getElementById("entryEmail").innerHTML = userEmail;
  document.getElementById("entryDescription").innerHTML = userDescr;
  document.getElementById("entryCity").innerHTML = userCity;
  document.getElementById('NewMessage').style.display='none';
  document.getElementById('entryModal').style.display='block';
}


function closeEntry(){
  document.getElementById("entryModal").style.display = "none";

}

// document.getElementById("submitForm").addEventListener("submit", function(event){
//   event.preventDefault()
//  );



// this is meant to validate the address
// my problem is that geocode is making an asynchronous call so this function finishes before
// geocode is even done. how do i make the function wait for geocode?
function validateForm(form) {
  /* const form = document.getElementById('id01'); */
  var address = document.getElementsByName('address')[0];
  var letters = /^[A-Za-z]+$/;

  if (address.value == ''){
    form.submit();
  }

  // Get geocoder instance



  myPromise = new Promise(function(resolve, reject) {
  var statusCheck;
  var geocoder = new google.maps.Geocoder();
  results = geocoder.geocode({'address': address.value}, function check(results, status){
    if (status !== google.maps.GeocoderStatus.ZERO_RESULTS) {
      resolve('fine');
    } else {
      reject('error');

    }
    
  })
      });
  


  myPromise
    .then(function whenOk(response) {
      form.submit();
      console.log(response);

    })
    .catch(function notOk(err) {
      const addressError = document.querySelector('#address + span.erroraddress')
      addressError.textContent = '  This is an invalid address';



    })

}



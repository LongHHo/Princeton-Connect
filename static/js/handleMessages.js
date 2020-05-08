    
  function send_new_message(){

    var reciever = document.getElementById('msgNetid').value;
    rec = encodeURIComponent(reciever);
    var message = document.getElementById('message').value;

    if (message == '') {
      return;
    }

    
    message = encodeURIComponent(message);

    let url = "/sendMessage?reciever=" + reciever + "&message=" + message

          r = $.ajax(
          {
            type: "GET",
            url: url,
          }
    );
    document.getElementById('NewMessage').style.display='none';
  }

  function openMsgForm() {
    
    document.getElementById('msgNetid').value = document.getElementById('entryNetid').innerHTML;
    document.getElementById('message').value = '';


    document.getElementById('NewMessage').style.display='block';

  } 

  function openMsgBox(netid) {
    
    document.getElementById('msgNetid').value = netid;
    document.getElementById('message').value = '';


    document.getElementById('NewMessage').style.display='block';

  } 
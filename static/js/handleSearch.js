
    var request = null;

function createAjaxRequest()  // From Nixon book
{
    var req;

    try  // Some browser other than Internet Explorer
    {
        req = new XMLHttpRequest();
    }
    catch (e1)
    {
        try  // Internet Explorer 6+
        {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e2)
        {
            try  // Internet Explorer 5
            {
            req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e3)
            {
            req = false;
            }
        }
    }
    return req;
}





function processReadyStateChange()
{
   var STATE_UNINITIALIZED = 0;
   var STATE_LOADING       = 1;
   var STATE_LOADED        = 2;
   var STATE_INTERACTIVE   = 3;
   var STATE_COMPLETED     = 4;

   if (this.readyState != STATE_COMPLETED)
      return;

   if (this.status != 200)         // Request succeeded?
   {
      //alert("AJAX error: Request failed: " +
      //   this.statusText);
      return;
   }

   if (this.responseText == null)  // Data received?
   {
      alert("AJAX error: No data received");
      return;
   }
   var resultsArea = document.getElementById('ResultsArea');
   resultsArea.innerHTML = this.responseText;
}

function getResults()
{
   var name1 = document.getElementById('name1').value;
   var description1 =
      document.getElementById('description1').value;
   var city1 = document.getElementById('city1').value;

   name1 = encodeURIComponent(name1);
   description1 = encodeURIComponent(description1);
   city1 = encodeURIComponent(city1);

   if (request != null)
      request.abort();

   request = createAjaxRequest();
   if (! request)
   {
      alert("AJAX error: Your browser doesn't support AJAX");
      return;
   }

   request.onreadystatechange = processReadyStateChange;

   request.open("POST", "/templates/lookup?" +
      "name1=" + name1 +
      "&description1=" + description1 +
      "&city1=" + city1);
   request.send(null);
}
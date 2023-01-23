$(document).ready(function(){

    $.ajax({
        type: 'GET',
        url: 'user/limits/1',
        success: function(data){
            var resp = data[0]
            limit = resp.limit

            if (limit == 0) {
                $('#companyIdsInput').prop('disabled', true)
                $('#btnGet').prop('disabled', true)
                $(getMessage("You have reached your daily requests limit", "danger")).insertAfter('#pagetitle')
            }
        }
    });


    $("#btnGet").click(function(){
        var companiesId = $("#companyIdsInput").val().split(/\n/);
        var companylist = []
        for (var i = 0; i < companiesId.length; i++){
            if (/\S/.test(companiesId[i])) {
                companylist.push($.trim(companiesId[i]));
            }
        }

        $.ajax({
            type: 'POST',
            url: 'ares/company/bulk',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify({
                companyList: companylist,
            }),
            beforeSend: function() {
                $("#loading").modal('show');
            },
            success: function(data){
                console.log(data.data)
                // clean table by remove previous results
                $('#loading').modal('hide')
                if ($('#results').length){
                    $('#results').remove()
                }
                $('#export').empty()
                $('#res').empty()
                $('#res').append($("<p></p>").text('Requested: ' + data.requested).addClass('mr-2'))
                $('#res').append($("<p></p>").text('Fetched: ' + data.fetched))
                $("#resultTable").append(parseRegisterData(data.data).attr('id', 'results'));
                $("#companyIdsInput").val('')
                $('#export').append($('<button></button>')
                    .text('Export Data')
                    .addClass('btn btn-primary rounded-lg')
                    .attr('id', 'exportData')
                    .on("click", () => {
                        var headings = []
                        var data = []

                        $('#resultTable th').each(function(){
                            headings.push($(this).text())
                        });

                        $('#resultTable td').each(function(){
                            data.push($(this).text())
                        });

                        var CSVString = prepCSVRow(headings, headings.length, '');
                        CSVString = prepCSVRow(data, headings.length, CSVString);


                        var downloadLink = document.createElement("a");
                        var blob = new Blob(["\ufeff", CSVString]);
                        var url = URL.createObjectURL(blob);
                        downloadLink.href = url;
                        downloadLink.download = "data.csv";

                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                    })
                )

                $.ajax({
                    type: 'GET',
                    url: 'user/limits/1',
                    success: function(data){
                        var resp = data[0]
                        limit = resp.limit
                        console.log(data.limit)

                        if (limit == 0) {
                            $('#companyIdsInput').prop('disabled', true)
                            $('#btnGet').prop('disabled', true)
                            $(getMessage("You have reached your daily requests limit", "danger")).insertAfter('#pagetitle')
                        }
                    }
                });

            }
        })


    });

})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}

function parseRegisterData(data) {
    var tbody = $('<tbody />');
    data.map((item) =>{
        var tr = $('<tr />');
        if (item.hasOwnProperty('companyId')){tr.append( $('<td />', {text : item.companyId}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('name')){tr.append( $('<td />', {text : item.name}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('legalFormName')){tr.append( $('<td />', {text : item.legalFormName}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('address')){tr.append( $('<td />', {text : parseAddress(item.address)}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('dateOfIncorporation')){tr.append( $('<td />', {text : item.dateOfIncorporation}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('state')){tr.append( $('<td />', {text : item.state}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('nace')){tr.append( $('<td />', {text : item.nace.code}));} else {tr.append( $('<td />', {text : ''}));}
        if (item.hasOwnProperty('nace')){tr.append( $('<td />', {text : item.nace.name}));} else {tr.append( $('<td />', {text : ''}));}
        tbody.append(tr)
    })

    return tbody
}

function parseAddress(address) {
    var resAddress = ''
    if (address.hasOwnProperty('fullAddress')){
        resAddress += address.fullAddress
    } else {
        if(address.hasOwnProperty('street')){
            resAddress += address.street + ' '
        } else {
            resAddress += address.city + ' '
        }
        if(address.hasOwnProperty('streetNo')){
            resAddress += address.streetNo
        }
        if(address.hasOwnProperty('houseNo')){
            resAddress += '/' + address.houseNo + ', '
        } else {
            if(address.hasOwnProperty('streetHouseNo')){
                resAddress += address.streetHouseNo + ', '
            } else {
                resAddress += ', '
            }
        }
        if(address.hasOwnProperty('zipCode')){
            resAddress += address.zipCode + ' '
        }
        if(address.hasOwnProperty('city')){
            resAddress += address.city
        }
        
        resAddress += ', ' + address.country
    }

    return resAddress
}


function prepCSVRow(arr, columnCount, initial) {
    var row = ''; 
    var delimeter = ';'; 
    var newLine = '\r\n';
  
    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);
    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimeter);
      });
      row += newLine;
    });
    return initial + row;
  }


  function getMessage(text, type){
    var message = 
        '   <div class="messages">' +
        '     <div class="alert alert-sm rounded-sm alert-'+ type +'">' + text + 
        '     </div>' +
        '   </div>';
    
    return message
  }
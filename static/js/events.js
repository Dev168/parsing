function clearTables() {

}
function getIconPath(sport) {
    if(sport == "Football"){
        return "static/img/football24.png";
    }
    if(sport == "Basketball"){
        return "static/img/basketball24.png";
    }
    if(sport == "Baseball"){
        return "static/img/baseball24.png";
    }
    else{
        return "static/img/tennis24.png";
    }
}

function fillTables(data) {

    var iconpath;
    var dataDiv = $("#data");

    data = JSON.parse(data);

    for(var sport in data){
        iconpath = getIconPath(sport);

        var leagues = data[sport];

        for(var league in leagues) {
            var el = dataDiv.append(
            `<table class=\"table table-condensed table-bordered text-center\">
                 <tr>
                     <td colspan=\"12\"  ><img src=` +iconpath+ `>` + league + `</td>
                 </tr>
            </table>`
            );

            var participantsList = leagues[league];
            for(var participants in participantsList) {
                dataDiv.append(
                    `<table class="table table-condensed table-bordered text-center">
                    <tr>
                    <td>` + participants + `</td>
                </tr>
                </table>`
                );

                var moneylines = participantsList[participants]["moneylines"];
                var handicaps = participantsList[participants]["handicaps"];

                var tableMoneyLines = $(`<table class="table table-condensed table-bordered text-center moneylines"></table>`);
                for (var moneyline in moneylines) {
                    moneylineObj = moneylines[moneyline];

                    if(!$.trim($("#time").html())){
                        $("#time").append(moneylineObj["oddsdate"])}

                    tableMoneyLines.append(`
                            <tr>
                                <td>` + moneylineObj["firstwin"] + `</td>
                                <td>` + moneylineObj["draw"] + `</td>
                                <td>` + moneylineObj["secondwin"] + `</td>
                             </tr>
                    `);
                }
                dataDiv.append(tableMoneyLines);

                var tableHandicaps = $(`<table class="table table-condensed table-bordered text-center handicaps"></table>`);
                for (var handicap in handicaps) {
                    handicapObj = handicaps[handicap];
                    tableHandicaps.append(`
                            <tr>
                                <td>` + handicapObj["firstforward"] + `</td>
                                <td>` + handicapObj["firstwin"] + `</td>
                                <td>` + handicapObj["secondforward"] + `</td>
                                <td>` + handicapObj["secondwin"] + `</td>
                             </tr>
                    `);
                }
                dataDiv.append(tableHandicaps);

            }
        }
    }
}


function bookmakerSelectHandler(selectedBookmaker){
    var value = selectedBookmaker.value;
    $("#data table").remove();
    $("#time").empty();
    $.get( "http://localhost/api/events", {"bookmaker": value}, function(data){
        fillTables(data);
    })
}

var bookmakerSelect = $("#bookmakerSelect");


bookmakerSelect.change(function(){
   bookmakerSelectHandler(this);
});

$( document ).ready(function() {
    bookmakerSelect.val(1);
    bookmakerSelectHandler(bookmakerSelect.get(0));
});

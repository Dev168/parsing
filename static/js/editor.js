/**
 * Created by Vlad on 16.07.2016.
 */


// Формирует html для select элемента
function getSelectTag(selectArray) {

    var selectTagHtml = "<option value="+ null + ">" + 'Отсутствует' + "</option>\n";

    $.each(selectArray, function (i, item) {

        selectTagHtml += "<option value="+ item.id + ">" + item.name + "</option>\n"

    });

    return '<select class="form-control">' + selectTagHtml + '</select>'
}

// Заполняет таблицу лигами
function fillTable(data){

    var trHTML = '';
    data = JSON.parse(data);

    var select_tag_html = getSelectTag(data.select);

    $.each(data.matches, function (i, item) {

        trHTML += "<tr class='success'>" +
        "<td class=\"vert-align text-center col-md-6\">" + item.name1 + "</td>" +
        "<td class=\"vert-align text-center col-md-6\">" + select_tag_html + "</td>" +
        "<td style='display: none'>" + item.id1 + "</td>" +
        "<td style='display: none'>" + item.id2 + "</td>" +
        "<td style='display: none'>" + item.uuid + "</td>" +
        "</tr>"

    });

    $.each(data.fix, function (i, item) {

        trHTML += "<tr class='danger'>" +
            "<td class=\"vert-align text-center col-md-6\">" + item.name + "</td>" +
            "<td class=\"vert-align text-center col-md-6\">" + select_tag_html + "</td>" +
            "<td style='display: none'>" + item.id + "</td>" +
            "<td style='display: none'>" + null + "</td>" +
            "<td style='display: none'>" + null + "</td>" +
            "</tr>"

    });

    dataTable.append(trHTML)

    dataTable.find("tr").each(function () {
        var $this = $(this);
        var selId = $this.find("td:nth-child(4)").html();
        $this.find("select").val(selId)
        }
    )

    tableLoading = false;
    $("table select").change(function() {
    matchSelectHandler(this);
    });
    updateVisibility();



}

// Заполняет select лист спортов
function fillSports() {
    $.get( "http://localhost/api/getSportsList", function(data){

        var selectValues = JSON.parse(data);

        $.each(selectValues, function(key, value) {
            sportChoice
                .append($("<option></option>")
                    .attr("value",value.uuid)
                    .text(value.name));
        });

        sportsListLoading = false;
        updateVisibility();
        sportSelectHandler();

    });
}

// Заполняет select лист лиг
function fillLeagues() {
    var el = sportChoice.val();

    $.get( "http://localhost/api/getLeaguesList", {"uuid": el}, function(data){

        var selectValues = JSON.parse(data);

        $.each(selectValues, function(key, value) {
            leagueChoice
                .append($("<option></option>")
                    .attr("value",value.uuid)
                    .text(value.name));
        });
        leaguesListLoading = false;
        updateVisibility();
        leagueSelectHandler();

    });
}

// Обновляет видимость элементов
function updateVisibility(){

    if (tableLoading){
        loading.show();
    }
    else{
        loading.hide();
    }

    var typeSelectValue = typeSelect.val();
    if (sportsListLoading){
        typeSelect.prop("disabled", true);

    }
    else{
        typeSelect.prop("disabled", false);
    }

    if (leaguesListLoading){
        sportChoice.prop("disabled", true);

    }
    else{
        sportChoice.prop("disabled", false);
    }

    if (typeSelectValue == "sports"){
        sportChoice.hide();
        leagueChoice.hide();
        leagueChoiceLoad.hide();
        sportChoiceLoad.hide();
    }
    else if(typeSelectValue == "leagues"){
        if(sportsListLoading){
            leagueChoice.hide();
            leagueChoiceLoad.hide();
            sportChoice.hide();
            sportChoiceLoad.show();
            sportChoiceLoad.css("float", "none");
        }
        else{
            leagueChoice.hide();
            leagueChoiceLoad.hide();
            sportChoiceLoad.hide();
            sportChoice.show();
            sportChoice.css("float", "none");
        }
    }
    else{
        if(sportsListLoading && !leaguesListLoading){
            sportChoice.hide();
            leagueChoice.hide();
            leagueChoiceLoad.hide();

            sportChoiceLoad.show();
            sportChoice.css("float", "none");

        }
        else if (leaguesListLoading){

            sportChoiceLoad.hide();
            leagueChoice.hide();

            sportChoice.show();
            sportChoice.css("float", "left");
            leagueChoiceLoad.show();
            leagueChoiceLoad.css("float", "none");
        }

        else if (!leaguesListLoading){

            sportChoiceLoad.hide();
            leagueChoiceLoad.hide();

            sportChoice.show();
            sportChoice.css("float", "left");
            leagueChoice.show();
            leagueChoice.css("float", "none");
        }

    }

}


// Обработчики событий

function sportSelectHandler(){
    dataTable.find("tr").remove();

    if (typeSelect.val() == "leagues"){
        tableLoading = true;
        updateVisibility();
        var el = sportChoice.val();
        $.get( "http://localhost/api/getLeagues", {"uuid": el}, function(data){
            fillTable(data)
        })
    }

    else if(typeSelect.val() == "participants"){
        leaguesListLoading = true;
        updateVisibility();
        leagueChoice
            .find("option")
            .remove();
        fillLeagues();
    }

}

function leagueSelectHandler() {
    dataTable.find("tr").remove();
    tableLoading = true;
    updateVisibility();
    var el = leagueChoice.val();
    $.get( "http://localhost/api/getParticipants", {"uuid": el}, function(data){
        fillTable(data)
    })
}

function typeSelectHandler(selectedType) {

    dataTable.find("tr").remove();

    if (typeSelect.val() == "sports") {
        tableLoading = true;
        updateVisibility();
        $.get("http://localhost/api/getSports", function (data) {
            fillTable(data)
        })
    }

    else if (typeSelect.val() == "leagues"){
        sportsListLoading = true;
        updateVisibility();
        sportChoice
            .find("option")
            .remove();

        fillSports();

    }

    else{
        sportsListLoading = true;
        updateVisibility();
        sportChoice
            .find("option")
            .remove();

        fillSports();
    }
}

function matchSelectHandler(selectedId){
    id1 = $(selectedId).val();
    id2 = $(selectedId).parent().parent().find("td:nth-child(3)").html();
    tableName = typeSelect.val();
    $("select").prop("disabled", true);
    $.post("http://localhost/api/updateUuid", {"id1": id1, "id2": id2, "tableName": tableName}, function(data){
        showResult(data);
    })
}

function showResult(resp){

    obj = JSON.parse(resp);
    if (obj["result"] == true){
        reload();
    }
    else{
        alert("Произошла ошибка на сервере");
        reload();
    }
}

function reload(){
    $("select").prop("disabled", false);
    tablee = typeSelect.val()
    if(tablee =="sports"){
        typeSelectHandler();
    }
    else if(tablee =="leagues"){
        sportSelectHandler();
    }
    else{
        leagueSelectHandler()
    }
}


// Регистрация обработчиков событий

var dataTable = $("#dataTable").find("tbody");
var sportChoice = $("#sportChoice");
var leagueChoice = $("#leagueChoice");
var typeSelect = $("#typeSelect");
var sportChoiceLoad = $("#sportChoiceLoad");
var leagueChoiceLoad = $("#leagueChoiceLoad");
var loading = $("#loading");
var sportsListLoading = false;
var leaguesListLoading = false;
var tableLoading = false;


typeSelect.change(function() {
    typeSelectHandler(this);
});


sportChoice.change(function() {
    sportSelectHandler();
});


leagueChoice.change(function () {
    leagueSelectHandler();
});

$( document ).ready(function() {
    typeSelect.val("sports");

    typeSelectHandler(typeSelect.get(0));
});

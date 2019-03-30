$(document).ready(function () {
    $("#car-brand-field").on("change", function () {
        $.getJSON('get_all_brand_models/' + $("#car-brand-field").val(), function (data) {
            var modelField = $("#car-model-field").html("");
            modelField.append("<option disabled selected >Select model</option>");
            data.forEach(function(model) {
               modelField.append("<option value='" +model.id + "'>"+model.name +"</option>");
            });
            modelField.removeAttr("disabled");
        });
    });

    $("#car-model-field").on("change", function () {
        $.getJSON('get_all_brand_models/' + $("#car-brand-field").val(), function (data) {
            $("#car-transmission-field").removeAttr("disabled");
            $("#car-privod-field").removeAttr("disabled");
        });
    });
});
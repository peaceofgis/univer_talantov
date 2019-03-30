var findByVin = function (vin_code) {
    var btn = $("#vin-button");
    var defaultButtonText = btn.html();
    btn.html("<div class=\"lds-hourglass\"></div>");
    setTimeout(function () {
        $.getJSON("get_by_vin/" + vin_code)
            .done(function (data) {
                setBrand(data.brand_id, function () {
                    setModel(data.model_id, function () {

                        $("#car-year-field").val(data.year);
                        $("#vin-error-alert").hide();
                    });
                });
            })
            .fail(function () {
                $("#vin-error-alert").slideDown();
            })
            .always(function () {
                btn.html(defaultButtonText);
            });
    }, 1000);
}

var setBrand = function (brand_id, callback) {
    $("#car-brand-field").val(brand_id);
    $.getJSON('get_all_brand_models/' + brand_id, function (data) {
        var modelField = $("#car-model-field").html("");
        modelField.append("<option disabled selected >Select model</option>");
        data.forEach(function (model) {
            modelField.append("<option value='" + model.id + "'>" + model.name + "</option>");
        });
        modelField.removeAttr("disabled");
        callback();
    });
};

var setModel = function (model_id, callback) {
    $("#car-model-field").val(model_id);
    $.getJSON('get_all_brand_models/' + model_id, function (data) {
        $("#car-transmission-field").removeAttr("disabled");
        $("#car-gear-field").removeAttr("disabled");
    });
    callback();
};

var calculate = function (data, callback) {
    $("#calculateModal").modal("show");
    modalTitle = $("#calculateModal").find(".modal-title");
    modalBody = $("#calculateModal").find(".modal-body");
    modalTitle.html("Идет поиск цен");
    modalBody.html("<div class=\"lds-ripple\"><div></div><div></div></div>");

    setTimeout(function () {
        var data = {
            "brand_id": Number($("#car-brand-field").val()),
            "model_id": Number($("#car-model-field").val()),
            "year": Number($("#car-year-field").val()),
            "mileage": Number($("#car-mileage-field").val()),
            "gear": Number($("#car-gear-field").val()),
            "transmission": Number($("#car-transmission-field").val()),
        };
        $.getJSON("calculate/", data)
            .done(function (data) {
                modalTitle.html("Информация найдена");
                modalBody.html("<div></div>");
                b = modalBody.find("div");
                b.append("<p>По заявленным данным найдена следующая информация:</p>");
                b.append("<p>Марка: <b>" + $("#car-brand-field option:selected").text() + "</b></p>");
                b.append("<p>Модель: <b>" + $("#car-model-field option:selected").text() + "</b></p>");
                b.append("<p>Год: <b>" + $("#car-year-field").val() + "</b></p>");
                b.append("<p>Пробег: <b>" + $("#car-mileage-field").val() + "</b></p>");
                b.append("<p>Привод: <b>" + $("#car-gear-field option:selected").text() + "</b></p>");
                b.append("<p>КПП: <b>" + $("#car-transmission-field option:selected").text() + "</b></p>");
                b.append("<p>Оценочная стоимость: <u>" + data.estimated_price + "</u> рублей</p>");
                b.slideDown("slow");
            })
            .fail(function () {
                modalBody.html("Произошла ошибка!");
            })
            .always(function () {
                callback();
            });
    }, 1000);
};

$(function () {
    $("#vin-button").on("click", function () {
        findByVin($("#vin-field").val());
    });

    $("#car-brand-field").on("change", function () {
        setBrand($("#car-brand-field").val());
    });

    $("#car-model-field").on("change", function () {
        setModel($("#car-model-field").val());
    });

    $("#calculateBtn").on("click", function () {
        calculate({}, function () {

        });
    });
});
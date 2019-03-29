$(document).ready(function () {
    $("car-brand-field").change(function () {
        $.get('get_all_brand_models/'.value);
    });
});
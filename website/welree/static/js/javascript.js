if (!window.console){window.console={};};if(!window.console.log){window.console.log=function(){};};

Function.prototype.partial = function(){
    var fn = this, args = Array.prototype.slice.call(arguments);
    return function() {
        return fn.apply(this, args.concat(Array.prototype.slice.call(arguments)));
    };
};

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

welree = {}
welree.tastypie_form_callback = function(e) {
    e.preventDefault();
    var form = $(this);
    if (form.is('button')) { form = form.closest('.modal-tastypie').find('form'); }
    var data = new FormData(form.get(0));
    console.log(data);
    form.find('p.text-error').text('');
    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: data,
      processData: false,
      contentType: false,
    })
    .done(function(status, data, xhr) {
        $('.modal:visible').modal('hide');
        window.location.reload(true);
    })
    .fail(function(data, status) {
        if (status == 'error') {
            form.find('p.text-error').text(data.responseText);
        };
    })
}

$(function() {
    $('.modal-tastypie form, form.form-tastypie').on('submit', welree.tastypie_form_callback);
    $('.modal-tastypie .btn-primary').on('click', welree.tastypie_form_callback);
    $('.modal-tastypie').on('shown.bs.modal', function() {
        $(this).find('form *:input[type!=hidden]:first').focus();
    });
    $('.modal-tastypie form label.required-field, form.form-tastypie label.required-field').each(function(i, el) { $(el).parent().find(':input').prop('required', true); });
})


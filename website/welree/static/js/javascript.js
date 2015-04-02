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

welree.suggestion_fields = {
    '#id_type': welree.facets['type'],
    '#id_material': welree.facets['material'],
    '#id_color': welree.facets['color'],
}

welree.popover = function(selector) {
    $(selector).popover({
        html: true,
        title: 'foo',
        content: 'bar',
        placement: 'top',
    });
}

welree.tastypie_form_callback = function(e) {
    e.preventDefault();
    var form = $(this);
    var redirect = form.attr('redirect');
    if (form.is('button')) { form = form.closest('.modal-tastypie').find('form'); }
    var data = new FormData(form.get(0));
    form.find('p.text-error').text('');
    form.find('.has-error').removeClass('has-error').find('.ajax-errors').remove();
    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: data,
      processData: false,
      contentType: false,
    })
    .done(function(data, status, xhr) {
        if (redirect) {
            window.location.href = redirect.replace(888, data.coll_id).replace(999, data.id);
        } else {
            $('.modal:visible').modal('hide');
            window.location.reload(true);
        }
    })
    .fail(function(data, status) {
        if (status == 'error') {
            if (data.status == 413) {
                var msg = '<div role="alert" class="alert alert-dismissable alert-danger"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>The selected image is too large. Please resize the image to be less than 10mb.</div>';
                window.scrollTo(0,0);
                $(msg).appendTo('div.message-container').hide().fadeIn(1000);
            } else {
                var errors = JSON.parse(data.responseText);
                $.each(errors, function(i, type) {
                    $.each(type, function(field, field_msgs) {
                        var parent;
                        if (field == '__all__') {
                            parent = form;
                        } else {
                            parent = form.find('label[for=id_'+field+']');
                        }
                        var error_node = '<ul class="ajax-errors">';
                        $.each(field_msgs, function(i, msg) {
                            error_node += '<li>' + msg + '</li>';
                        });
                        $(error_node+'</ul>').insertAfter(parent);
                        form.find('#div_id_'+field).addClass('has-error');
                    });
                });
            }
        };
    })
}

$(function() {
    $('.modal-tastypie form, form.form-tastypie')
        .on('submit', welree.tastypie_form_callback)
        .find('input[type=url]').attr('type', 'text');
    $('.modal-tastypie .btn-primary').on('click', welree.tastypie_form_callback);
    $('.modal-tastypie').on('shown.bs.modal', function() {
        $(this).find('form *:input[type!=hidden]:first').focus();
    });
    $('.modal-tastypie form label.required-field, form.form-tastypie label.required-field').each(function(i, el) { $(el).parent().find(':input').prop('required', true); });

    $.each(welree.suggestion_fields, function(name, suggestions) {
        var parent = $(name).parent();
        var dropdown = '<ul class="dropdown-menu" role="menu">'
        $.each(suggestions, function(i, suggestion) {
            dropdown += '<li><a href="#" class="dropdown-suggestion">'+suggestion+'</a></li>';
        });
        parent
            .addClass('btn-group clearfix')
            .css('display', 'block')
            .append('<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><span class="caret"></span></button>')
            .append(dropdown+'</ul>')
            .find('input').css({'width': 'auto', 'float': 'left'});
    });
    $('.dropdown-suggestion').on('click', function(e) {
        e.preventDefault();
        var val = $(this).text();
        $(this).closest('div.btn-group').find('input').val(val);
    });
    $('#header .search-category').on('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        $(this).find('.glyphicon').toggleClass('glyphicon-plus glyphicon-minus');
        $(this).find('ul').slideToggle();
    });
    $('#header .search-category li.search-facet').on('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        var facet = $(this).attr('data-facet');
        var value = $(this).attr('data-facet-value');
        window.location = '/search/?selected_facets='+facet+'_exact:"'+encodeURIComponent(value)+'";'
    });
    welree.popover('a.action-add');
})


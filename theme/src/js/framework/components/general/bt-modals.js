(function ($) {
    function bt3DataModals() {
        return {
            template: function ($render, id) {
                const _class = id.replace('#', '');
                $('.' + _class).remove();
                const $d = $('<div/>')
                    .addClass("modal fade")
                    .addClass(_class)
                    .attr("tabindex", "-1")
                    .attr("role", "dialog")
                    .attr("aria-hidden", "true")
                    .append(
                        $('<div/>')
                            .addClass("modal-dialog modal-dialog-centered")
                            .attr('role', "document")
                            .append(
                                $('<div/>')
                                    .addClass("modal-content")
                                    .append(
                                        $('<div/>')
                                            .addClass("modal-header")
                                            .append(
                                                $('<h4/>')
                                                    .addClass("modal-title"),
                                                $('<button/>')
                                                    .addClass("close")
                                                    .attr("type", "button")
                                                    .attr("data-dismiss", "modal")
                                                    .attr("aria-label", "Close")
                                                    .append(
                                                        $("<span/>")
                                                            .attr("aria-hidden", "true")
                                                            .html('&times;'),
                                                        $("<span/>")
                                                            .addClass('sr-only')
                                                            .html('Close')
                                                    )
                                            ),
                                        $('<div/>')
                                            .addClass("modal-body"),
                                        $('<div/>')
                                            .addClass("modal-footer")
                                    )
                            )
                    );
                $render.append($d);
                return $d;
            },
            config: function ($dialog, data, callback, onOpen, onClose) {

                if ($dialog.length) {

                    $dialog.find('div.modal-header').find('h4').html(data['title']);
                    $dialog.find('div.modal-body').html('');

                    if (data['msg']) {
                        $dialog.find('div.modal-body').append($('<p/>').addClass('text-center').html(data['msg']));
                    }

                    if (data['btns']) {
                        $dialog.find('div.modal-footer').html('');
                        $.each(data['btns'], function (i, btn) {
                            if (btn) {
                                if (btn['_type'] === "close") {
                                    $dialog.find('div.modal-footer')
                                        .append(
                                            $('<button/>')
                                                .addClass(`btn ${btn['_class'] || 'btn-default'}`)
                                                .html(btn['_text'] || 'Cancelar')
                                                .attr('data-dismiss', 'modal')
                                                .attr('type', 'button')
                                        );
                                } else {
                                    $dialog.find('div.modal-footer')
                                        .append(
                                            $('<button/>')
                                                .addClass(`action btn  ${btn['_class']}`)
                                                .html(`<span class="${btn['_icon'] || ''}"></span>${btn['_text']}`)
                                                .attr('name', btn['_name'])
                                                .attr('type', btn['_type']).click(function (e) {

                                                if (btn['_url']) {
                                                    document.location.href = btn['_url'];
                                                }
                                                if (btn['_form']) {
                                                    const $form = $(btn['_form']);
                                                    if (btn['_action']) {
                                                        $form
                                                            .attr('action', btn['_action'])
                                                            .prop('action', btn['_action']);
                                                    }
                                                    $form[0].submit();
                                                }
                                                if (callback) {
                                                    callback();
                                                }
                                            })
                                        );
                                }
                            }
                        });
                    }

                    if (data['forms']) {
                        $.each(data['forms'], function (i, form) {
                            $dialog.find('div.modal-body').append($('<div/>').addClass("form-group").html(form));
                        });

                        const $required = $dialog.find(':required');
                        if ($required.length) {
                            const $action = $dialog.find('.action');
                            $action.addClass($required.length ? 'disabled' : '');
                            $required.keyup(function (e) {
                                $action.removeClass($(this).val().length ? 'disabled' : '').addClass(!($(this).val().length) ? 'disabled' : '');
                            });
                        }
                    }

                    $dialog.on('show.bs.modal', function () {
                        if (onOpen) {
                            onOpen();
                        }
                        $('.wrapper').addClass('modal-blur');
                    });
                    $dialog.on('hide.bs.modal', function () {
                        if (onClose) {
                            onClose();
                        }
                        $('.wrapper').removeClass('modal-blur');
                    });

                    $dialog.modal('show');

                }
            },
            dialog: function ($render, $obj, callback, onOpen, onClose) {
                const $data = $obj.find('[data-type="dialog"]');
                if ($data.length) {
                    $obj = $data;
                }

                $obj = $obj.data();

                window.bt3DataModals.config(
                    window.bt3DataModals.template($render, $obj['dialog']),
                    $obj, callback, onOpen, onClose);

            },

            json: function ($render, json) {
                window.bt3DataModals.config(window.bt3DataModals.template($render, json.dialog), json);
            },
        };
    }

    if (!window.bt3DataModals) {
        window.bt3DataModals = bt3DataModals();
    }
})(jQuery);
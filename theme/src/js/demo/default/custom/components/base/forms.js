class EventsToFormWithProcess {
    constructor(form) {
        this.form = $(form);
    }

    _addValidation() {
        this.form.validate({
            errorPlacement: () => {
                return false;
            }
        });
    }

    _enabledBtn() {
        $('[data-block-check]').each(function () {
            const $btn = $(this);
            const $check = $('input[type="checkbox"]');

            function toogleBtn(checked) {
                $btn.attr('disabled', checked !== $btn.data('blockCheck'));
            }

            toogleBtn($check[0].checked);
            $check.click(function () {
                toogleBtn(this.checked);
            });
        });
    }


    _onlyNumbers() {
        const $select = $('input.numeric');
        if ($select.length) {
            $select.removeNumeric();
            $select.numeric({
                negative: false,
                decimalPlaces: 2,
            });
        }
    }

    _addSelect2() {
        $("select").select2({
            closeOnSelect: true
        });
    }

    _showDialog() {
        const self = this;
        $('[data-type="show-dialog"]').click(function () {
            if (self.form.valid()) {
                if (window.bt3DataModals) {
                    window.bt3DataModals.dialog(self.form, $(this));
                }
            }
        });
    }

    init() {
        this._addValidation();
        this._showDialog();
        this._onlyNumbers();
        this._addSelect2();
        this._enabledBtn();
    }

}
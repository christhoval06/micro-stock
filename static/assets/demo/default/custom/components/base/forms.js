class EventsToFormWithProcess{constructor(t){this.form=$(t)}_addValidation(){this.form.validate({errorPlacement:()=>!1})}_enabledBtn(){$("[data-block-check]").each(function(){const t=$(this),e=$('input[type="checkbox"]');function i(e){t.attr("disabled",e!==t.data("blockCheck"))}i(e[0].checked),e.click(function(){i(this.checked)})})}_onlyNumbers(){const t=$("input.numeric");t.length&&(t.removeNumeric(),t.numeric({negative:!1,decimalPlaces:2}))}_addSelect2(){$("select").select2()}_showDialog(){const t=this;$('[data-type="show-dialog"]').click(function(){t.form.valid()&&window.bt3DataModals&&window.bt3DataModals.dialog(t.form,$(this))})}init(){this._addValidation(),this._showDialog(),this._onlyNumbers(),this._addSelect2(),this._enabledBtn()}}
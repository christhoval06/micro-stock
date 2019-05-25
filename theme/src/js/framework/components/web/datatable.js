class DataTable extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        const config = JSON.parse(JSON.parse(this.getAttribute('config')));
        config['ajax']['data'] = function (data) {
            const keys = Object.keys(data);
            for (let i = 0; i <= keys.length; i++) {
                const key = keys[i],
                    value = data[key];
                delete data[key];
                data['datatable-' + key] = value;
            }
        };
        config['ajax']['beforeSend'] = function (request) {
            request.setRequestHeader("datatable", true);
        };

        this._datatable = $(this).find('table').DataTable(config);
        // new $.fn.dataTable.FixedHeader(this._datatable);

    }

    disconnectedCallback() {
        this._datatable.destroy();
    }
}

window.addEventListener('load', () => {
    window.customElements.define('app-datatable', DataTable);
});
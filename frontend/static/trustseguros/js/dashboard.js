$.fn.extend({
    swapIn: function (toSwap) {
        Object.entries(toSwap)
            .forEach(([k, $v]) => this.find(`[data-swap="${k}"]`).replaceWith($v));
        return this;
    }
});


Date.prototype.addDays = function (days) {
    let date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
};


function filter_data(data, start, end) {
    let filtered = [];
    if (start !== undefined && end !== undefined) {
        filtered = data.filter(obj => obj.fecha_vence >= start && obj.fecha_vence <= end)
    }
    if (start === undefined && end !== undefined) {
        filtered = data.filter(obj => obj.fecha_vence <= end)
    }
    if (start !== undefined && end === undefined) {
        filtered = data.filter(obj => obj.fecha_vence >= start)
    }
    return filtered
}


function reduce_sum(data, start, end, field, callback) {
    const filtered_data = filter_data(data, start, end);
    const value = filtered_data.reduce((acc, val) => {
        acc += val[field];
        return acc;
    }, 0);

    return $('<a href="javascript:void(0)"></a>')
        .text(intcommas(parseFloat(value).toFixed(2)))
        .data(filtered_data)
        .on('click', callback);
}

function reduce_count(data, start, end, field, callback) {
    const filtered_data = filter_data(data, start, end);

    return $('<a href="javascript:void(0)"></a>')
        .text(Object.keys(_.groupBy(filtered_data, field)).length)
        .data(filtered_data)
        .on('click', callback);
}


const dashModal = $('#dashboard-modal').iziModal({});

$(document).ready(function () {
    $('.dateinput').datepicker({
        dateFormat: 'dd/mm/yy',
    });
});
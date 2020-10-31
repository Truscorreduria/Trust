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


function reduce_sum(data, start, end, field) {
    return data.reduce((acc, val) => {
        if (start !== undefined && end !== undefined) {
            if (val.fecha_vence >= start && val.fecha_vence <= end) {
                acc = parseFloat(acc) + parseFloat(val[field])
            }
        }
        if (start === undefined && end !== undefined) {
            if (val.fecha_vence <= end) {
                acc = parseFloat(acc) + parseFloat(val[field])
            }
        }
        if (start !== undefined && end === undefined) {
            if (val.fecha_vence >= start) {
                acc = parseFloat(acc) + parseFloat(val[field])
            }
        }
        return parseFloat(acc).toFixed(2);
    }, 0);
}

function reduce_count(data, start, end, field, callback) {
    let filtered_data = [];
    if (start !== undefined && end !== undefined) {
        filtered_data = data.filter(obj => obj.fecha_vence >= start && obj.fecha_vence <= end)
    }
    if (start === undefined && end !== undefined) {
        filtered_data = data.filter(obj => obj.fecha_vence <= end)
    }
    if (start !== undefined && end === undefined) {
        filtered_data = data.filter(obj => obj.fecha_vence >= start)
    }

    return $('<a href="#"></a>')
        .text(Object.keys(_.groupBy(filtered_data, field)).length)
        .data(filtered_data)
        .on('click', callback);
}
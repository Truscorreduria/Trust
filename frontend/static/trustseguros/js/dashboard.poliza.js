$(document).ready(function () {
    class DashBoard {
        constructor() {

            //region props
            this.height = 1800;
            this.sidebar_width = 300;
            this.width = window.innerWidth - this.sidebar_width;

            this.histogram_estado_height = 320;
            this.histogram_estado_width = 600;
            this.histogram_estado_axis_Y = null;
            this.histogram_estado_axis_X = null;
            this.barscolor_estado = '#4195da';

            this.histogram_ramo_height = 300;
            this.histogram_ramo_width = this.width - 150;
            this.histogram_ramo_axis_Y = null;
            this.histogram_ramo_axis_X = null;
            this.colorScaleRamo = null;
            this.ramoTextColor = '#dac277';

            this.pieRadius = 180;
            this.pieFilter = null;
            this.arc = null;
            this.outerArc = null;
            this.colorScalePie = null;
            this.pieCenterColor = '#8edcb3';

            this.legend_axis_Y = null;
            this.legendLineHeight = 20;

            this.barWidth = (this.width - 100) / 2;
            this.barColor = '#547a95';
            this.barScalePrima = null;
            this.barScaleComision = null;

            this.svg = null;
            this.svgPie = null;
            this.svgLegend = null;
            this.svgHistogramEstado = null;
            this.svgHistogramRamo = null;
            this.svgBar = null;

            this.data = [];
            this.estados = [];
            this.grupos = [];
            this.ramos = [];

            // endregion

            d3.json('.', {
                method: 'POST',
                body: JSON.stringify({}),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    "X-CSRFToken": getCookie('csrftoken'),
                }
            }).then(response => {
                this.data = [...response.polizas];

                this.svg = d3.select("#dashboard-polizas").append('svg')
                    .attr('width', this.width).attr('height', this.height);

                this.svgBar = this.svg.append('g').attr('class', 'progres-bar')
                    .attr('transform', `translate(${0}, ${0})`);

                this.svgPie = this.svg.append('g')
                    .attr('transform', `translate(${550}, ${280})`);

                this.svgLegend = this.svg.append("g")
                    .attr('transform', `translate(${60}, ${150})`);

                this.svgHistogramEstado = this.svg.append('g')
                    .attr('transform', `translate(${900}, ${120})`);

                this.svgHistogramRamo = this.svg.append('g')
                    .attr('transform', `translate(${50}, ${500})`);

                this.drawPie();
                this.drawLegend();
                this.drawHistogramEstado();
                this.drawHistogramRamo();
                this.drawProgresBar();

            }).catch(err => {
                console.log(err)
            })


        };

        range = (start, end) => {
            return Array(end - start + 1).fill().map((_, idx) => start + idx)
        };

        groupByEstado = data => {
            data = d3.group(data, d => d.status);
            data = Array.from(data, ([key, value]) => {
                return {
                    estado: key, total: value.length,
                    data: value
                }
            });
            if (this.estados.length > 0) {
                this.estados.forEach((estado,) => {
                    let obj = data.find(obj => obj.estado === estado);
                    if (obj === undefined) {
                        data.push({
                            estado: estado,
                            total: 0,
                            data: []
                        })
                    }
                })
            }

            data.sort(function (a, b) {
                if (a.estado < b.estado) return -1;
                if (a.estado > b.estado) return 1;
                return 0;
            });

            return data;
        };

        groupByGrupo = data => {
            data = d3.group(data, d => d.grupo);
            data = Array.from(data, ([key, value]) => {
                return {
                    grupo: key, total: value.length,
                    data: value
                }
            });

            if (this.grupos.length > 0) {
                this.grupos.forEach((grupo,) => {
                    let obj = data.find(obj => obj.grupo === grupo);
                    if (obj === undefined) {
                        data.push({
                            grupo: grupo,
                            total: 0,
                            data: []
                        })
                    }
                })
            }

            data.sort(function (a, b) {
                if (a.grupo < b.grupo) return -1;
                if (a.grupo > b.grupo) return 1;
                return 0;
            });

            return data;
        };

        groupByRamo = data => {
            data = d3.group(data, d => d.ramo);
            data = Array.from(data, ([key, value]) => {
                return {
                    ramo: key, total: value.length,
                    data: value
                }
            });

            if (this.ramos.length > 0) {
                this.ramos.forEach((ramo,) => {
                    let obj = data.find(obj => obj.ramo === ramo);
                    if (obj === undefined) {
                        data.push({
                            ramo: ramo,
                            total: 0,
                            data: []
                        })
                    }
                })
            }

            data.sort(function (a, b) {
                if (a.ramo < b.ramo) return -1;
                if (a.ramo > b.ramo) return 1;
                return 0;
            });

            return data;
        };

        calculatePercent = (segment, total, precision) => {
            let percent = (parseFloat(segment) / parseFloat(total)) * 100;
            return `${percent.toFixed(precision)}%`;
        };

        calulateBars = data => {
            let comision_total = d3.sum(this.data, d => d.comision);
            let prima_total = d3.sum(this.data, d => d.prima);
            let comision = d3.sum(data, d => d.comision);
            let prima = d3.sum(data, d => d.prima);

            return {
                comision: comision,
                comision_percent: this.calculatePercent(comision, comision_total, 0),
                prima: prima,
                prima_percent: this.calculatePercent(prima, prima_total, 0),
            }
        };

        legendPercent = (d, data) => {
            let total = d3.sum(data.map(v => v.total));
            return this.calculatePercent(d.total, total, 2)
        };

        drawPolyLine = d => {
            if (parseFloat(d.data.total) > 1) {
                let posA = this.arc.centroid(d);
                let posB = this.outerArc.centroid(d);
                let posC = this.outerArc.centroid(d);
                let midangle = d.startAngle + (d.endAngle - d.startAngle) / 2;
                posC[0] = this.pieRadius * 0.95 * (midangle < Math.PI ? 1 : -1);
                return [posA, posB, posC]
            } else {
                return ""
            }

        };

        pieLabelPos = d => {
            let pos = this.outerArc.centroid(d);
            let midangle = d.startAngle + (d.endAngle - d.startAngle) / 2;
            pos[0] = this.pieRadius * 0.99 * (midangle < Math.PI ? 1 : -1);
            return 'translate(' + pos + ')';
        };

        pieLabelAnchor = d => {
            let midangle = d.startAngle + (d.endAngle - d.startAngle) / 2;
            return (midangle < Math.PI ? 'start' : 'end')
        };

        pieLabelText = d => {
            if (parseFloat(d.data.total) > 0) {
                return `${d.data.grupo} (${d.data.total})`
            } else {
                return ``
            }
        };

        pieTotalText = (d, data) => {
            if (d !== undefined) {
                return data.find(el => el.grupo === d.grupo).total
            } else {
                return d3.sum(data, d => d.total)
            }
        };

        drawPie = () => {
            let data = this.groupByGrupo(this.data);
            let total = d3.sum(data, d => d.total);

            this.grupos = data.map(d => d.grupo);
            this.grupos.sort();
            this.colorScalePie = d3.scaleOrdinal()
                .domain(this.grupos)
                .range(d3.schemeCategory10);

            this.pieFilter = d3.pie()
                .value(d => d.total)
                .sort((a, b) => {
                    if (a.grupo < b.grupo) return -1;
                    if (a.grupo > b.grupo) return 1;
                    return 0;
                });
            data = this.pieFilter(data);

            this.arc = d3.arc()
                .innerRadius(this.pieRadius * 0.5)
                .outerRadius(this.pieRadius * 0.8);

            this.outerArc = d3.arc()
                .innerRadius(this.pieRadius * 0.9)
                .outerRadius(this.pieRadius * 0.9);

            this.svgPie
                .selectAll('allSlices')
                .data(data)
                .enter()
                .append('path')
                .attr('d', this.arc)
                .attr("fill", d => this.colorScalePie(d.data.grupo))
                .attr("stroke", "white")
                .style("stroke-width", "2px")
                .on('mouseover', d => {
                    this.updateHistogramEstado(d.data.data, this.colorScalePie(d.data.grupo));
                    this.updateHistogramRamo(d.data.data, this.colorScalePie(d.data.grupo));
                    this.updatePieCenter(d, data);
                    this.updateProgresBar(d.data.data, this.colorScalePie(d.data.grupo));
                })
                .on('mouseout', () => {
                    this.updateHistogramEstado(this.data, this.barscolor_estado);
                    this.updateHistogramRamo(this.data);
                    this.updatePieCenter(undefined, data);
                    this.updateProgresBar(this.data, this.barColor);
                });

            this.svgPie
                .append('text')
                .attr('class', 'pie-total')
                .text(total)
                .attr('transform', 'translate(0, -20)')
                .style('text-anchor', 'middle')
                .style('font-size', '2.5em')
                .style('fill', this.pieCenterColor);

            this.svgPie
                .append('text')
                .attr('class', 'pie-percent')
                .text('100%')
                .attr('transform', 'translate(0, 40)')
                .style('text-anchor', 'middle')
                .style('font-size', '4em')
                .style('fill', this.pieCenterColor);

            this.svgPie
                .append('text')
                .attr('class', 'pie-grupo')
                .text('POR GRUPO')
                .attr('transform', 'translate(-500, -180)')
                .style('font-size', '2em')
                .style('fill', this.pieCenterColor);

            /*this.svgPie
                .selectAll('allPolylines')
                .data(data)
                .enter()
                .append('polyline')
                .attr("stroke", "black")
                .style("fill", "none")
                .attr("stroke-width", 1)
                .attr('points', this.drawPolyLine);


            this.svgPie
                .selectAll('allLabels')
                .data(data)
                .enter()
                .append('text')
                .text(this.pieLabelText)
                .attr('transform', this.pieLabelPos)
                .style('text-anchor', this.pieLabelAnchor)
                .style('font-size', '0.9em');*/
        };

        drawLegend = () => {
            let data = this.groupByGrupo(this.data);

            this.legend_axis_Y = d3.scaleBand()
                .domain(this.grupos)
                .range([0, this.legendLineHeight * this.grupos.length]);

            let tr = this.svgLegend.selectAll(".legend").data(data).enter().append('g');

            tr.append("rect")
                .attr("class", 'box')
                .attr("width", '16').attr("height", '16')
                .attr("y", d => this.legend_axis_Y(d.grupo))
                .attr("fill", d => this.colorScalePie(d.grupo));

            tr.append("text").text(d => d3.format(",")(d.total))
                .attr("class", 'total')
                .attr("text-anchor", "middle")
                .attr('x', 30).attr("y", d => this.legend_axis_Y(d.grupo) + 13)
                .style('font-size', '.8em')
                .attr("fill", d => this.colorScalePie(d.grupo));

            tr.append("text").text(d => this.legendPercent(d, data))
                .attr("class", 'percent')
                .attr("text-anchor", "middle")
                .attr('x', 70).attr("y", d => this.legend_axis_Y(d.grupo) + 13)
                .style('font-size', '.75em')
                .attr("fill", d => this.colorScalePie(d.grupo));

            tr.append("text").text(d => d.grupo)
                .attr("class", 'grupo')
                .attr('x', 100).attr("y", d => this.legend_axis_Y(d.grupo) + 13)
                .style('font-size', '.75em')
                .attr("fill", d => this.colorScalePie(d.grupo));
        };

        drawHistogramEstado = () => {
            let data = this.groupByEstado(this.data);

            this.estados = data.map(d => d.estado).sort();

            this.histogram_estado_axis_X = d3.scaleBand()
                .domain(this.estados)
                .range([0, this.histogram_estado_width]);

            this.histogram_estado_axis_Y = d3.scaleLinear()
                .range([this.histogram_estado_height, 0])
                .domain([0, d3.max(data, d => d.total) + 100]);

            this.svgHistogramEstado.append("g")
                .call(d3.axisLeft(this.histogram_estado_axis_Y));

            this.svgHistogramEstado.append("g")
                .call(d3.axisBottom(this.histogram_estado_axis_X))
                .attr('transform', `translate(0, ${this.histogram_estado_height})`);

            this.svgHistogramEstado.append('text').attr('class', 'estado-text')
                .text('POR ESTADO')
                .style('font-size', '2em')
                .style('fill', this.barscolor_estado)
                .attr('transform', `translate(0,-20)`);

            let bars = this.svgHistogramEstado.selectAll(".bar").data(data).enter()
                .append("g").attr("class", "bar");

            bars.append("rect")
                .attr("x", d => this.histogram_estado_axis_X(d.estado) + 2)
                .attr("y", d => this.histogram_estado_axis_Y(d.total))
                .attr("width", this.histogram_estado_axis_X.bandwidth() - 2)
                .attr("height", d => this.histogram_estado_height - this.histogram_estado_axis_Y(d.total))
                .attr('fill', this.barscolor_estado)
                .on('mouseover', d => {
                    this.updatePie(d.data);
                    this.updateLegend(d.data);
                    this.updateHistogramRamo(d.data, this.barscolor_estado);
                    this.svgHistogramEstado.select('.estado-text').text(d.estado);
                    this.updateProgresBar(d.data, this.barscolor_estado);
                })
                .on('mouseout', () => {
                    this.updatePie(this.data);
                    this.updateLegend(this.data);
                    this.updateHistogramRamo(this.data);
                    this.svgHistogramEstado.select('.estado-text').text('POR ESTADO');
                    this.updateProgresBar(this.data, this.barColor);
                });

            bars.append("text")
                .text(d => d3.format(",")(d.total))
                .attr("x", d => this.histogram_estado_axis_X(d.estado) + this.histogram_estado_axis_X.bandwidth() / 2)
                .attr("y", d => this.histogram_estado_axis_Y(d.total) - 5)
                .attr("text-anchor", "middle");
        };

        drawHistogramRamo = () => {
            let data = this.groupByRamo(this.data);

            this.ramos = data.map(d => d.ramo).sort();
            this.colorScaleRamo = d3.scaleOrdinal()
                .domain(this.ramos)
                .range(d3.schemeSet3);

            this.histogram_ramo_axis_X = d3.scaleBand()
                .domain(this.ramos)
                .range([0, this.histogram_ramo_width]);

            this.histogram_ramo_axis_Y = d3.scaleSymlog()
                .range([this.histogram_ramo_height, 0])
                .domain([0, d3.max(data, d => d.total) + 100]);

            this.svgHistogramRamo.append("g")
                .call(d3.axisLeft(this.histogram_ramo_axis_Y));

            this.svgHistogramRamo.append('text').attr('class', 'ramo-text')
                .text('POR RAMO')
                .style('font-size', '2em')
                .style('fill', this.ramoTextColor)
                .attr('transform', `translate(0,-20)`);

            let bars = this.svgHistogramRamo.selectAll(".bar").data(data).enter()
                .append("g").attr("class", "bar");

            bars.append("rect")
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + 2)
                .attr("y", d => this.histogram_ramo_axis_Y(d.total))
                .attr("width", this.histogram_ramo_axis_X.bandwidth() - 2)
                .attr("height", d => this.histogram_ramo_height - this.histogram_ramo_axis_Y(d.total))
                .attr('fill', d => this.colorScaleRamo(d.ramo))
                .on('mouseover', d => {
                    this.updatePie(d.data);
                    this.updateLegend(d.data);
                    this.updateHistogramEstado(d.data, this.colorScaleRamo(d.ramo));
                    this.svgHistogramRamo.select('.ramo-text').text(d.ramo)
                        .style('fill', this.colorScaleRamo(d.ramo));
                    this.updateProgresBar(d.data, this.colorScaleRamo(d.ramo));
                })
                .on('mouseout', () => {
                    this.updateHistogramEstado(this.data, this.barscolor_estado);
                    this.updatePie(this.data);
                    this.updateLegend(this.data);
                    this.svgHistogramRamo.select('.ramo-text').text('POR RAMO')
                        .style('fill', '#dac277');
                    this.updateProgresBar(this.data, this.barColor);
                });

            bars.append("text")
                .text(d => d3.format(",")(d.total))
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + this.histogram_ramo_axis_X.bandwidth() / 2)
                .attr("y", d => this.histogram_ramo_axis_Y(d.total) - 5)
                .attr("text-anchor", "middle");

            this.svgHistogramRamo.append("g")
                .attr("class", "axis")
                .attr("transform", "translate(0," + this.histogram_ramo_height + ")")
                .call(d3.axisBottom(this.histogram_ramo_axis_X).ticks(this.ramos.length))
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)");
        };

        drawProgresBar = () => {
            let data = this.calulateBars(this.data);

            this.barScalePrima = d3.scaleLinear()
                .range([0, this.barWidth])
                .domain([0, data.prima]);

            this.barScaleComision = d3.scaleLinear()
                .range([0, this.barWidth])
                .domain([0, data.comision]);

            let comision = this.svgBar.append('g').attr('class', 'bar-comision');
            let prima = this.svgBar.append('g').attr('class', 'bar-comision');

            comision.append('rect')
                .attr('class', 'bar-bg')
                .attr('width', this.barWidth).attr('height', 10)
                .attr('rx', 3).attr('ry', 3)
                .attr('transform', `translate(0, 30)`)
                .style('fill', 'gray');
            comision.append('rect')
                .attr('class', 'bar-value-prima')
                .attr('width', this.barWidth).attr('height', 10)
                .attr('rx', 3).attr('ry', 3)
                .attr('transform', `translate(0, 30)`)
                .style('fill', this.barColor);
            comision.append('text').text(`Prima U$ ${d3.format(',')(data.prima)}`)
                .attr('class', 'text-prima')
                .attr('transform', `translate(0, 20)`)
                .style('fill', this.barColor)
                .style('font-size', '1.5em');
            comision.append('text').text(`100%`)
                .attr('class', 'text-prima-percent')
                .attr('transform', `translate(${this.barWidth - 30}, 20)`)
                .style('fill', 'gray')
                .style('text-anchor', 'middle')
                .style('font-size', '1.5em');

            prima.append('rect')
                .attr('class', 'bar-bg')
                .attr('width', this.barWidth).attr('height', 10)
                .attr('rx', 3).attr('ry', 3)
                .attr('transform', `translate(800, 30)`)
                .style('fill', 'gray');
            prima.append('rect')
                .attr('class', 'bar-value-comision')
                .attr('width', this.barWidth).attr('height', 10)
                .attr('rx', 3).attr('ry', 3)
                .attr('transform', `translate(800, 30)`)
                .style('fill', this.barColor);
            prima.append('text').text(`Comision U$ ${d3.format(',')(data.comision)}`)
                .attr('class', 'text-comision')
                .attr('transform', `translate(800, 20)`)
                .style('fill', this.barColor)
                .style('font-size', '1.5em');
            prima.append('text').text(`100%`)
                .attr('class', 'text-comision-percent')
                .attr('transform', `translate(${800 + (this.barWidth - 30)}, 20)`)
                .style('fill', 'gray')
                .style('text-anchor', 'middle')
                .style('font-size', '1.5em');
        };

        updateHistogramEstado = (data, color) => {
            this.svgHistogramEstado.select('.estado-text')
                .style('fill', color);

            data = this.groupByEstado(data);
            let bars = this.svgHistogramEstado.selectAll(".bar")
                .data(data);

            bars.select("rect").transition().duration(500)
                .attr("y", d => this.histogram_estado_axis_Y(d.total))
                .attr("x", d => this.histogram_estado_axis_X(d.estado) + 2)
                .attr("height", d => this.histogram_estado_height - this.histogram_estado_axis_Y(d.total))
                .attr("fill", color);

            bars.select("text").transition().duration(500)
                .text(d => d3.format(",")(d.total))
                .attr("y", (d) => this.histogram_estado_axis_Y(d.total) - 5)
                .attr("x", d => this.histogram_estado_axis_X(d.estado) + this.histogram_estado_axis_X.bandwidth() / 2);
        };

        updateHistogramRamo = (data, color) => {
            data = this.groupByRamo(data);
            let bars = this.svgHistogramRamo.selectAll(".bar")
                .data(data);
            bars.select("text").transition().duration(500)
                .text(d => d3.format(",")(d.total))
                .attr("y", (d) => this.histogram_ramo_axis_Y(d.total) - 5)
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + this.histogram_ramo_axis_X.bandwidth() / 2);
            if (color === undefined) {
                this.svgHistogramRamo.select('.ramo-text')
                    .style('fill', this.ramoTextColor);
                bars.select("rect").transition().duration(500)
                    .attr("y", d => this.histogram_ramo_axis_Y(d.total))
                    .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + 2)
                    .attr("height", d => this.histogram_ramo_height - this.histogram_ramo_axis_Y(d.total))
                    .attr("fill", d => this.colorScaleRamo(d.ramo));
            } else {
                this.svgHistogramRamo.select('.ramo-text')
                    .style('fill', color);
                bars.select("rect").transition().duration(500)
                    .attr("y", d => this.histogram_ramo_axis_Y(d.total))
                    .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + 2)
                    .attr("height", d => this.histogram_ramo_height - this.histogram_ramo_axis_Y(d.total))
                    .attr("fill", d => color);
            }
        };

        updatePie = (data) => {
            data = this.groupByGrupo(data);
            let total = d3.sum(data, d => d.total);
            data = this.pieFilter(data);
            this.svgPie.selectAll("path").data(data) //.transition().duration(500)
                .attr("d", this.arc);
            this.svgPie.select('.pie-total').text(total);
            /*this.svgPie.selectAll("polyline").data(data).transition().duration(500)
                .attr('points', this.drawPolyLine);
            this.svgPie.selectAll("text").data(data).transition().duration(500)
                .text(this.pieLabelText)
                .attr('transform', this.pieLabelPos)
                .style('text-anchor', this.pieLabelAnchor);*/
        };

        updatePieCenter = (d, data) => {
            let total = d3.sum(data, d => d.data.total);
            if (d !== undefined) {
                let percent = (d.data.total / total) * 100;
                this.svgPie.select('.pie-total').text(d.data.total)
                    .style("fill", this.colorScalePie(d.data.grupo));
                this.svgPie.select('.pie-percent').text(`${percent.toFixed(0)}%`)
                    .style("fill", this.colorScalePie(d.data.grupo));
                this.svgPie.select('.pie-grupo').text(d.data.grupo)
                    .style("fill", this.colorScalePie(d.data.grupo));
            } else {
                this.svgPie.select('.pie-total').text(total)
                    .style("fill", this.pieCenterColor);
                this.svgPie.select('.pie-percent').text(`100%`)
                    .style("fill", this.pieCenterColor);
                this.svgPie.select('.pie-grupo').text(`POR GRUPO`)
                    .style("fill", this.pieCenterColor);
            }

        };

        updateLegend = data => {
            data = this.groupByGrupo(data);
            let tr = this.svgLegend.selectAll('g').data(data);
            tr.select('.total')
                .text(d => d3.format(",")(d.total));
            tr.select('.percent')
                .text(d => this.legendPercent(d, data));
        };

        updateProgresBar = (data, color) => {
            data = this.calulateBars(data);
            this.svgBar.select('.text-comision').transition().duration(500)
                .text(`Comisión U$ ${d3.format(',')(data.comision)}`)
                .style('fill', color);

            this.svgBar.select('.text-prima-percent').transition().duration(500)
                .text(data.prima_percent);

            this.svgBar.select('.text-comision-percent').transition().duration(500)
                .text(data.comision_percent);

            this.svgBar.select('.text-prima').transition().duration(500)
                .text(`Prima U$ ${d3.format(',')(data.prima)}`)
                .style('fill', color);

            this.svgBar.select('.bar-value-prima').transition().duration(500)
                .attr('width', this.barScalePrima(data.prima))
                .style('fill', color);
            this.svgBar.select('.bar-value-comision').transition().duration(500)
                .attr('width', this.barScaleComision(data.comision))
                .style('fill', color);
        };
    }

    new DashBoard()
});
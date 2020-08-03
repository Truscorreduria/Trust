$(document).ready(function () {
    class DashBoard {
        constructor() {
            this.height = 1800;
            this.sidebar_width = 300;
            this.width = window.innerWidth - this.sidebar_width;

            this.histogram_estado_height = 350;
            this.histogram_estado_width = 600;
            this.histogram_estado_axis_Y = null;
            this.histogram_estado_axis_X = null;
            this.barscolor_estado = '#4195da';

            this.histogram_ramo_height = 350;
            this.histogram_ramo_width = this.width - 50;
            this.histogram_ramo_axis_Y = null;
            this.histogram_ramo_axis_X = null;
            this.barscolor_ramo = '#dabb4e';

            this.pieRadius = 200;
            this.pieFilter = null;
            this.arc = null;
            this.outerArc = null;

            this.svg = null;
            this.svgPie = null;
            this.svgHistogramEstado = null;
            this.svgHistogramRamo = null;

            this.data = [];
            this.estados = [];
            this.grupos = [];
            this.ramos = [];

            d3.json('.', {
                method: 'POST',
                body: JSON.stringify({
                    hola: 'hola',
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    "X-CSRFToken": getCookie('csrftoken'),
                }
            }).then(response => {
                this.data = [...response.data];

                this.svg = d3.select("#dashboard-polizas")
                    .append('svg')
                    .attr('width', this.width)
                    .attr('height', this.height);

                this.svgPie = this.svg.append('g')
                    .attr('transform', `translate(${400}, ${200})`);

                this.drawPie(response.data);

                this.svgHistogramEstado = this.svg.append('g')
                    .attr('transform', `translate(${900}, ${0})`);

                this.drawHistogramEstado();

                this.svgHistogramRamo = this.svg.append('g')
                    .attr('transform', `translate(${50}, ${400})`);

                this.drawHistogramRamo();


            }).catch(err => {
                console.log(err)
            })


        };

        range = (start, end) => {
            return Array(end - start + 1).fill().map((_, idx) => start + idx)
        };

        groupByEstado = data => {
            data = d3.group(data, d => d.status.label);
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

        drawPie = (data) => {
            data = this.groupByGrupo(data);

            this.grupos = data.map(d => d.grupo);
            let colorScale = d3.scaleOrdinal()
                .domain(this.grupos)
                .range(d3.schemeCategory10);

            this.pieFilter = d3.pie()
                .value(d => d.total)
                .sort((el1, el2) => el1.total - el2.total);
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
                .attr("fill", d => colorScale(d.data.grupo))
                .attr("stroke", "white")
                .style("stroke-width", "2px")
                .on('mouseover', d => {
                    this.updateHistogramEstado(d.data.data, colorScale(d.data.grupo));
                    this.updateHistogramRamo(d.data.data, colorScale(d.data.grupo));
                })
                .on('mouseout', () => {
                    this.updateHistogramEstado(this.data, this.barscolor_estado);
                    this.updateHistogramRamo(this.data, this.barscolor_ramo);
                });

            this.svgPie
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
                .style('font-size', '0.9em');
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
                    this.updateHistogramRamo(d.data, this.barscolor_ramo)
                })
                .on('mouseout', () => {
                    this.updatePie(this.data);
                    this.updateHistogramRamo(this.data, this.barscolor_ramo)
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
            let colorScale = d3.scaleOrdinal()
                .domain(this.ramos)
                .range(d3.schemeSet3);

            this.histogram_ramo_axis_X = d3.scaleBand()
                .domain(this.ramos)
                .range([0, this.histogram_ramo_width]);

            this.histogram_ramo_axis_Y = d3.scaleLinear()
                .range([this.histogram_estado_height, 0])
                .domain([0, d3.max(data, d => d.total) + 100]);

            this.svgHistogramRamo.append("g")
                .call(d3.axisLeft(this.histogram_ramo_axis_Y));

            let bars = this.svgHistogramRamo.selectAll(".bar").data(data).enter()
                .append("g").attr("class", "bar");

            bars.append("rect")
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + 2)
                .attr("y", d => this.histogram_ramo_axis_Y(d.total))
                .attr("width", this.histogram_ramo_axis_X.bandwidth() - 2)
                .attr("height", d => this.histogram_ramo_height - this.histogram_ramo_axis_Y(d.total))
                .attr('fill', d => colorScale(d.ramo))
                .on('mouseover', d => {
                    this.updatePie(d.data);
                    this.updateHistogramEstado(d.data, colorScale(d.ramo));
                })
                .on('mouseout', () => {
                    this.updateHistogramEstado(this.data, this.barscolor_estado);
                    this.updatePie(this.data);
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

        updateHistogramEstado = (data, color) => {
            let bars = this.svgHistogramEstado.selectAll(".bar");
            data = this.groupByEstado(data);
            bars.data(data);

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
            let bars = this.svgHistogramRamo.selectAll(".bar");
            data = this.groupByRamo(data);
            bars.data(data);

            bars.select("rect").transition().duration(500)
                .attr("y", d => this.histogram_ramo_axis_Y(d.total))
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + 2)
                .attr("height", d => this.histogram_ramo_height - this.histogram_ramo_axis_Y(d.total))
                .attr("fill", color);

            bars.select("text").transition().duration(500)
                .text(d => d3.format(",")(d.total))
                .attr("y", (d) => this.histogram_ramo_axis_Y(d.total) - 5)
                .attr("x", d => this.histogram_ramo_axis_X(d.ramo) + this.histogram_ramo_axis_X.bandwidth() / 2);
        };

        updatePie = (data) => {
            data = this.groupByGrupo(data);
            data = this.pieFilter(data);
            this.svgPie.selectAll("path").data(data).transition().duration(500)
                .attr("d", this.arc);
            this.svgPie.selectAll("polyline").data(data).transition().duration(500)
                .attr('points', this.drawPolyLine);
            this.svgPie.selectAll("text").data(data).transition().duration(500)
                .text(this.pieLabelText)
                .attr('transform', this.pieLabelPos)
                .style('text-anchor', this.pieLabelAnchor);
        };
    }

    new DashBoard()
});
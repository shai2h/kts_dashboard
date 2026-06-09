"use client";

import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";
import { useDashboard } from "@/hooks/useDashboard";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
    ssr: false,
});

export default function HorizontalBar() {
    const { data, loading, error } = useDashboard();

    if (loading) {
        return <div>Загрузка...</div>;
    }

    if (error || !data) {
        return <div className="text-red-500">Ошибка загрузки данных</div>;
    }

    const byPodr = data.by_podr;

    // значения (проценты)
    const seriesData = byPodr.map(item =>
        Number(item.percent.toFixed(1))
    );

    // подписи (подразделения)
    const categories = byPodr.map(item => item.podr);

    const options: ApexOptions = {
        series: [{
            name: 'Показатель',
            data: seriesData
        }],
        chart: {
            type: 'bar',
            height: 380,
            toolbar: {
                show: true
            }
        },
        plotOptions: {
            bar: {
                barHeight: '100%',
                distributed: true,
                horizontal: true,
                dataLabels: {
                    position: 'bottom' as const,
                },
            }
        },
        colors: ['#ff3838', '#2dc5f7', '#fc8312'],

        dataLabels: {
            enabled: true,
            textAnchor: 'start' as const,
            style: {
                colors: ['#fff'],
                fontSize: '16px',
                fontWeight: 'bold'
            },
            formatter: function (val: number, opts: any) {
                const category = opts.w.globals.labels[opts.dataPointIndex];
                return `${category}: ${val}%`;
            },
            offsetX: 10,
            dropShadow: {
                enabled: true,
                top: 1,
                left: 1,
                blur: 1,
                opacity: 0.45
            }
        },
        stroke: {
            width: 1,
            colors: ['#fff']
        },
        xaxis: {
            max: 100,
            categories: categories,
            labels: {
                formatter: function (val: string) {
                    return `${val}%`;
                }
            }
        },
        yaxis: {
            labels: {
                show: false // Скрываем Y-ось, так как метки внутри баров
            }
        },
        tooltip: {
            theme: 'dark' as const,
            y: {
                title: {
                    formatter: function () {
                        return '';
                    }
                },
                formatter: function (val: number, opts: any) {
                    const category = opts.w.globals.labels[opts.dataPointIndex];
                    return `<strong>${category}</strong><br>${val}% выполнения`;
                }
            }
        },
        legend: {
            show: false
        }
    };

    return (
        <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Процент выполнения плана по подразделениям
            </h3>

            {/* Горизонтальная гистограмма */}
            <ReactApexChart
                options={options}
                series={[{ name: 'Показатель', data: seriesData }]}
                type="bar"
                height={380}
            />
        </div>
    );
}

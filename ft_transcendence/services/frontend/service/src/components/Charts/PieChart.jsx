import React from 'react';

import './PieChart.css';

const PieChart = ({ data = {} }) => {

    return (
        <div className={`piechart row`}>
            <div
                className={`chart`}
                style={{background: `conic-gradient(${Object.keys(data).map((segment, index) => {
                    return `${data[segment]?.color} ${data[segment].value}%${index < Object.keys(data).length - 1 ? ', ' : ')'}`;
                }).join('')}` }}
            >
            </div>
            <div className='data col' >
                {Object.keys(data).map((segment, index) => {
                    return (
                        <div className='row'>
                            <p>{data[segment].name} ({data[segment].value}%)</p>
                            <div
                                className='indicator'
                                style={{backgroundColor: data[segment].color}}
                            >
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    );
}

export default PieChart;

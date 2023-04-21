import {getPlayerAge} from "@/classes/Utils";

export function getAgeRepartitionStatData(gamesSelection, data){
    const datachart = {
        labels: [],
        datasets: []
    }

    for(let i = 0; i < 100; i++){
        datachart.labels.push(i);
    }

    for(let i = 0; i < gamesSelection.length; i++) {
        if (!gamesSelection[i].selected) continue;
        let dataGame = new Array(100).fill(0);

        for (let p of Object.keys(data[gamesSelection[i].id].players)) {
            let player = data[gamesSelection[i].id].players[p];
            if(!player || !player["status-active"]) continue;
            let age = getPlayerAge(player["birthdate"]);
            dataGame[age]++;
        }

        datachart.datasets.push({
            label: gamesSelection[i].name,
            data: dataGame,
            borderColor: gamesSelection[i]["main_color"],
            backgroundColor: gamesSelection[i]["secondary_color"],
        })
    }
    return datachart;
}

export function getPlayerAgeStatOptions(){
    return {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + " : "+ context.parsed + " players"
                    }
                }
            },
            legend: {
                position: 'top',
                display: false
            },
            title: {
                display: false
            },
            datalabels: {
                labels: {
                    title: {
                        font: {
                            weight: 'bold'
                        }
                    },
                    value: {
                        color: 'white'
                    }
                },
                formatter: function(value, context) {
                    return context.dataIndex;
                }
            }
        }
    };
}
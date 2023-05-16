import {getTimeRangeFromAllGames} from "@/classes/Utils";


export function getCashPrizeEvolutionOptions(){
    return {
        responsive: true,
        plugins: {
            datalabels: {
                display: false
            },
            legend: {
                position: 'top',
            },
            title: {
                display: false
            }
        }};
}

export function CashPrizeEvolution(gamesSelection, data){
    const datachart = {
        labels: [],
        datasets: []
    }

    const timeRange = getTimeRangeFromAllGames(gamesSelection, data);
    for(let i = timeRange.min; i <= timeRange.max; i++){
        datachart.labels.push(i);
    }

    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        let dataGame = [];
        for(let j = timeRange.min; j <= timeRange.max; j++){
            let count = 0;
            for (let t in data[gamesSelection[i].id].tournaments) {
                let tournament = data[gamesSelection[i].id].tournaments[t];
                if(!tournament["start-date"].includes(j)) continue;
                count += tournament["prize-pool"];
            }
            dataGame.push(count);
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
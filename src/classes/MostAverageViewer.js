import {getTimeRangeFromAllGames} from "@/classes/Utils";

export function getMostAverageViewerTournamentOptions(){
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

export function getMostAverageViewerTournament(gamesSelection, data){
    const datachart = {
        labels: [],
        datasets: []
    }

    const timeRange = getTimeRangeFromAllGames(gamesSelection, data);
    for(let i = 2016; i <= timeRange.max; i++){
        datachart.labels.push(i);
    }

    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        let dataGame = [];
        for(let j = 2016; j <= timeRange.max; j++){
            let max = 0;
            for (let t in data[gamesSelection[i].id].tournaments) {
                let tournament = data[gamesSelection[i].id].tournaments[t];
                if(!tournament["start-date"].includes(j) || tournament["average-viewers"] === undefined) continue;
                if(tournament["average-viewers"] > max){
                    max = tournament["average-viewers"];
                }
            }
            if (max === 0) max = undefined;
            dataGame.push(max);
        }

        datachart.datasets.push({
            label: gamesSelection[i].name,
            data: dataGame,
            borderColor: gamesSelection[i]["main_color"],
            backgroundColor: gamesSelection[i]["secondary_color"],
            skipNull: true
        })
    }
    return datachart;
}
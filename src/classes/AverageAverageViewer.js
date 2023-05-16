import {getTimeRangeFromAllGames} from "@/classes/Utils";

export function getAverageAverageViewerTournamentOptions(){
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

export function getAverageAverageViewerTournament(gamesSelection, data){
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
            let sum = 0;
            let count = 0;
            for (let t in data[gamesSelection[i].id].tournaments) {
                let tournament = data[gamesSelection[i].id].tournaments[t];
                if(!tournament["start-date"].includes(j) || tournament["average-viewers"] === undefined) continue;
                if(tournament["average-viewers"] > 0){
                    sum += tournament["average-viewers"];
                    count++;
                }
            }
            let average = undefined;
            if (sum !== 0) average = sum / count;
            dataGame.push(average);
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
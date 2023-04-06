import {getTimeRangeFromAllGames} from "@/classes/Utils";

export function PlayerNationalityStatData(gamesSelection, data, country){
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
                for (let p in tournament.players) {
                    let player = tournament.players[p];
                    if(data[gamesSelection[i].id].players[player] !== undefined && data[gamesSelection[i].id].players[player].country.toLowerCase() === country.toLowerCase()) count ++;
                }
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

export function getPlayerNationalityStatOptions(){
    return {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: false
            }
        }};
}
import data from "@/assets/data.json";
import {getAllCountryPlayers} from "@/classes/Utils";
import {Colors} from "chart.js";

export function getRateOfRetiredPlayersOptions(){
    return {
        plugins: {
            title: {
                display: false
            },
            datalabels: {
                display: false
            }
        },
        responsive: true,
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true
            }
        }
    };
}

export function getRateOfRetiredPlayersData(gamesSelection, data){
    let retiredByGameMap = new Map();
    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        for(let p in data[gamesSelection[i].id].players){
            let player = data[gamesSelection[i].id].players[p];
            if(retiredByGameMap.has(data[gamesSelection[i].id].name)) {
                retiredByGameMap.get(data[gamesSelection[i].id].name).active+=player["status-active"]?1:0;
            } else {
                retiredByGameMap.set(data[gamesSelection[i].id].name, {game: data[gamesSelection[i].id].name, active: player["status-active"]?1:0, numberOfPlayers: Object.keys(data[gamesSelection[i].id].players).length, main_color: gamesSelection[i]["main_color"], secondary_color : gamesSelection[i]["secondary_color"]});
            }
        }
    }
    let retiredByGame = [...retiredByGameMap.values()];

    const datachart = {
        labels: retiredByGame.map((game) => game.game),
        datasets: []
    }
    datachart.datasets.push({
        label: "Active players (%)",
        data: retiredByGame.map((game) => game.active/game.numberOfPlayers*100),
        borderColor: retiredByGame.map((game) => game.main_color),
        backgroundColor: retiredByGame.map((game) => game.secondary_color),
    });

    return datachart;
}
import data from "@/assets/data.json";
import {getAllCountryPlayers} from "@/classes/Utils";

export function getPlayerBestPrizeOptions(){
    return {
        plugins: {
            title: {
                display: false
            },
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

export function getPlayerBestPrizeData(gamesSelection, data){

    let playersBestPrize = [];
    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        for(let p in data[gamesSelection[i].id].players){
            let player = data[gamesSelection[i].id].players[p];
            player["game_index"] = i;
            playersBestPrize.push(player);
        }
    }
    playersBestPrize.sort((a, b) => b["approx-total-winning"] - a["approx-total-winning"]);
    const datachart = {
        labels: [],
        datasets: [{
            label: "Approximate total winnings",
            data: [],
            borderColor: [],
            backgroundColor: [],
        }]
    }
    for(let i = 0; i < 30 ; i++) {
        datachart.labels.push(playersBestPrize[i]["nickname"]);
        datachart.datasets[0].data.push(playersBestPrize[i]["approx-total-winning"]);
        datachart.datasets[0].borderColor.push(gamesSelection[playersBestPrize[i]["game_index"]]["main_color"]);
        datachart.datasets[0].backgroundColor.push(gamesSelection[playersBestPrize[i]["game_index"]]["secondary_color"]);
    }

    return datachart;
}
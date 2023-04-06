import data from "@/assets/data.json";
import {getAllCountryPlayers} from "@/classes/Utils";

export function getRegionalDistributionOptions(){
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

export function getRegionalDistributionData(gamesSelection, data){
    const countries = getAllCountryPlayers(data);
    const datachart = {
        labels: countries,
        datasets: []
    }

    let countryIndexes = {};
    countries.forEach((country, index) => {
        countryIndexes[country] = index;
    });

    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        let dataGame = Array(countries.length).fill(0);
        for(let p in data[gamesSelection[i].id].players){
            let player = data[gamesSelection[i].id].players[p];
            dataGame[countryIndexes[player.country]]++;
        }
        datachart.datasets.push({
            label: gamesSelection[i].name,
            data: dataGame,
            borderColor: gamesSelection[i]["main_color"],
            backgroundColor: gamesSelection[i]["secondary_color"],
        });
    }

    return datachart;
}
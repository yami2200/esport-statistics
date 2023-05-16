import data from "@/assets/data.json";
import {getAllCountryPlayers} from "@/classes/Utils";
import {Colors} from "chart.js";

export function getMostWinningTeamOptions(){
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

export function getMostWinningTeamData(gamesSelection, data){
    //team name -> team name, number of wins

    let teamsWinMap = new Map();
    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        for(let tournament of data[gamesSelection[i].id].tournaments){
            if(teamsWinMap.has(tournament["team-winner"])) {
                teamsWinMap.get(tournament["team-winner"]).counting++;
            } else {
                teamsWinMap.set(tournament["team-winner"], {team: tournament["team-winner"], counting: 1});
            }
        }
    }
    const teamWin = [...teamsWinMap.values()];
    teamWin.sort((a, b) => b["counting"] - a["counting"]);

    const datachart = {
        labels: teamWin.map((team) => team.team).slice(0, 30),
        datasets: []
    }
    datachart.datasets.push({
        label: "Wins count",
        data: teamWin.map((team) => team.counting).slice(0, 30),
        borderColor: "#880f8d",
        backgroundColor: "#ba3dc0",
    });

    return datachart;
}
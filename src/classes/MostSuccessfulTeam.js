import data from "@/assets/data.json";
import {getAllCountryPlayers} from "@/classes/Utils";
import {Colors} from "chart.js";

export function getMostSuccessfulTeamOptions(){
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

export function getMostSuccessfulTeamData(gamesSelection, data){
    //team name -> team name, number of wins

    let teamsWinMap = new Map();
    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        for(let tournament of data[gamesSelection[i].id].tournaments){
            for(let team of tournament["teams"]) {
                if(teamsWinMap.has(team)) {
                    teamsWinMap.get(team).participating++;
                } else {
                    teamsWinMap.set(team, {team: team, participating: 1, counting: 0});
                }
            }
            if(teamsWinMap.has(tournament["team-winner"])) {
                teamsWinMap.get(tournament["team-winner"]).counting++;
            } else {
                teamsWinMap.set(tournament["team-winner"], {team: tournament["team-winner"], participating: 1, counting: 1});
            }
        }
    }
    let teamWin = [...teamsWinMap.values()]
        .filter((team) => team.participating > 1)
        .map((team) => {return{team : team.team, winrate: team.counting/team.participating*100}});
    teamWin.sort((a, b) => b["winrate"] - a["winrate"]);
    teamWin = teamWin.slice(0, 30);

    const datachart = {
        labels: teamWin.map((team) => team.team),
        datasets: []
    }
    datachart.datasets.push({
        label: "Team winrate (%)",
        data: teamWin.map((team) => team.winrate),
        borderColor: "#880f8d",
        backgroundColor: "#ba3dc0",
    });

    return datachart;
}
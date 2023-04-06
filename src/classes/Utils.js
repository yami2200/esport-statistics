export function getTimeRangeFromAllGames(gamesSelection, data){
    let min = 9999
    let max = 0
    for(let i = 0; i < gamesSelection.length; i++){
        if(!gamesSelection[i].selected) continue;
        const game = data[gamesSelection[i].id];
        const minGame = parseInt(game["time-range"].split("-")[0]);
        const maxGame = parseInt(game["time-range"].split("-")[1]);
        if(minGame < min) min = minGame;
        if(maxGame > max) max = maxGame;
    }
    max = Math.min(max, new Date().getFullYear()-1);
    return {min: min, max: max};
}

export function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

export function getAllCountryPlayers(data){
    let countries = new Set();
    let games = Object.keys(data);
    for(let i = 0; i < games.length; i++){
        const game = data[games[i]];
        let players = Object.keys(game.players);
        for (let p in players) {
            const player = players[p];
            countries.add(game.players[player].country);
        }
    }
    let result = Array.from(countries);
    result.sort()
    return result;
}
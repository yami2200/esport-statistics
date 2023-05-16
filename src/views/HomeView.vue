<script setup>
import data from "@/assets/data.json"
import {ref, shallowReactive} from 'vue'
import DataStats from "@/components/data-stats.vue";
import StatCardWrapper from "@/components/stat-card-wrapper.vue";
import LineChart from "@/components/charts/line-chart.vue";
import {getPlayerNationalityStatOptions, PlayerNationalityStatData} from "@/classes/PlayerNationalityStat";
import TextSelect from "@/components/inputs/text-select.vue";
import {getAllCountryPlayers} from "@/classes/Utils";
import BarChart from "@/components/charts/bar-chart.vue";
import PieChart from "@/components/charts/pie-chart.vue";
import {getRegionalDistributionData, getRegionalDistributionOptions} from "@/classes/RegionalDistribution";
import ModalDataInfo from "@/components/modal-data-info.vue";
import {getAgeRepartitionStatData, getPlayerAgeStatOptions} from "@/classes/AgeRepartition";
import {CashPrizeEvolution, getCashPrizeEvolutionOptions} from "@/classes/CashPrizeEvolution";
import {
    getRegionalDistributionWinningData,
    getRegionalDistributionWinningOptions
} from "@/classes/ApproxWinningPerCountry";
import {getPlayerBestPrizeData, getPlayerBestPrizeOptions} from "@/classes/PlayerBestPrize";
import {getMostAverageViewerTournament, getMostAverageViewerTournamentOptions} from "@/classes/MostAverageViewer";
import {getMostPeakViewerTournament, getMostPeakViewerTournamentOptions} from "@/classes/MostPeakViewer";
import {
    getAverageAverageViewerTournament,
    getAverageAverageViewerTournamentOptions
} from "@/classes/AverageAverageViewer";
import InfoNote from "@/components/notes/info-note.vue";

const countryList = getAllCountryPlayers(data);
const modal = ref(null)
const gamesKeys = Object.keys(data);
const games = gamesKeys.map((key) => data[key].name);
const gamesSelection = gamesKeys.map((key) => {return shallowReactive({name: data[key].name,
    id:key,
    selected: true,
    main_color: data[key]["main-color"],
    secondary_color: data[key]["secondary-color"]
});});
const settings = ref(null)

function getStarted(){
  window.scrollTo({top: settings.value.offsetTop-100, behavior: 'smooth'});
}

function updateGamesSelection(data){
    gamesSelection[data.index].selected = data.value;
}

function openModal(type, game){
    console.log(type, game);
    const title = data[game].name + " data " + type + " :";
    let dataToDisplay = [];
    let url = data[game].url;
    if(type === "players"){
        dataToDisplay = Object.keys(data[game].players).map((player) => {
            return {
                name: data[game].players[player].nickname,
                status: (data[game].players[player]["status-active"] ? "Active" : "Not active"),
                country: data[game].players[player]["country"]
            }
        })

    } else if(type === "tournaments"){
        url += "index.php?search="
        dataToDisplay = data[game].tournaments.map((tournament) => {
            return {
                name: tournament.name,
                "start-date": tournament["start-date"],
                location: tournament.location
            }
        });
    }
    modal.value.openModal(dataToDisplay, title, url)
}
</script>

<template>
  <main>
    <div class="hero" style="background-image: url(/background.jpg)">
      <div class="hero-overlay bg-opacity-60"></div>
      <div class="hero-content text-center text-neutral-content">
        <div class="max-w-md">
          <h1 class="mb-5 text-5xl font-bold text-white">E-sport Statistics !</h1>
          <p class="mb-5 text-white text-lg">This website provides a comprehensive collection of statistics and comparisons on various esports games. The site gathers its data from Liquipedia and presents it in an easily accessible and understandable format.</p>
          <button class="btn btn-primary" @click="getStarted">Get Started</button>
        </div>
      </div>
    </div>
    <modal-data-info ref="modal"></modal-data-info>
    <div ref="settings" class="wrappersettings">
      <div class="card w-screen-50 bg-base-300 shadow-xl mt-5 settings mb-5" style="padding-bottom: 50px;">
          <div v-for="(game) in gamesKeys" class="wrappersettings">
              <span class="text-3xl font-bold mt-5 mb-6 text-white"> {{data[game].name}} </span>
              <data-stats
                      @openModal="openModal($event, game)"
                      :players="Object.keys(data[game].players).length"
                      :tournaments="data[game].tournaments.length"
                      :note="'* '+data[game]['data-note']"
                      :time="data[game]['time-range']"
              ></data-stats>
          </div>
      </div>
      <div class="wrappersettings">
          <span class="text-5xl font-bold mt-6 mb-7 text-white "> 🌏 Nationality Section : </span>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Evolution of specific player nationality in tournaments"
                  subtitle="Tracking the Annual Count of Players from selected country in Major Tournaments."
                  @update-games-selection="updateGamesSelection"
          >
              <template #input="{setUserInput}">
                  <div class="input1">
                      <text-select inputid="country" title="Country : " :list="countryList" @setUserInput="setUserInput" defaultValue="France"></text-select>
                  </div>
              </template>
              <template #graph="{ userInput }">
                  <line-chart v-if="userInput.country" :chart-data="PlayerNationalityStatData(gamesSelection, data, userInput.country)" :chart-options="getPlayerNationalityStatOptions()"></line-chart>
              </template>
          </stat-card-wrapper>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Regional distribution of Esports players"
                  subtitle="Number of current and past players by country in tournaments history"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <bar-chart :chart-data="getRegionalDistributionData(gamesSelection, data)" :chart-options="getRegionalDistributionOptions()"></bar-chart>
              </template>
          </stat-card-wrapper>
          <span class="text-5xl font-bold mt-6 mb-7 text-white "> 🎂 Age Section : </span>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Age distribution of Esports players"
                  subtitle="Age of current players in the esport scene"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <pie-chart :chart-data="getAgeRepartitionStatData(gamesSelection, data)" :chart-options="getPlayerAgeStatOptions()"></pie-chart>
              </template>
          </stat-card-wrapper>
          <span class="text-5xl font-bold mt-6 mb-7 text-white "> 💸 CashPrize Section : </span>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Evolution of cash-prize in tournaments"
                  subtitle="Tracking the Sum of all cashprize in Major Tournaments. (dollars)"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <line-chart :chart-data="CashPrizeEvolution(gamesSelection, data)" :chart-options="getCashPrizeEvolutionOptions()"></line-chart>
              </template>
          </stat-card-wrapper>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Approx total Winnings of Esports players by Nationality"
                  subtitle="Sum of all cashprize won by players per country in Major Tournaments. (dollars)"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <bar-chart :chart-data="getRegionalDistributionWinningData(gamesSelection, data)" :chart-options="getRegionalDistributionWinningOptions()"></bar-chart>
              </template>
          </stat-card-wrapper>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Players with the higher approximate total winnings"
                  subtitle="Ranking of all players based on the total amount of money they won. (dollars)"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <bar-chart :chart-data="getPlayerBestPrizeData(gamesSelection, data)" :chart-options="getPlayerBestPrizeOptions()"></bar-chart>
              </template>
          </stat-card-wrapper>
          <span class="text-5xl font-bold mt-6 mb-7 text-white "> 🎞 Viewers Section : </span>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Top average viewers per year in tournaments"
                  subtitle="Display the top average viewers per year in all tournaments for each year"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <line-chart :chart-data="getMostAverageViewerTournament(gamesSelection, data)" :chart-options="getMostAverageViewerTournamentOptions()"></line-chart>
              </template>
              <template #note>
                  <info-note text="The data is not available for Counter Strike Global Offensive."></info-note>
              </template>
          </stat-card-wrapper>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Top peak viewers per year in tournaments"
                  subtitle="Display the top peak viewers per year from all tournaments for each year"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <line-chart :chart-data="getMostPeakViewerTournament(gamesSelection, data)" :chart-options="getMostPeakViewerTournamentOptions()"></line-chart>
              </template>
              <template #note>
                  <info-note text="The data is not available for Counter Strike Global Offensive."></info-note>
              </template>
          </stat-card-wrapper>
          <stat-card-wrapper
                  :games="gamesSelection"
                  title="Mean of Average viewers per year in all tournaments"
                  subtitle="Display the mean of average viewers per year of all tournaments for each year"
                  @update-games-selection="updateGamesSelection"
          >
              <template #graph>
                  <line-chart :chart-data="getAverageAverageViewerTournament(gamesSelection, data)" :chart-options="getAverageAverageViewerTournamentOptions()"></line-chart>
              </template>
              <template #note>
                  <info-note text="The data is not available for Counter Strike Global Offensive."></info-note>
              </template>
          </stat-card-wrapper>
      </div>
    </div>


  </main>
</template>

<style scoped>
  .hero {
    height: 85vh;
  }
  .wrappersettings{
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
  }
  .w-screen-50{
    width: 60vw;
  }
  .settings{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }
  .input1{
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      margin-bottom: 20px;
  }
</style>
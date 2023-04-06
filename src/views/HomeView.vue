<script setup>
import data from "@/assets/data.json"
import {ref, shallowReactive} from 'vue'
import DataStats from "@/components/data-stats.vue";
import StatCardWrapper from "@/components/stat-card-wrapper.vue";
import LineChart from "@/components/line-chart.vue";
import {PlayerNationalityStatData} from "@/classes/PlayerNationalityStat";
import TextSelect from "@/components/inputs/text-select.vue";
import {getAllCountryPlayers} from "@/classes/Utils";

const countryList = getAllCountryPlayers(data);
const gamesKeys = Object.keys(data);
const games = gamesKeys.map((key) => data[key].name);
const gamesSelection = gamesKeys.map((key) => {return shallowReactive({name: data[key].name,
    id:key,
    selected: true,
    main_color: data[key]["main-color"],
    secondary_color: data[key]["secondary-color"]
});});
const settings = ref(null)
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: false
        }
    }};
const datachart = {
    labels: ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
    datasets: [
        {
            label: 'Lol',
            data: [10, 20, {}, 51, 10],
            borderColor: "#d75050",
            backgroundColor: "#ce7c7c",
        },
        {
            label: 'RL',
            data: [5, 15, 35, 4, 20],
            borderColor: "#50aed7",
            backgroundColor: "#7cc7ce",
        }
    ]
}

function getStarted(){
  window.scrollTo({top: settings.value.offsetTop-100, behavior: 'smooth'});
}

function updateGamesSelection(data){
    gamesSelection[data.index].selected = data.value;
}
</script>

<template>
  <main>
    <div class="hero" style="background-image: url(/background.jpg)">
      <div class="hero-overlay bg-opacity-60"></div>
      <div class="hero-content text-center text-neutral-content">
        <div class="max-w-md">
          <h1 class="mb-5 text-5xl font-bold text-white">Hello there !</h1>
          <p class="mb-5 text-white text-lg">This website provides a comprehensive collection of statistics and comparisons on various esports games. The site gathers its data from Liquipedia and presents it in an easily accessible and understandable format.</p>
          <button class="btn btn-primary" @click="getStarted">Get Started</button>
        </div>
      </div>
    </div>
    <div ref="settings" class="wrappersettings">
      <div class="card w-screen-50 bg-base-300 shadow-xl mt-5 settings mb-5" style="padding-bottom: 50px;">
          <div v-for="(game) in gamesKeys" class="wrappersettings">
              <span class="text-3xl font-bold mt-5 mb-6 text-white"> {{data[game].name}} </span>
              <data-stats
                      :players="Object.keys(data[game].players).length"
                      :tournaments="data[game].tournaments.length"
                      :note="'* '+data[game]['data-note']"
                      :time="data[game]['time-range']"
              ></data-stats>
          </div>
      </div>
      <div class="h-screen">
          <!--<stat-card-wrapper
                  :games="gamesSelection"
                  title="Nationality of players"
                  @update-games-selection="updateGamesSelection"
          >
          </stat-card-wrapper>-->
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
                  <line-chart v-if="userInput.country" :chart-data="PlayerNationalityStatData(gamesSelection, data, userInput.country)" :chart-options="options"></line-chart>
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
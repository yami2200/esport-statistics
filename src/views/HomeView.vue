<script setup>
import data from "@/assets/data.json"
import { ref } from 'vue'
import DataStats from "@/components/data-stats.vue";
const gamesKeys = Object.keys(data);
const games = gamesKeys.map((key) => data[key].name);
const settings = ref(null)

function getStarted(){
  window.scrollTo({top: settings.value.offsetTop-100, behavior: 'smooth'});
}
</script>

<template>
  <main>
    <div class="hero" style="background-image: url(/src/assets/background.jpg)">
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
      <div class="card w-screen-50 bg-base-300 shadow-xl mt-5 settings mb-10" style="padding-bottom: 50px;">
          <div v-for="(game) in gamesKeys" class="wrappersettings">
              <span class="text-3xl font-bold mt-5 mb-6 text-white"> {{data[game].name}} </span>
              <data-stats
                      :players="data[game].players.length"
                      :tournaments="data[game].tournaments.length"
                      :note="'* '+data[game]['data-note']"
              ></data-stats>
          </div>
      </div>
      <div class="h-screen">

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
  .comparisonGameSettings{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
  }
  .nowrap {
    white-space: nowrap;
  }
</style>
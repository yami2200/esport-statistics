<script setup>
const games = ["League of Legends", "Counter Strike", "Rocket League", "Dota 2"];
</script>

<template>
  <main>
    <div class="hero" style="background-image: url(/src/assets/background.jpg)">
      <div class="hero-overlay bg-opacity-60"></div>
      <div class="hero-content text-center text-neutral-content">
        <div class="max-w-md">
          <h1 class="mb-5 text-5xl font-bold">Hello there !</h1>
          <p class="mb-5">This website provides a comprehensive collection of statistics and comparisons on various esports games. The site gathers its data from Liquipedia and presents it in an easily accessible and understandable format.</p>
          <button class="btn btn-primary">Get Started</button>
        </div>
      </div>
    </div>
    <div class="wrappersettings">
      <div class="alert shadow-lg mt-5 w-screen-50 bg-neutral">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <div>
            <h3 class="font-bold">Statistics Display !</h3>
            <div class="text-xs">Select which data you want to display :</div>
          </div>
        </div>
        <div class="flex-none">
          <div class="btn-group">
            <button class="btn btn-active">Specific Game Statistics</button>
            <button class="btn">Global Statistics</button>
          </div>
        </div>
      </div>
      <div class="card w-screen-50 bg-neutral shadow-xl mt-5 settings mb-10">
        <span class="mb-2 text-lg	">Game Statistics : </span>
        <select class="select select-primary w-full max-w-xs">
          <option v-for="game in games">{{game}}</option>
        </select>
        <div class="comparisonGameSettings mt-5">
          <div class="form-control">
            <label class="cursor-pointer label nowrap">
              <span class="label-text mr-3">Compare with :</span>
              <input type="checkbox" checked="checked" class="checkbox checkbox-secondary" />
            </label>
          </div>
          <select class="select select-secondary w-full max-w-xs ml-5">
            <option v-for="game in games">{{game}}</option>
          </select>
        </div>
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
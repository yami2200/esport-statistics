<template>
    <div class="card w-screen-50 bg-base-300 shadow-xl mt-2 settings mb-5">
        <span class="text-3xl font-bold mt-5 mb-1 text-white"> {{title}} </span>
        <span v-if="subtitle" class="w-full text-lg mt-3 mb-1 text-white" style="text-align: center!important"> {{subtitle}} </span>
        <div class="gridwrapper">
            <div class="stat">
                <slot name="input" :setUserInput="setUserInput"></slot>
                <slot name="graph" :userInput="userInput"></slot>
                <div class="mt-4">
                    <slot name="note"></slot>
                </div>
            </div>
            <div class="gameselector">
                <label v-for="(game, i) in games" class="label cursor-pointer">
                    <span class="label-text text-white">{{game.name}}</span>
                    <input type="checkbox" v-model="games[i].selected" @input="updateSelection($event, i)" class="checkbox checkbox-primary" />
                </label>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "stat-card-wrapper",
    data:() => ({
       userInput: {},
    }),
    props: {
        games: {
            type: Array,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        subtitle: {
            type: String,
            required: false
        }
    },
    methods:{
        updateSelection($event, index){
            this.$emit('update-games-selection', {index: index, value: $event.target.checked});
        },
        setUserInput(attribute, value){
            this.userInput[attribute] = value;
        }
    },
}
</script>

<style scoped>
.gridwrapper{
    display: grid;
    grid-template-columns: 75% 25%;
    grid-template-rows: 1fr;
    grid-gap: 10px;
    padding: 10px;
    width: 100%;
}
.stat{
    grid-column: 1;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
}
.gameselector{
    height: 100%;
    grid-column: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
}
.label{
    justify-content: right!important;
}
.label span{
    margin-right: 10px;
}
</style>
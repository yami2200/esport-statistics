<template>
    <div class="form-control">
        <label class="input-group input-group-md">
            <span class="bg-base-100 text-white text-lg">{{title}}</span>
            <select ref="select" class="select select-bordered text-white text-lg" @change="updateSelection">
                <option v-for="item in list">{{item}}</option>
            </select>
        </label>
    </div>
</template>

<script>
export default {
    name: "text-select",
    props:{
        title: {
            type: String,
            required: true
        },
        list:{
            type: Array,
            required: true
        },
        inputid:{
            type: String,
            required: true
        },
        defaultValue: {
            type: String,
            required: false
        }
    },
    methods:{
        updateSelection($event){
            console.log("send emit", this.inputid, $event.target.value);
            this.$emit('setUserInput', this.inputid,  $event.target.value);
        }
    },
    mounted() {
        if(this.defaultValue){
            this.$refs.select.value= this.defaultValue;
            this.$emit('setUserInput', this.inputid,  this.defaultValue);
        }
        else this.$emit('setUserInput', this.inputid,  this.list[0]);
    }
}
</script>

<style scoped>

</style>
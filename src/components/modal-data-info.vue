<template>
    <div>
        <input type="checkbox" id="my-modal-4" class="modal-toggle"/>
        <label for="my-modal-4" class="modal cursor-pointer text-center w-full">
            <label class="modal-box relative" for="" style="max-width: 70vw!important; max-height: 70vh;">
                <h1 class="text-3xl font-bold text-white">{{ title }}</h1>
                <input type="text" placeholder="Filter" class="input input-primary w-full max-w-xs mt-5 mb-5" v-model="filter" />
                <div class="overflow-x-auto" style="overflow-y: scroll!important; max-height: 40vh!important; height: 40vh!important;">
                    <table class="table table-compact w-full">
                        <thead>
                        <tr>
                            <th></th>
                            <th class="text-white">Name</th>
                            <th v-for="attribute in attributes" class="text-white"> {{attribute}}</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(element, i) in filteredData">
                            <th class="text-white">{{i+1}}</th>
                            <td class="text-blue-400">
                                <a :href="url+element.name" target="_blank">{{element.name}}</a>
                            </td>
                            <td v-for="attribute in attributes" class="text-white">
                                {{element[attribute]}}
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </label>
        </label>
    </div>
</template>

<script>
export default {
    name: "modal-data-info",

    data() {
        return {
            data: [],
            attributes: [],
            title: "",
            url : "",
            filter: ""
        }
    },

    computed:{
        filteredData(){
            return this.data.filter((element) => {
                return element.name.toLowerCase().includes(this.filter.toLowerCase());
            })
        }
    },

    methods: {
        openModal(data, title, url){
            document.getElementById('my-modal-4').checked = true;
            this.data = data;
            this.attributes = Object.keys(data[0]);
            this.attributes.splice(this.attributes.indexOf("name") ,1);
            this.title = title;
            this.url = url;
            this.filter = "";
        }
    }
}
</script>

<style scoped>

</style>
<template>
    <div>Work orders</div>
    <button @click="showTable">Show Table</button>
    <my-svg></my-svg>
    <my-table :tableData="tableData"></my-table>
</template>
    
<script>
    export default {
        name: "work-orders",
        
        data(){
            return {
            tableData: {},
            }
        },

        methods:{
            showTable(){
                fetch('http://127.0.0.1:8000/workOrders/').then((data)=>data.json()).then((data)=>this.tableData = data);
            }
        }

    }
</script>

<style scoped>

</style>
    
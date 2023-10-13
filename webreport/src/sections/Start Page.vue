<template>
  <h1>{{ date }}</h1>

  <button @click="updateData">show table WO</button>


</template>

<script>

  export default {
    name: "start-page",
    data(){
      return {
        date: (new Date(Date.now())).toLocaleString(),
        table: {}
      }
    },
    mounted() {
      setInterval(() => {
        let newDate = new Date(Date.now())
        this.date = newDate.toLocaleString()
      }, 1000);
    },
    methods:{
      updateData(){
        fetch('http://127.0.0.1:8000/workOrders/').then((data)=>data.json()).then((data)=>this.table = data);
      },
    }

  };
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>

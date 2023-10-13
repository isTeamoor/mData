<template>
  <div class="sideBar">
    <button @click="$router.push('/startPage')">Go to Start Page</button>
    <br><hr>
    <button @click="$router.push('/s-Curve')">S-Curve</button>
  </div>

  <div class="display">
    <router-view/>
  </div>
</template>

<script>
//<button @click="$router.push({name:'plan-fact', params:{id:0, section:'section'}})">Plan - Fact</button>
</script>



<style>
* {
  box-sizing: border-box;
  margin: 0;
}
#app {
    width:80%;
    height: 900px;
    margin: auto;
    border: 1px solid black;
}
.sideBar {
  display: inline-block;
  width: 20%;
  height: 100%;  
  border: 1px solid black;
  background: bisque;
}
.display {
  display: inline-block;
  width: 80%;
  height: 100%;  
  border: 1px solid black;
  background: aqua;
  vertical-align:top;
}
button {
  display: block;
  width: 100%;
}
</style>

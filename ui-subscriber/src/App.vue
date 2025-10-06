<template>
  <div id="app">
    <SubscriberNews />
  </div>
</template>

<script>
import SubscriberNews from "./components/SubscriberNews.vue";

export default {
  name: "App",
  components: { SubscriberNews },
};
</script>

<style>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #121212;
  color: white;
  margin: 0;
  padding: 0;
}
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>


<script setup>
import { reactive, ref } from 'vue';

const weatherInfo = reactive({
    Location: '',
    humidityPct: 0.0,
    windSpeed: 0.0
});

const backend = `http://backend:8001`;
async function  askWeatherRequest() {
const rawResultRequest = await fetch(`${backend}/predict_temperature`, {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify(weatherInfo),
});
document.getElementById("predictions").textContent =
JSON.stringify(await rawResultRequest.json(), null, 2);
};

const sentRequest = ref(false);
const temperature = ref(0.0)


function askWeather() {
    const res_request = askWeatherRequest();
    sentRequest.value = true;
    temperature.value = res_request;
}
</script>


<template>
<form @submit.prevent="askWeather">
        <label for="Location">Location</label>
        <select name="Location" id="Location" v-model="weatherInfo.Location">
            <option value="New York" >New York</option>
            <option value="Los Angeles" >Los Angeles</option>
            <option value="Chicago" >Chicago</option>
            <option value="Philadelphia" >Philadelphia</option>
            <option value="Dallas" >Dallas</option>
            <option value="Phoenix" >Phoenix</option>
            <option value="San Diego" >San Diego</option>
            <option value="San Antonio" >San Antonio</option>
            <option value="San Jose" >San Jose</option>
            <option value="Houston" >Houston</option>
        </select>
        <label for="humidity_pct">Humidity</label>
        <input id="humidity_pct" v-model="weatherInfo.humidityPct" type="number" step="0.01" max="100.0" min="0.0" inputmode="decimal" />
        <label for="wind_speed">Wind Speed in kilometer per hour</label>
        <input id="wind_speed" v-model="weatherInfo.windSpeed" typ="number" step="0.001" min="0.0" inputmode="decimal" />
    <button type="submit">Submit</button>
</form>
<p  v-if="!sentRequest">
    No value sent
</p>
<p v-else>
    {{ temperature }}
</p>
</template>


<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>

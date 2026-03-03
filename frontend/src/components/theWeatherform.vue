
<script setup>
import { reactive, ref } from 'vue';

const weatherInfo = reactive({
    humidityPct: 0.0,
    windSpeed: 0.0
});

// browser-side code cannot resolve the Docker service name `backend`;
// use an environment variable or fall back to the internal service address so
// that requests work from within a container. Vite prefixes environment
// variables with VITE_ so that they are exposed to the client bundle. See
// https://vitejs.dev/guide/env-and-mode.html
// during local development `npm run dev` the vite dev server proxies
// '/predict_temperature' to the backend; avoid hardcoding a host so the
// proxy can work. When the app is built in docker an environment variable
// is provided which will be used instead.
const backendEnv = import.meta.env.VITE_BACKEND_URL;
const backend = backendEnv || "";
async function  askWeatherRequest() {
  // choose relative path when no backend is configured
  const url = backend ? `${backend}/predict_temperature` : '/predict_temperature';
  const rawResultRequest = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // backend expects { features: [[humidity, wind_speed]] }
    body: JSON.stringify({
      features: [[weatherInfo.humidityPct, weatherInfo.windSpeed]],
    }),
  });
  if (!rawResultRequest.ok) {
    throw new Error(`HTTP ${rawResultRequest.status}`);
  }
  const result = await rawResultRequest.json();
  document.getElementById("predictions").textContent =
    JSON.stringify(result, null, 2);
  return result; // return parsed JSON for callers
};

const sentRequest = ref(false);
const temperature = ref(0.0)


async function askWeather() {
    try {
        const res = await askWeatherRequest();
        sentRequest.value = true;
        temperature.value = res ? res.predictions?.[0] : null;
    } catch (err) {
        console.error("API error:", err);
        sentRequest.value = true;
        temperature.value = `Error: ${err.message}`;
    }
}
</script>


<template>
<form @submit.prevent="askWeather">
        <label for="Location">Location</label>
        <select name="Location" id="Location">
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

<!-- area where request JSON is dumped -->
<pre id="predictions" class="mt-2"></pre>

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

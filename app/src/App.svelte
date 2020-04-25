<script>
  import { onMount } from 'svelte';

  let venues;

  async function loadVenues() {
  venues = await fetch("https://nifty-passkey-275314.uc.r.appspot.com/", {
    "method": "GET",
      "headers": {
        "content-type": "application/json"
      },
    })
    .then(response => response.json())
    .catch(err => {
      console.log(err);
    });
  }

  onMount(loadVenues);
</script>

<style lang="scss" global>
@import 'src/assets/scss/crowdcast.scss'; 
</style>

<main>
  <h1>Crowdcast</h1>
  <div>{JSON.stringify(venues, 2, null)}</div>
</main>

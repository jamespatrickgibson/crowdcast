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

<style lang="scss">
  @use "./src/assets/scss/variables" as *;

h1 {
color: $color;
}
</style>

<main>
  <h1>Crowdcast</h1>
  <div>{JSON.stringify(venues, 2, null)}</div>
</main>

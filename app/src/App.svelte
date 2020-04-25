<script>
  import { onMount } from "svelte";

  // Components
  import Header from "./components/Header.svelte";
  import VenueListItem from "./components/VenueListItem.svelte";

  let venues;

  async function loadVenues() {
    venues = await fetch(
      "https://nifty-passkey-275314.uc.r.appspot.com/venues?latitude=123.21&longitude=73.12&range=15",
      {
        method: "GET",
        headers: {
          "content-type": "application/json"
        }
      }
    )
      .then(response => response.json())
      .catch(err => {
        console.log(err);
      });
  }

  onMount(loadVenues);
</script>

<style lang="scss" global>
  @import "src/assets/scss/crowdcast.scss";
</style>

<main>
  <Header />

  {#if venues}
    <VenueListItem>
      <pre>{JSON.stringify(venues, null, 2)}</pre>
    </VenueListItem>
  {:else}
    <p>Loading</p>
  {/if}
</main>

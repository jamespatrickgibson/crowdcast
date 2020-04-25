<script>
  import { onMount } from "svelte";

  // Components
  import Box from "./components/Box.svelte";
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
    {#each venues as venue (venue.id)}
      <VenueListItem
        address="{venue.address}"
        name="{venue.name}"
        latitude="{venue.latitude}"
        longitude="{venue.longitude}"
        distance="{venue.distance}"
        timestamp="{venue.timestamp}"
        maxCapacity="{venue.max_capacity}"
        currentCapacity="{venue.current_capacity}"
        queueLength="{venue.queue_length}"
        queueWaitTime="{venue.queue_wait_time}"
      />
    {/each}
    <hr />
    <pre>{JSON.stringify(venues, null, 2)}</pre>
  {:else}
    <Box />
    <p>Loading</p>
  {/if}
</main>

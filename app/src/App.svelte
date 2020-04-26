<script>
  import { onMount } from "svelte";

  // Components
  import Box from "./components/Box.svelte";
  import Header from "./components/Header.svelte";
  import Text from "./components/Text.svelte";
  import Map from "./components/Map.svelte";
  import MapMarker from "./components/MapMarker.svelte";
  import VenueListItem from "./components/VenueListItem.svelte";

  let venues;

  async function loadVenues() {
    venues = await fetch(
      "https://nifty-passkey-275314.uc.r.appspot.com/venues",
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

  function isVenueFull(venue) {
    if (venue.current_capacity >= venue.max_capacity) {
      return true;
    }
    return false;
  }

  onMount(loadVenues);
</script>

<style lang="scss" global>
  @import "src/assets/scss/crowdcast.scss";
</style>

<main>
  <Header />
  <Map lat="{37.872}" lon="{-122.258}" zoom="{13}">
    {#if venues}
      {#each venues.results as venue (venue.id)}
        <MapMarker
          lat="{venue.latitude}"
          lon="{venue.longitude}"
          label="{venue.name}"
        />
      {/each}
    {/if}

  </Map>

  {#if venues}
    <Box space="2">
      {#each venues.results as venue (venue.id)}
        <VenueListItem
          address="{venue.address}"
          name="{venue.name}"
          latitude="{venue.latitude}"
          longitude="{venue.longitude}"
          distance="{venue.distance.toFixed(2)}"
          timestamp="{venue.timestamp}"
          maxCapacity="{venue.max_capacity}"
          openNow="{venue.open_now}"
          currentCapacity="{venue.current_capacity}"
          photoUrl="{venue.photo_url}"
          queueLength="{venue.queue_length}"
          queueWaitTime="{venue.queue_wait_time}"
          isFull="{isVenueFull(venue)}"
        />
      {/each}
    </Box>
    <!-- <hr />
    <pre>{JSON.stringify(venues.results, null, 2)}</pre> -->
  {:else}
    <Box>
      <Text>Loading</Text>
    </Box>
  {/if}
</main>

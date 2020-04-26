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
  @use "./src/assets/scss/utils/all" as *;
  @import "src/assets/scss/crowdcast.scss";

  main {
    @include desktop {
      position: fixed;
      top: var(--cc-size-height-header);
      right: 0;
      bottom: 0;
      left: 0;
      overflow: hidden;
      display: grid;
      grid-template-columns: 1fr 30rem;
    }
  }

  .venues-list {
    @include desktop {
      position: relative;
    }

    &__content {
      padding: var(--space-2);

      @include desktop {
        overflow: scroll;
        height: 100%;
        position: absolute;
        top: 0;
        right: 0;
        left: auto;
        width: 100%;
        padding: var(--space-3);
        padding-bottom: var(--cc-size-height-header);
      }
    }
  }
</style>

<Header />

<main>
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
    <div class="venues-list">
      <div class="venues-list__content">
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
      </div>
    </div>
    <hr />
    <!-- <pre>{JSON.stringify(venues, null, 2)}</pre> -->
  {:else}
    <Box>
      <Text>Loading</Text>
    </Box>
  {/if}
</main>

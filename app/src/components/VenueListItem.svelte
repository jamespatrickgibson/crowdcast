<script>
  export let address;
  export let currentCapacity;
  export let distance;
  export let name;
  export let latitude;
  export let longitude;
  export let timestamp;
  export let maxCapacity;
  export let queueLength;
  export let queueWaitTime;

  import Box from "./Box.svelte";
  import Text from "./Text.svelte";
</script>

<style>
  .venue-list-item {
    margin-bottom: var(--space-2);
  }
  .map-data {
    display: none;
  }
  .max-capacity {
    display: none;
  }
  .updated-time {
    display: none;
  }
</style>

<div class="venue-list-item">
  <Box background="white" radius="2" shadow="2">
    <Text size="5" variant="strong">{name}</Text>
    <Text size="2">{address}</Text>
    <Text size="1" variant="strong">{distance}mi Away</Text>

    <Text size="3">{currentCapacity} People There</Text>

    <div class="map-data">
      <Text size="1">Lat/Long {latitude} / {longitude}</Text>
    </div>
    <div class="updated-time">
      <Text size="2">Updated {timestamp}</Text>
    </div>
    <div class="max-capacity">
      <Text>{maxCapacity} Max Capacity</Text>
    </div>

    {#if queueWaitTime}
      <Text size="3">{queueLength} People In Line</Text>
      <Text size="2">{queueWaitTime} Minute Wait</Text>
    {:else}
      <Text size="2">No Wait!</Text>
    {/if}
  </Box>
</div>

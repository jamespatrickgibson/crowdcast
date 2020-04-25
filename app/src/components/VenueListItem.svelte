<script>
  import Box from "./Box.svelte";
  export let name;
  export let latitude;
  export let longitude;
  export let distance;
  export let timestamp;
  export let maxCapacity;
  export let currentCapacity;
  export let queueLength;
  export let queueWaitTime;
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;
</style>

<div>
  <Box>
    <p>{name}</p>
    <p>{latitude}</p>
    <p>{longitude}</p>
    <p>{distance}</p>
    <p>{timestamp}</p>
    <p>{maxCapacity}</p>
    <p>{currentCapacity}</p>
    <p>{queueLength}</p>
    <p>{queueWaitTime}</p>
  </Box>
</div>

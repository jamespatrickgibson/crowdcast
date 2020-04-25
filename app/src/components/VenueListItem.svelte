<script>
  import Box from "./Box.svelte";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;
</style>

<div>
  <Box>
    <slot />
  </Box>
</div>

<script>
  export let space = "3";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;
  .box {
    @each $size, $space in $spacers {
      &.has-space-#{$size} {
        padding: $space;
      }
    }
  }
</style>

<div
  class="box"
  class:has-space-1="{space === '1'}"
  class:has-space-2="{space === '2'}"
  class:has-space-3="{space === '3'}"
  class:has-space-4="{space === '4'}"
  class:has-space-5="{space === '5'}"
  class:has-space-6="{space === '6'}"
  class:has-space-7="{space === '7'}"
  class:has-space-8="{space === '8'}"
>
  <slot />
</div>

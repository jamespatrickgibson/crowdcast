<script>
  export let space = "3";
  export let background;
  export let radius = "0";
  export let shadow = "0";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;
  .box {
    // Spacing
    @each $size, $space in $spacers {
      &.has-space-#{$size} {
        padding: $space;
      }
    }

    // Radii
    @each $scale, $radius in $radii {
      &.has-radius-#{$scale} {
        border-radius: $radius;
      }
    }

    // Shadow
    @each $scale, $shadow in $shadows {
      &.has-shadow-#{$scale} {
        box-shadow: $shadow;
      }
    }

    // Backgrounds
    &.is-background-white {
      @include theme(white);
    }
    &.is-background-light {
      @include theme(light);
    }
    &.is-background-dark {
      @include theme(dark);
    }
    &.is-background-black {
      @include theme(black);
    }
    &.is-background-brand {
      @include theme(brand);
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
  class:is-background-white="{background === 'white'}"
  class:is-background-light="{background === 'light'}"
  class:is-background-dark="{background === 'dark'}"
  class:is-background-black="{background === 'black'}"
  class:is-background-brand="{background === 'brand'}"
  class:has-radius-1="{radius === '1'}"
  class:has-radius-2="{radius === '2'}"
  class:has-radius-3="{radius === '3'}"
  class:has-radius-4="{radius === '4'}"
  class:has-shadow-1="{shadow === '1'}"
  class:has-shadow-2="{shadow === '2'}"
  class:has-shadow-3="{shadow === '3'}"
  class:has-shadow-4="{shadow === '4'}"
>
  <slot />
</div>

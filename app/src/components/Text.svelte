<script>
  export let size = "4";
  export let variant = "";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .text {
    font-weight: var(--weight-medium);
    @each $number, $scale in $type-scale {
      &.is-size-#{$number} {
        font-size: $scale;
        line-height: var(--line-height-#{$number});
      }
    }

    // Variants
    &.is-strong {
      font-weight: var(--weight-bold);
    }
  }
</style>

<p
  class="text"
  class:is-size-1="{size === '1'}"
  class:is-size-2="{size === '2'}"
  class:is-size-3="{size === '3'}"
  class:is-size-4="{size === '4'}"
  class:is-size-5="{size === '5'}"
  class:is-size-6="{size === '6'}"
  class:is-size-7="{size === '7'}"
  class:is-size-8="{size === '8'}"
  class:is-size-9="{size === '9'}"
  class:is-size-10="{size === '10'}"
  class:is-size-11="{size === '11'}"
  class:is-size-12="{size === '12'}"
  class:is-strong="{variant === 'strong'}"
>
  <slot />
</p>

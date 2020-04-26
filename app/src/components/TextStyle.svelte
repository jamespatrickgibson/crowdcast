<script>
  export let tone = "neutral";
  export let caps;
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;
  .text-style {
    &.is-muted {
      color: var(--color-neutral-600);
    }
    &.is-subtle {
      color: var(--color-neutral-700);
    }
    &.is-brand {
      color: var(--color-primary-500);
    }
    &.is-uppercase {
      text-transform: uppercase;
    }
  }
</style>

<span
  class="text-style"
  class:is-neutral="{tone === 'neutral'}"
  class:is-muted="{tone === 'muted'}"
  class:is-subtle="{tone === 'subtle'}"
  class:is-brand="{tone === 'brand'}"
  class:is-strong="{tone === 'strong'}"
  class:is-uppercase="{caps === 'uppercase'}"
>
  <slot />
</span>

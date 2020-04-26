<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .tag {
    font-size: var(--type-scale-2);
    line-height: var(--line-height-3);
    font-weight: var(--weight-bold);
    background: var(--color-primary-050);
    color: var(--color-primary-300);
    display: inline-flex;
    padding: 0 var(--space-1);
    border-radius: var(--size-border-radius-2);
  }
</style>

<div class="tag">
  <slot />
</div>

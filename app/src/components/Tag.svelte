<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .tag {
    font-size: var(--type-scale-1);
    line-height: var(--line-height-3);
    font-weight: var(--weight-bold);
    background: var(--color-primary-050);
    color: var(--color-primary-400);
    display: inline-flex;
    align-items: center;
    padding: 0 var(--space-2);
    border-radius: var(--size-border-radius-2);
  }
</style>

<div class="tag">
  <slot />
</div>

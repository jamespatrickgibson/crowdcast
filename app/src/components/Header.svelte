<script>

</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .header {
    background: var(--color-neutral-100);
    height: grid-8pt(7);
    display: flex;
    align-items: center;
    padding: 0 var(--space-2);
  }

  .logo {
    font-weight: var(--weight-bold);
    // text-transform: uppercase;
    font-size: var(--type-scale-5);
    // line-height: baseline(6);
    background: pink;
  }
</style>

<header class="header">
  <div class="logo">Crowdcast</div>
</header>

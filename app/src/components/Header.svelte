<script>

</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .header {
    // https://www.toptal.com/designers/subtlepatterns/patterns/memphis-mini-dark.png
    background-image: url("./memphis-mini-dark.png"),
      linear-gradient(
        var(--color-background-brand),
        var(--color-background-brand)
      );
    background-blend-mode: screen;
    color: var(--color-text-on-brand);
    height: grid-8pt(9);
    display: flex;
    align-items: center;
    padding: var(--space-3) var(--space-3) 0 var(--space-3);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
  }

  .logo {
    font-weight: var(--weight-bold);
    text-transform: lowercase;
    font-size: var(--type-scale-6);
    line-height: baseline(5);
    color: var(--color-white);
  }
</style>

<header class="header">
  <div class="logo">Crowdcast</div>
</header>

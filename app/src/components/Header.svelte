<script>

</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .header {
    // https://www.toptal.com/designers/subtlepatterns/patterns/prism.png
    // https://www.toptal.com/designers/subtlepatterns/patterns/webb.png
    // https://www.toptal.com/designers/subtlepatterns/patterns/double-bubble-dark.png
    // https://www.toptal.com/designers/subtlepatterns/patterns/memphis-mini-dark.png
    background-image: url("https://www.toptal.com/designers/subtlepatterns/patterns/memphis-mini-dark.png"),
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
    position: sticky;
    top: 0;
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

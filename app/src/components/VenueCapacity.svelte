<script>
  export let maximum;
  export let current;

  function fullness() {
    let degree = current / maximum;

    if (degree === 0) {
      return "Empty";
    } else if (degree > 0 && degree < 0.25) {
      return "Plenty of Room";
    } else if (degree > 0.26 && degree < 0.5) {
      return "Picking Up";
    } else if (degree > 0.51 && degree < 0.75) {
      return "Getting Busier";
    } else if (degree > 0.76 && degree < 0.9) {
      return "Almost Full";
    } else {
      return "Packed";
    }
  }

  import Stack from "./Stack.svelte";
  import Text from "./Text.svelte";
  import TextStyle from "./TextStyle.svelte";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  $venue-capacity-bar-color: var(--color-neutral-300);
  $venue-capacity-value-color: var(--color-primary-400);

  .venue-capacity {
    progress {
      apperance: none;
      border: none;
      border-radius: 290486px;
      display: block;
      height: var(--space-2);
      overflow: hidden;
      padding: 0;
      width: 100%;

      &::-webkit-progress-bar {
        // background-color: $venue-capacity-bar-color;
        background-image: linear-gradient(
          to right,
          var(--color-neutral-200),
          var(--color-neutral-400)
        );
      }

      &::-webkit-progress-value {
        background-image: linear-gradient(
          to right,
          var(--color-primary-300),
          var(--color-primary-600)
        );
      }

      &::-moz-progress-bar {
        background-image: linear-gradient(
          to right,
          var(--color-primary-300),
          var(--color-primary-600)
        );
      }

      &::-ms-fill {
        background-image: linear-gradient(
          to right,
          var(--color-primary-300),
          var(--color-primary-600)
        );
        border: none;
      }
    }
  }
</style>

<div class="venue-capacity">
  <Stack space="1">
    <progress value="{current}" max="{maximum}"></progress>
    <Text size="3" variant="strong">
      <TextStyle tone="brand">{fullness()}</TextStyle>
    </Text>
  </Stack>
</div>

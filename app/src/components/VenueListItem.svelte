<script>
  export let address;
  export let currentCapacity;
  export let distance;
  export let name;
  export let latitude;
  export let longitude;
  export let timestamp;
  export let maxCapacity;
  export let openNow = false;
  export let photoUrl;
  export let queueLength;
  export let queueWaitTime;
  export let isFull = false;

  import Box from "./Box.svelte";
  import Tag from "./Tag.svelte";
  import Text from "./Text.svelte";
  import TextStyle from "./TextStyle.svelte";
  import Stack from "./Stack.svelte";
  import VenueCapacity from "./VenueCapacity.svelte";
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .venue-list-item {
    margin-bottom: var(--space-2);
    display: grid;
    grid-template-columns: 8rem 1fr;
    @include theme(white);
    border-radius: var(--size-border-radius-3);
    overflow: hidden;
    box-shadow: $shadow-3;

    &__image {
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    &__content {
      padding: var(--space-3);
    }
  }
</style>

<div class="venue-list-item">
  <figure class="venue-list-item__image">
    <img src="{photoUrl}" alt="{name}" loading="lazy" />
  </figure>
  <div class="venue-list-item__content">
    <Stack space="3">
      {#if openNow}
        <Tag>Open Now</Tag>
      {/if}

      <div>
        <Text size="5" variant="strong">{name}</Text>
        <Text size="2">{address}</Text>
        <Text size="1" variant="strong">
          <TextStyle tone="muted">{distance}mi Away</TextStyle>
        </Text>
      </div>

      {#if queueWaitTime && isFull}
        <Text size="3">Currently Full</Text>
        <Text size="3">{queueLength} People In Line</Text>
        <Text size="2">{queueWaitTime} Minute Wait</Text>
      {:else}
        <VenueCapacity current="{currentCapacity}" maximum="{maxCapacity}" />
      {/if}
    </Stack>
  </div>
</div>

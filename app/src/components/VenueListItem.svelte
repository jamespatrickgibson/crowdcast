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

    &__status {
      display: flex;
      align-items: center;
      height: grid-8pt(3);
    }

    &__wait-time {
      height: grid-8pt(4);
      padding-top: grid-8pt(1);
    }

    &__capacity {
      height: grid-8pt(7);
      padding-top: grid-8pt(2);
    }
  }
</style>

<div class="venue-list-item" class:is-full="{isFull}">
  <figure class="venue-list-item__image">
    <img src="{photoUrl}" alt="{name}" loading="lazy" />
  </figure>
  <div class="venue-list-item__content">
    <Stack space="2">

      <!-- Venue Info -->
      <div>
        <Text size="4" variant="strong">{name}</Text>
        <Text size="2">{address}</Text>
        <Text size="1" variant="strong">
          <TextStyle tone="muted">{distance}mi Away</TextStyle>
        </Text>
      </div>

      <!-- Venue Status -->
      {#if queueWaitTime && isFull}
        <div class="venue-list-item__status">
          <!-- {#if openNow}
          <Tag>Open Now</Tag>
        {/if} -->

          <Tag>Currently Full</Tag>
        </div>
      {/if}

      {#if queueWaitTime && isFull}
        <div class="venue-list-item__wait-time">
          <Text size="2" variant="strong">
            About a {queueWaitTime} Minute Wait
          </Text>
          <Text size="1" variant="strong">
            <TextStyle tone="muted">{queueLength} People In Line</TextStyle>
          </Text>
        </div>
      {:else}
        <div class="venue-list-item__capacity">
          <VenueCapacity current="{currentCapacity}" maximum="{maxCapacity}" />
        </div>
      {/if}
    </Stack>
  </div>
</div>

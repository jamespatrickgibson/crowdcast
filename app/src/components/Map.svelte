<script>
  import { onMount, setContext } from "svelte";
  import { mapbox, key } from "./mapbox.js";

  setContext(key, {
    getMap: () => map
  });

  export let lat;
  export let lon;
  export let zoom;

  let container;
  let map;

  onMount(() => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://unpkg.com/mapbox-gl/dist/mapbox-gl.css";

    link.onload = () => {
      map = new mapbox.Map({
        container,
        style: "mapbox://styles/mapbox/streets-v9",
        center: [lon, lat],
        zoom: 13
      });
    };

    document.head.appendChild(link);

    return () => {
      map.remove();
      link.parentNode.removeChild(link);
    };
  });
</script>

<style lang="scss">
  @use "./src/assets/scss/utils/all" as *;

  .venue-map {
    width: 100%;
    height: 30vh;
    z-index: -1;
    @include desktop {
      z-index: -1;
      height: 100vh;
    }
  }
</style>

<div class="venue-map" bind:this="{container}">
  {#if map}
    <slot />
  {/if}
</div>

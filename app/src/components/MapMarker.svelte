<script>
  import { getContext } from "svelte";
  import { mapbox, key } from "./mapbox.js";
  import Text from "./Text.svelte";

  const { getMap } = getContext(key);
  const map = getMap();

  export let lat;
  export let lon;
  export let label;
  export let image;

  let desc = `<img width="100%" src="${image}"/><strong>${label}</strong>`;

  // const popup = new mapbox.Popup({ offset: 25 }).setText(label);
  const popup = new mapbox.Popup({ offset: 25 })
    .setHTML(desc)
    .setMaxWidth("30vw");

  const marker = new mapbox.Marker()
    .setLngLat([lon, lat])
    .setPopup(popup)
    .addTo(map);
</script>

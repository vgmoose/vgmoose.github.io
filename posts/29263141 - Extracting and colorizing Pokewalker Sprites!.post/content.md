---
layout: post
title: Extracting and colorizing Pokewalker Sprites!
date: 2025-08-21 11:01:00
comments: true
categories: pokemon, reverse engineering, pokewalker, revamped, spriting
id: 2307083881
---

The [Pokewalker](https://bulbapedia.bulbagarden.net/wiki/Pokéwalker) is a handheld pedometer that came bundled with HGSS, and it has a bunch of [two-frame grayscale sprites](https://archives.bulbagarden.net/wiki/Category:Pokéwalker_Pokémon_sprites). The sprites used on the walker are taken from Diamond/Pearl and positioned so that they'll fit on the small display, but lack any color information.

Below are the original grayscale Pokewalker sprites (with transparency), and their now fully colorized counterparts. Drag the slider to see the difference, or click one of these direct links: [Grayscale](./pwalk_gray.png) - [Color](./pwalk_color.png) (Slider code from [this post](https://muffinman.io/blog/image-comparison-slider/)):

<div class="comparison-slider" aria-label="Image comparison slider showing [image 1 description] and [image 2 description]. Use the slider to compare the images.">
  <div class="compare" style="overflow: visible;">
    <img class="compare__image-one" alt="Grayscale (original) Pokewalker sprites" src="./pwalk_gray.png" />
      <div class="compare__mask">
        <img class="compare__image-two" alt="Colorized Pokewalker sprites" src="./pwalk_color.png" />
      </div>
    <div class="compare__separator">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" class="compare__icon" viewBox="0 0 16 16">
        <path d="M 6 2 L 1 8 L 6 14 M 10 2 L 15 8 L 10 14" stroke="currentColor"></path>
      </svg>
    </div>
    <input class="compare__input" type="range" min="0" step="0.5" max="100" value="50" />
  </div>
</div>

In 2020, [Dmitry.GR posted some information](https://dmitry.gr/?r=01.Myself&proj=06.Work) on reverse engineering the protocol, as well as the sprite format used by the device. These sprites are not actually stored on the walker though! HG/SS transfer them over to the Pokewalker each time that you sync with it. These sprites can be extracted from the HG/SS DS ROM.

Then, the original full-color Diamond/Pearl sprites can be exgtracted and aligned with these grayscale counterparts, to create an accurate representation of what the images would have looked like if they were colored from the start.

Some code used in this effort is here: https://github.com/vgmoose/pypokescript

I didn't yet go through all the alternate forms, but that might be a goal in the future. As for _why_ do this with the sprites, maybe they could be useful in creating full-color recreation of the pokewalker. Or adding a color overlay to a Pokewalker emulator!


<style>
.compare {
  --mask-width: 50%;
  --handle-size: 16px;

  position: relative;
  border: 1px solid rgb(0 0 0 / 0.05);
}

.compare__separator {
  position: absolute;
  top: 0;
  height: 100%;
  left: var(--mask-width);
  width: 2px;
  margin-left: -1px;
  background: black;
  z-index: 1;
  pointer-events: none;
}

.compare__image-one {
  width: 100%;
  display: block;
  pointer-events: auto; /* Allow interaction */
  user-drag: none;
  -webkit-user-drag: none;
  -khtml-user-drag: none;
  -moz-user-drag: none;
  -o-user-drag: none;
}

.compare__mask {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 1;
  background: white;
  overflow: hidden;
  width: var(--mask-width);
}

.compare__image-two {
  height: 100%;
  width: auto;
  pointer-events: auto; /* Allow interaction */
  user-drag: none;
  -webkit-user-drag: none;
  -khtml-user-drag: none;
  -moz-user-drag: none;
  -o-user-drag: none;
}

#content .compare__mask img {
    max-width: unset;
}

.compare__input {
  appearance: none;
  -webkit-appearance: none;
  -webkit-tap-highlight-color: transparent;
  position: absolute;
  top: 0;
  left: calc(var(--handle-size) / -2);
  width: calc(100% + var(--handle-size));
  height: 100%;
  opacity: 0;
  z-index: -1; /* Move behind everything */
  cursor: col-resize;
  background-color: transparent;
  pointer-events: none; /* Disable all pointer events */
}

/* Firefox */
.compare__input::-moz-range-track {
  height: 100%;
}

.compare__input::-moz-range-thumb {
  height: 100%;
  border-radius: 0;
  width: var(--handle-size);
  border: none;
}

/* Webkit */
.compare__input::-webkit-slider-runnable-track {
  height: 100%;
}

.compare__input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  height: 100%;
  border-radius: 0;
  width: var(--handle-size);
  border: none;
}

.compare__icon {
  position: absolute;
  z-index: 2;
  color: #333;
  width: var(--handle-size);
  height: var(--handle-size);
  top: 50%;
  left: var(--mask-width);
  transform: translate(-50%, -50%);
  padding: 6px;
  border: 2px solid currentColor;
  border-radius: 50%;
  background: rgba(255, 255, 255, 1);
}

.compare__icon path {
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2px;
}
</style>
<script>
  document.body.onload = function() {
    const compare = document.querySelector(".compare");
    const input = document.querySelector(".compare input");
    const separator = document.querySelector(".compare__separator");
    const images = compare.querySelectorAll("img");

    let isDragging = false;

    console.log("Slider initialized, found", images.length, "images");

    // Prevent image dragging but allow right-click
    images.forEach((img, index) => {
      img.addEventListener("dragstart", (e) => {
        console.log("Preventing drag on image", index);
        e.preventDefault();
      });

      // Handle mouse events directly on images
      img.addEventListener("mousedown", (e) => {
        console.log("Image mousedown, button:", e.button);
        if (e.button === 0) { // Left mouse button only
          isDragging = true;
          updateSlider(e);
          e.preventDefault(); // Prevent text selection
          e.stopPropagation(); // Prevent event from bubbling
        }
      });

      img.addEventListener("contextmenu", (e) => {
        console.log("Context menu on image", index);
        // Allow right-click context menu - don't prevent default
      });
    });

    function updateSlider(e) {
      console.log("Updating slider, mouse X:", e.clientX);
      const rect = compare.getBoundingClientRect();
      const percent = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100));
      console.log("New percentage:", percent);
      input.value = percent;
      compare.style.setProperty("--mask-width", `${percent}%`);
    }

    // Fallback: Handle mouse events on the entire compare container
    compare.addEventListener("mousedown", (e) => {
      console.log("Compare container mousedown, button:", e.button);
      if (e.button === 0 && !isDragging) { // Left mouse button only
        isDragging = true;
        updateSlider(e);
        e.preventDefault();
      }
    });

    document.addEventListener("mousemove", (e) => {
      if (isDragging) {
        updateSlider(e);
      }
    });

    document.addEventListener("mouseup", (e) => {
      if (isDragging) {
        console.log("Mouse up, stopping drag");
        isDragging = false;
      }
    });

    // Set initial position
    compare.style.setProperty("--mask-width", `${input.value}%`);
    console.log("Initial mask width set to:", input.value + "%");
  }
</script>
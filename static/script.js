const form = document.getElementById("controls");
const fileInput = document.getElementById("image");
const overlayInput = document.getElementById("overlay");
const animationTypeInput = document.getElementById("animation_type");
const framesInput = document.getElementById("frames");
const durationInput = document.getElementById("frame_duration");
const colorInput = document.getElementById("bgcolor");
const transparentBgCheckbox = document.getElementById("transparent-bg");
const statusEl = document.getElementById("status");
const outputImg = document.getElementById("gif-output");
const downloadLink = document.getElementById("download-link");

let debounceTimer = null;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.className = isError ? "status error" : "status";
}

function clampValue(value, min, max, fallback) {
  const num = Number(value);
  if (Number.isNaN(num)) return fallback;
  return Math.min(Math.max(num, min), max);
}

async function generateGif() {
  const [file] = fileInput.files;
  if (!file) {
    setStatus("Select an image to start generating.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);
  
  // Add overlay image if present
  const [overlayFile] = overlayInput.files;
  if (overlayFile) {
    formData.append("overlay", overlayFile);
  }
  
  formData.append("animation_type", animationTypeInput.value);
  formData.append("frames", clampValue(framesInput.value, 2, 240, 24));
  formData.append("frame_duration", clampValue(durationInput.value, 10, 5000, 50));
  
  // Use transparent background if checkbox is checked
  const bgColor = transparentBgCheckbox.checked ? "transparent" : (colorInput.value || "#000000");
  formData.append("bgcolor", bgColor);

  setStatus("Generating GIF...");

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.error || "Request failed");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    
    // Revoke old URL if it exists
    if (outputImg.src.startsWith('blob:')) {
      URL.revokeObjectURL(outputImg.src);
    }
    
    outputImg.src = url;
    outputImg.style.display = "block";
    downloadLink.href = url;
    downloadLink.style.display = "inline-block";
    setStatus("GIF updated.");
  } catch (err) {
    console.error(err);
    setStatus(err.message || "Something went wrong", true);
  }
}

function triggerAutoGenerate() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(generateGif, 400); // 400ms debounce
}

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    generateGif();
  }
});

// Regenerate when overlay image changes
overlayInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    generateGif();
  }
});

[animationTypeInput, framesInput, durationInput, colorInput].forEach((input) => {
  input.addEventListener("input", triggerAutoGenerate);
});

// Handle transparent background checkbox
transparentBgCheckbox.addEventListener("change", () => {
  colorInput.disabled = transparentBgCheckbox.checked;
  if (fileInput.files.length > 0) {
    triggerAutoGenerate();
  }
});

// Provide an initial hint
setStatus("Select an image to begin.");

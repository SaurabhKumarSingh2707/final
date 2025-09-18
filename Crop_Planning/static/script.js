document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("crop-form");
  const resultContainer = document.getElementById("result-container");
  const resultText = document.getElementById("result-text");
  const guideContainer = document.getElementById("guide-container");
  const guideTitle = document.getElementById("guide-title");
  const guideTimeline = document.getElementById("guide-timeline");
  const guideHowToPlant = document.getElementById("guide-how-to-plant");
  const guideFertilizer = document.getElementById("guide-fertilizer");
  const guideIdealRainfall = document.getElementById("guide-ideal-rainfall");
  const guidePostHarvest = document.getElementById("guide-post-harvest");

  // Form submission is handled below after validation setup

  // Crop recommendation system is handled in form submission below
});

let scene, camera, renderer, particles;

function initThreeJS() {
  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 50;

  renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById("three-canvas"),
    alpha: true,
    antialias: true,
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 0);

  createParticles();

  animate();

  window.addEventListener("resize", onWindowResize);
}

function createParticles() {
  const geometry = new THREE.BufferGeometry();
  const particleCount = 100;

  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);

  const greenColor = new THREE.Color(0x2e7d32);
  const lightGreenColor = new THREE.Color(0x4caf50);

  for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3;

    positions[i3] = (Math.random() - 0.5) * 200;
    positions[i3 + 1] = (Math.random() - 0.5) * 200;
    positions[i3 + 2] = (Math.random() - 0.5) * 100;

    const color = Math.random() > 0.5 ? greenColor : lightGreenColor;
    colors[i3] = color.r;
    colors[i3 + 1] = color.g;
    colors[i3 + 2] = color.b;
  }

  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: 2,
    vertexColors: true,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending,
  });

  particles = new THREE.Points(geometry, material);
  scene.add(particles);
}

function animate() {
  requestAnimationFrame(animate);

  if (particles) {
    particles.rotation.x += 0.001;
    particles.rotation.y += 0.002;
  }

  renderer.render(scene, camera);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener("load", initThreeJS);

const form = document.getElementById("crop-form");
const progressBar = document.getElementById("progress-bar");
const submitBtn = document.getElementById("submit-btn");
const resultContainer = document.getElementById("result-container");

function updateProgress() {
  const inputs = form.querySelectorAll("input[required], select[required]");
  const filled = Array.from(inputs).filter(
    (input) => input.value.trim() !== ""
  ).length;
  const progress = (filled / inputs.length) * 100;
  progressBar.style.width = progress + "%";
}

form.addEventListener("input", updateProgress);
form.addEventListener("change", updateProgress);

function validateField(field) {
  const formGroup = field.closest(".form-group");
  const isValid = field.value.trim() !== "" && field.checkValidity();

  formGroup.classList.remove("error", "success");
  if (field.value.trim() !== "") {
    formGroup.classList.add(isValid ? "success" : "error");
  }

  return isValid;
}

form.querySelectorAll("input, select").forEach((field) => {
  field.addEventListener("blur", () => validateField(field));
  field.addEventListener("input", () => {
    if (field.closest(".form-group").classList.contains("error")) {
      validateField(field);
    }
  });
});

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const fields = form.querySelectorAll("input[required], select[required]");
  let isValid = true;

  fields.forEach((field) => {
    if (!validateField(field)) {
      isValid = false;
    }
  });

  if (!isValid) {
    const firstError = form.querySelector(".form-group.error");
    if (firstError) {
      firstError.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    return;
  }

  submitBtn.innerHTML = '<span class="loading"></span> Analyzing Your Farm...';
  submitBtn.disabled = true;

  setTimeout(() => {
    // Get form data for intelligent crop recommendation
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      const el = document.getElementsByName(key)[0];
      data[key] = el.type === "number" ? parseFloat(value) : value;
    });

    // Intelligent crop recommendation based on conditions
    const recommendedCrop = getRecommendedCrop(data);

    document.getElementById("result-text").textContent = recommendedCrop.name;
    document.getElementById(
      "guide-title"
    ).textContent = `Complete Growing Guide for ${recommendedCrop.name}`;

    document.getElementById("guide-timeline").innerHTML = recommendedCrop.timeline;
    document.getElementById("guide-how-to-plant").innerHTML = recommendedCrop.howToPlant;
    document.getElementById("guide-fertilizer").innerHTML = recommendedCrop.fertilizer;
    document.getElementById("guide-ideal-rainfall").innerHTML = recommendedCrop.idealRainfall;
    document.getElementById("guide-post-harvest").innerHTML = recommendedCrop.postHarvest;

    resultContainer.classList.remove("hidden");
    resultContainer.scrollIntoView({ behavior: "smooth" });

    submitBtn.innerHTML = "Get Full Farming Plan";
    submitBtn.disabled = false;
  }, 2000);
});

// Intelligent crop recommendation function
function getRecommendedCrop(data) {
  const { pH, Temperature, Rainfall, Soil_Type, Season, Market_Demand, Fertilizer_Used, Pest_Issue, Irrigation_Method } = data;
  
  // Expanded crop database with growing conditions
  const crops = {
    wheat: {
      name: "Wheat",
      conditions: { minPH: 6.0, maxPH: 7.5, minTemp: 15, maxTemp: 25, minRain: 300, maxRain: 750, seasons: ["Winter"], soils: ["Loamy", "Clay"] },
      timeline: "<strong>Planting:</strong> November-December<br><strong>Harvest:</strong> March-April (120-150 days)<br><strong>Best Time:</strong> Rabi season",
      howToPlant: "• Prepare field with deep plowing<br>• Seed rate: 100-125 kg/hectare<br>• Sowing depth: 3-5 cm<br>• Row spacing: 20-23 cm<br>• Apply basal fertilizer before sowing",
      fertilizer: "<strong>Basal:</strong> DAP 100 kg/ha<br><strong>Top dressing:</strong> Urea 50 kg at tillering, 50 kg at heading<br><strong>Micronutrients:</strong> Zinc sulphate 25 kg/ha",
      idealRainfall: "<strong>Total:</strong> 450-650 mm<br><strong>Critical stages:</strong> Crown root initiation, tillering, grain filling<br><strong>Irrigation:</strong> 4-6 irrigations needed",
      postHarvest: "• Harvest at 20-25% moisture<br>• Dry to 12% moisture for storage<br>• Store in cool, dry place<br>• Market timing: April-May for best prices"
    },
    rice: {
      name: "Rice",
      conditions: { minPH: 5.5, maxPH: 7.0, minTemp: 20, maxTemp: 35, minRain: 1000, maxRain: 2500, seasons: ["Monsoon"], soils: ["Clay", "Loamy"] },
      timeline: "<strong>Planting:</strong> June-July (Kharif)<br><strong>Harvest:</strong> November-December (120-140 days)<br><strong>Transplanting:</strong> 20-25 days after sowing",
      howToPlant: "• Prepare nursery beds<br>• Seed rate: 20-25 kg/hectare<br>• Transplant 2-3 seedlings per hill<br>• Spacing: 20x15 cm<br>• Maintain 2-5 cm water level",
      fertilizer: "<strong>NPK:</strong> 120:60:40 kg/ha<br><strong>Application:</strong> 50% N basal, 25% at tillering, 25% at panicle initiation<br><strong>Organic:</strong> 5-10 tonnes FYM/ha",
      idealRainfall: "<strong>Total:</strong> 1200-1800 mm<br><strong>Distribution:</strong> Well-distributed throughout season<br><strong>Water depth:</strong> 2-5 cm in field",
      postHarvest: "• Harvest at proper maturity (80% grains golden)<br>• Dry to 14% moisture<br>• Store in moisture-proof containers<br>• Market: November-February"
    },
    cotton: {
      name: "Cotton",
      conditions: { minPH: 6.0, maxPH: 8.0, minTemp: 20, maxTemp: 35, minRain: 500, maxRain: 1000, seasons: ["Monsoon", "Summer"], soils: ["Black", "Loamy"] },
      timeline: "<strong>Planting:</strong> April-June<br><strong>Harvest:</strong> October-January (150-180 days)<br><strong>Picking:</strong> Multiple harvests",
      howToPlant: "• Deep plowing and field preparation<br>• Seed rate: 1.5-2.5 kg/hectare<br>• Spacing: 90-120 cm between rows<br>• Plant 2-3 seeds per hill<br>• Maintain plant population 55,000-75,000/ha",
      fertilizer: "<strong>NPK:</strong> 100:50:50 kg/ha<br><strong>Split application:</strong> 25% at sowing, 50% at squaring, 25% at flowering<br><strong>Micronutrients:</strong> Boron, Zinc application",
      idealRainfall: "<strong>Total:</strong> 600-800 mm<br><strong>Distribution:</strong> 75% during vegetative growth<br><strong>Dry period:</strong> Required during boll opening",
      postHarvest: "• First picking at 60% boll opening<br>• Multiple pickings every 15 days<br>• Proper drying and ginning<br>• Store in moisture-free environment"
    },
    tomato: {
      name: "Tomato",
      conditions: { minPH: 6.0, maxPH: 7.0, minTemp: 18, maxTemp: 29, minRain: 400, maxRain: 800, seasons: ["Winter", "Summer"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> October-November (Winter), February-March (Summer)<br><strong>Harvest:</strong> 90-120 days<br><strong>Transplanting:</strong> 4-5 weeks after sowing",
      howToPlant: "• Raise seedlings in nursery<br>• Transplant at 4-5 leaf stage<br>• Spacing: 60x45 cm<br>• Provide support with stakes<br>• Mulching recommended",
      fertilizer: "<strong>NPK:</strong> 150:100:100 kg/ha<br><strong>Application:</strong> 50% basal, remaining in splits<br><strong>Organic:</strong> 20-25 tonnes FYM/ha<br><strong>Calcium:</strong> For preventing blossom end rot",
      idealRainfall: "<strong>Total:</strong> 500-750 mm<br><strong>Distribution:</strong> Avoid excess during flowering<br><strong>Irrigation:</strong> Drip irrigation preferred<br><strong>Water requirement:</strong> 400-600 mm",
      postHarvest: "• Harvest at breaker stage<br>• Multiple harvests every 3-4 days<br>• Cool storage at 12-15°C<br>• Market within 7-10 days for fresh market"
    },
    maize: {
      name: "Maize",
      conditions: { minPH: 6.0, maxPH: 7.5, minTemp: 20, maxTemp: 35, minRain: 400, maxRain: 800, seasons: ["Monsoon", "Summer"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> June-July (Kharif), February-March (Rabi)<br><strong>Harvest:</strong> 90-120 days<br><strong>Silking:</strong> 55-65 days",
      howToPlant: "• Field preparation with deep plowing<br>• Seed rate: 18-20 kg/hectare<br>• Spacing: 60x20 cm<br>• Depth: 3-4 cm<br>• Gap filling within 10 days",
      fertilizer: "<strong>NPK:</strong> 120:60:40 kg/ha<br><strong>Nitrogen splits:</strong> 1/3 basal, 1/3 at knee high, 1/3 at tasseling<br><strong>Organic:</strong> 8-10 tonnes FYM/ha",
      idealRainfall: "<strong>Total:</strong> 500-750 mm<br><strong>Critical stages:</strong> Tasseling and silking<br><strong>Distribution:</strong> Well-distributed growth period",
      postHarvest: "• Harvest when moisture content is 20-25%<br>• Dry to 14% for storage<br>• Proper storage to prevent pest damage<br>• Value addition opportunities available"
    },
    sugarcane: {
      name: "Sugarcane",
      conditions: { minPH: 6.5, maxPH: 7.5, minTemp: 26, maxTemp: 33, minRain: 1000, maxRain: 1500, seasons: ["Monsoon"], soils: ["Loamy", "Clay"] },
      timeline: "<strong>Planting:</strong> February-March, October-November<br><strong>Harvest:</strong> 12-18 months<br><strong>Ratoon:</strong> 2-3 crops possible",
      howToPlant: "• Deep plowing and land preparation<br>• Use 3-bud setts<br>• Spacing: 90-120 cm between rows<br>• Plant in furrows 8-10 cm deep<br>• Gap filling within 30 days",
      fertilizer: "<strong>NPK:</strong> 280:90:90 kg/ha<br><strong>Application:</strong> Split doses at planting, 45 days, and 90 days<br><strong>Micronutrients:</strong> Iron, Zinc, Manganese",
      idealRainfall: "<strong>Total:</strong> 1200-1500 mm<br><strong>Distribution:</strong> Throughout growing season<br><strong>Critical:</strong> High water requirement crop",
      postHarvest: "• Harvest at proper maturity (12-14 months)<br>• Cut close to ground level<br>• Transport to mill within 24-48 hours<br>• Ratoon management for next crop"
    },
    soybean: {
      name: "Soybean",
      conditions: { minPH: 6.0, maxPH: 7.0, minTemp: 20, maxTemp: 30, minRain: 450, maxRain: 700, seasons: ["Monsoon"], soils: ["Loamy", "Clay"] },
      timeline: "<strong>Planting:</strong> June-July<br><strong>Harvest:</strong> October-November (90-120 days)<br><strong>Flowering:</strong> 35-45 days",
      howToPlant: "• Field preparation with 2-3 plowings<br>• Seed rate: 75-80 kg/hectare<br>• Row spacing: 30-45 cm<br>• Seed treatment with Rhizobium<br>• Depth: 2-3 cm",
      fertilizer: "<strong>NPK:</strong> 30:75:30 kg/ha (being legume, needs less N)<br><strong>Starter dose:</strong> 20 kg N/ha<br><strong>Rhizobium:</strong> Bacterial inoculation essential",
      idealRainfall: "<strong>Total:</strong> 500-700 mm<br><strong>Distribution:</strong> Well-distributed, avoid waterlogging<br><strong>Critical stages:</strong> Flowering and pod filling",
      postHarvest: "• Harvest when pods rattle<br>• Moisture content: 12-14%<br>• Proper drying and cleaning<br>• Store in pest-proof containers"
    },
    potato: {
      name: "Potato",
      conditions: { minPH: 5.5, maxPH: 6.5, minTemp: 15, maxTemp: 25, minRain: 400, maxRain: 600, seasons: ["Winter"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> October-December<br><strong>Harvest:</strong> January-March (90-120 days)<br><strong>Earthing up:</strong> 2-3 times during growth",
      howToPlant: "• Use certified seed tubers<br>• Cut tubers 2-3 days before planting<br>• Plant at 15-20 cm depth<br>• Row spacing: 50-60 cm<br>• Seed rate: 25-30 quintals/ha",
      fertilizer: "<strong>NPK:</strong> 120:75:100 kg/ha<br><strong>Application:</strong> Full P&K + 1/3 N at planting, remaining N in 2 splits<br><strong>Organic:</strong> 20-25 tonnes FYM/ha",
      idealRainfall: "<strong>Total:</strong> 500-700 mm<br><strong>Distribution:</strong> Uniform throughout crop period<br><strong>Avoid:</strong> Waterlogging conditions",
      postHarvest: "• Harvest when plants turn yellow<br>• Cure in shade for 10-15 days<br>• Store at 2-4°C with 90-95% humidity<br>• Avoid exposure to light"
    },
    onion: {
      name: "Onion",
      conditions: { minPH: 6.0, maxPH: 7.5, minTemp: 15, maxTemp: 25, minRain: 350, maxRain: 650, seasons: ["Winter"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> November-December<br><strong>Harvest:</strong> March-May (120-150 days)<br><strong>Transplanting:</strong> 6-8 weeks after sowing",
      howToPlant: "• Raise seedlings in nursery<br>• Transplant at pencil thickness<br>• Spacing: 15x10 cm<br>• Plant at 2-3 cm depth<br>• Avoid deep planting",
      fertilizer: "<strong>NPK:</strong> 100:50:50 kg/ha<br><strong>Application:</strong> Basal dose + top dressing at 30 and 60 days<br><strong>Sulphur:</strong> 40-50 kg/ha for quality bulbs",
      idealRainfall: "<strong>Total:</strong> 400-500 mm<br><strong>Distribution:</strong> Uniform water supply needed<br><strong>Stop irrigation:</strong> 15-20 days before harvest",
      postHarvest: "• Harvest when neck softens<br>• Cure in field for 4-5 days<br>• Store in well-ventilated area<br>• Market timing crucial for price"
    },
    chickpea: {
      name: "Chickpea (Chana)",
      conditions: { minPH: 6.5, maxPH: 7.5, minTemp: 20, maxTemp: 30, minRain: 300, maxRain: 500, seasons: ["Winter"], soils: ["Loamy", "Clay"] },
      timeline: "<strong>Planting:</strong> October-November<br><strong>Harvest:</strong> March-April (120-140 days)<br><strong>Flowering:</strong> 45-60 days after sowing",
      howToPlant: "• Seed treatment with Rhizobium<br>• Seed rate: 60-80 kg/hectare<br>• Row spacing: 30 cm<br>• Sowing depth: 3-4 cm<br>• Pre-irrigation recommended",
      fertilizer: "<strong>NPK:</strong> 20:40:20 kg/ha (low N due to N-fixation)<br><strong>Starter dose:</strong> Important for nodulation<br><strong>Phosphorus:</strong> Critical for root development",
      idealRainfall: "<strong>Total:</strong> 300-400 mm<br><strong>Distribution:</strong> Light showers preferred<br><strong>Avoid:</strong> Heavy rains during flowering and maturity",
      postHarvest: "• Harvest when pods turn brown<br>• Thresh when moisture is 12-14%<br>• Store in moisture-proof containers<br>• High protein content crop"
    },
    mustard: {
      name: "Mustard",
      conditions: { minPH: 6.0, maxPH: 7.5, minTemp: 15, maxTemp: 25, minRain: 250, maxRain: 400, seasons: ["Winter"], soils: ["Loamy", "Clay"] },
      timeline: "<strong>Planting:</strong> October-November<br><strong>Harvest:</strong> February-March (120-150 days)<br><strong>Flowering:</strong> 45-50 days",
      howToPlant: "• Field preparation with 2-3 plowings<br>• Seed rate: 4-5 kg/hectare<br>• Row spacing: 30 cm<br>• Sowing depth: 2-3 cm<br>• Line sowing preferred",
      fertilizer: "<strong>NPK:</strong> 80:40:40 kg/ha<br><strong>Application:</strong> Full dose at sowing or split N application<br><strong>Sulphur:</strong> 40-60 kg/ha for oil content",
      idealRainfall: "<strong>Total:</strong> 300-400 mm<br><strong>Distribution:</strong> Light irrigation required<br><strong>Critical stage:</strong> Siliqua formation",
      postHarvest: "• Harvest when siliquae turn yellow<br>• Dry properly before threshing<br>• Oil content: 35-42%<br>• Good market demand for oil"
    },
    barley: {
      name: "Barley",
      conditions: { minPH: 6.0, maxPH: 8.0, minTemp: 12, maxTemp: 22, minRain: 300, maxRain: 500, seasons: ["Winter"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> November-December<br><strong>Harvest:</strong> April-May (120-140 days)<br><strong>Grain filling:</strong> 90-110 days",
      howToPlant: "• Prepare fine seedbed<br>• Seed rate: 100 kg/hectare<br>• Row spacing: 22-23 cm<br>• Sowing depth: 3-4 cm<br>• Timely sowing important",
      fertilizer: "<strong>NPK:</strong> 80:40:20 kg/ha<br><strong>Application:</strong> Basal + top dressing of N at tillering<br><strong>Micronutrients:</strong> Zinc and iron if deficient",
      idealRainfall: "<strong>Total:</strong> 350-500 mm<br><strong>Water requirement:</strong> Less than wheat<br><strong>Tolerance:</strong> Better drought tolerance than wheat",
      postHarvest: "• Harvest at proper maturity<br>• Dry to 12% moisture<br>• Used for malt, feed, and food<br>• Good market for brewing industry"
    },
    sunflower: {
      name: "Sunflower",
      conditions: { minPH: 6.0, maxPH: 7.5, minTemp: 20, maxTemp: 30, minRain: 400, maxRain: 650, seasons: ["Monsoon", "Winter"], soils: ["Loamy", "Sandy"] },
      timeline: "<strong>Planting:</strong> June-July (Kharif), January-February (Rabi)<br><strong>Harvest:</strong> 90-120 days<br><strong>Flowering:</strong> 50-60 days",
      howToPlant: "• Deep plowing for root development<br>• Seed rate: 8-10 kg/hectare<br>• Spacing: 60x30 cm<br>• Depth: 2-3 cm<br>• Single seed per hill",
      fertilizer: "<strong>NPK:</strong> 60:90:40 kg/ha<br><strong>Application:</strong> Basal + side dressing at flower initiation<br><strong>Boron:</strong> 1 kg/ha for seed filling",
      idealRainfall: "<strong>Total:</strong> 500-750 mm<br><strong>Distribution:</strong> Well-distributed during vegetative growth<br><strong>Avoid excess:</strong> During maturity",
      postHarvest: "• Harvest when back of head turns brown<br>• Dry to 9-11% moisture<br>• Oil content: 38-48%<br>• High demand for cooking oil"
    },
    groundnut: {
      name: "Groundnut (Peanut)",
      conditions: { minPH: 6.0, maxPH: 7.0, minTemp: 25, maxTemp: 32, minRain: 500, maxRain: 750, seasons: ["Monsoon"], soils: ["Sandy", "Loamy"] },
      timeline: "<strong>Planting:</strong> June-July<br><strong>Harvest:</strong> October-November (120-140 days)<br><strong>Flowering:</strong> 30-40 days, Pegging: 40-50 days",
      howToPlant: "• Deep plowing and harrowing<br>• Seed rate: 120-140 kg/hectare<br>• Row spacing: 30 cm<br>• Depth: 3-4 cm<br>• Seed treatment with Rhizobium",
      fertilizer: "<strong>NPK:</strong> 25:50:75 kg/ha<br><strong>Gypsum:</strong> 500 kg/ha at flowering for shell development<br><strong>Calcium:</strong> Essential for pod filling",
      idealRainfall: "<strong>Total:</strong> 500-750 mm<br><strong>Distribution:</strong> Good rains during vegetative growth<br><strong>Pod development:</strong> Moderate moisture needed",
      postHarvest: "• Harvest when leaves turn yellow<br>• Dry pods to 8-10% moisture<br>• Store in cool, dry place<br>• Oil content: 48-50%, protein: 25-28%"
    },
    millets: {
      name: "Pearl Millet (Bajra)",
      conditions: { minPH: 6.5, maxPH: 8.0, minTemp: 25, maxTemp: 35, minRain: 250, maxRain: 500, seasons: ["Monsoon"], soils: ["Sandy", "Loamy"] },
      timeline: "<strong>Planting:</strong> June-July<br><strong>Harvest:</strong> September-October (75-90 days)<br><strong>Flowering:</strong> 45-55 days",
      howToPlant: "• Minimum tillage required<br>• Seed rate: 4-5 kg/hectare<br>• Row spacing: 45 cm<br>• Depth: 2-3 cm<br>• Drought tolerant crop",
      fertilizer: "<strong>NPK:</strong> 40:20:0 kg/ha<br><strong>Application:</strong> Light fertilizer requirement<br><strong>Organic matter:</strong> Benefits from FYM application",
      idealRainfall: "<strong>Total:</strong> 300-500 mm<br><strong>Tolerance:</strong> Excellent drought tolerance<br><strong>Water stress:</strong> Can withstand dry spells",
      postHarvest: "• Harvest when grains are hard<br>• Dry to 12% moisture<br>• Nutritious - high in iron and protein<br>• Growing demand for health foods"
    }
  };

  // Scoring system to find best crop match
  let bestCrop = null;
  let bestScore = -1;

  Object.values(crops).forEach(crop => {
    let score = 0;

    // pH compatibility (high weight)
    if (pH >= crop.conditions.minPH && pH <= crop.conditions.maxPH) {
      score += 25;
    } else {
      score -= 10;
    }

    // Temperature compatibility (high weight)
    if (Temperature >= crop.conditions.minTemp && Temperature <= crop.conditions.maxTemp) {
      score += 25;
    } else {
      score -= 10;
    }

    // Rainfall compatibility (high weight)
    if (Rainfall >= crop.conditions.minRain && Rainfall <= crop.conditions.maxRain) {
      score += 20;
    } else {
      score -= 8;
    }

    // Season compatibility (medium weight)
    if (crop.conditions.seasons.includes(Season)) {
      score += 15;
    } else {
      score -= 5;
    }

    // Soil type compatibility (medium weight)
    if (crop.conditions.soils.includes(Soil_Type)) {
      score += 10;
    } else {
      score -= 3;
    }

    // Market demand bonus (low weight)
    if (Market_Demand === "High") score += 5;
    else if (Market_Demand === "Medium") score += 3;

    // Irrigation method bonus
    if (Irrigation_Method === "Drip" && (crop.name === "Tomato" || crop.name === "Cotton")) score += 3;
    if (Irrigation_Method === "Canal" && (crop.name === "Rice" || crop.name === "Sugarcane")) score += 3;

    if (score > bestScore) {
      bestScore = score;
      bestCrop = crop;
    }
  });

  // Fallback to tomato if no good match (shouldn't happen with proper scoring)
  return bestCrop || crops.tomato;
}

updateProgress();

let lastScrollTop = 0;
const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollTop > lastScrollTop && scrollTop > 100) {
    navbar.style.transform = "translateY(-100%)";
  } else {
    navbar.style.transform = "translateY(0)";
  }

  lastScrollTop = scrollTop;
});

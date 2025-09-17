// Enhanced Search and Filter System
class DealerFilter {
  constructor() {
    this.searchInput = document.getElementById('searchInput');
    this.clearSearch = document.getElementById('clearSearch');
    this.categoryFilter = document.getElementById('categoryFilter');
    this.stateFilter = document.getElementById('stateFilter');
    this.districtFilter = document.getElementById('districtFilter');
    this.sortBy = document.getElementById('sortBy');
    this.resetFilters = document.getElementById('resetFilters');
    this.resultsSummary = document.getElementById('resultsSummary');
    this.resultsCount = document.getElementById('resultsCount');
    this.noResults = document.getElementById('noResults');
    
    this.dealerCards = document.querySelectorAll('.dealer-card');
    this.sections = document.querySelectorAll('.section');
    
    this.initializeEventListeners();
    this.initializeDistrictState();
    this.updateResultsCount();
  }

  initializeDistrictState() {
    // Disable district dropdown initially
    this.districtFilter.disabled = true;
    this.districtFilter.innerHTML = '<option value="all">Select State First</option>';
  }
  
  initializeEventListeners() {
    // Search input
    this.searchInput.addEventListener('input', () => this.handleSearch());
    this.clearSearch.addEventListener('click', () => this.clearSearchInput());
    
    // Filter controls
    this.categoryFilter.addEventListener('change', () => this.applyFilters());
    this.stateFilter.addEventListener('change', () => this.handleStateChange());
    this.districtFilter.addEventListener('change', () => this.applyFilters());
    this.sortBy.addEventListener('change', () => this.applySorting());
    this.resetFilters.addEventListener('click', () => this.resetAllFilters());
    
    // Show/hide clear button
    this.searchInput.addEventListener('input', () => {
      this.clearSearch.style.display = this.searchInput.value ? 'block' : 'none';
    });
  }
  
  handleStateChange() {
    const selectedState = this.stateFilter.value;
    
    if (selectedState === 'all') {
      // Reset district filter and disable it
      this.districtFilter.disabled = true;
      this.districtFilter.innerHTML = '<option value="all">Select State First</option>';
      this.districtFilter.value = 'all';
    } else {
      // Enable district filter and populate with state-specific districts
      this.districtFilter.disabled = false;
      this.updateDistrictOptions();
    }
    
    this.applyFilters();
  }
  
  updateDistrictOptions() {
    const selectedState = this.stateFilter.value;
    const districtOptions = this.getDistrictsByState(selectedState);
    
    // Clear current district options
    this.districtFilter.innerHTML = '<option value="all">All Districts</option>';
    
    // Add new district options
    districtOptions.forEach(district => {
      const option = document.createElement('option');
      option.value = district.value;
      option.textContent = district.name;
      this.districtFilter.appendChild(option);
    });
    
    // Reset district selection to "all"
    this.districtFilter.value = 'all';
  }
  
  getDistrictsByState(state) {
    const districtMap = {
      'punjab': [
        { value: 'ludhiana', name: 'Ludhiana' },
        { value: 'amritsar', name: 'Amritsar' },
        { value: 'fazilka', name: 'Fazilka' },
        { value: 'sangrur', name: 'Sangrur' },
        { value: 'bathinda', name: 'Bathinda' },
        { value: 'jalandhar', name: 'Jalandhar' },
        { value: 'patiala', name: 'Patiala' },
        { value: 'gurdaspur', name: 'Gurdaspur' },
        { value: 'hoshiarpur', name: 'Hoshiarpur' },
        { value: 'firozpur', name: 'Firozpur' },
        { value: 'faridkot', name: 'Faridkot' },
        { value: 'muktsar', name: 'Muktsar' },
        { value: 'moga', name: 'Moga' },
        { value: 'kapurthala', name: 'Kapurthala' },
        { value: 'tarn-taran', name: 'Tarn Taran' },
        { value: 'barnala', name: 'Barnala' },
        { value: 'fatehgarh-sahib', name: 'Fatehgarh Sahib' },
        { value: 'mohali', name: 'Mohali' },
        { value: 'ropar', name: 'Ropar' },
        { value: 'pathankot', name: 'Pathankot' },
        { value: 'mansa', name: 'Mansa' },
        { value: 'nawanshahr', name: 'Nawanshahr' }
      ],
      'haryana': [
        { value: 'gurgaon', name: 'Gurgaon' },
        { value: 'faridabad', name: 'Faridabad' },
        { value: 'panipat', name: 'Panipat' },
        { value: 'ambala', name: 'Ambala' },
        { value: 'yamunanagar', name: 'Yamunanagar' },
        { value: 'rohtak', name: 'Rohtak' },
        { value: 'hisar', name: 'Hisar' },
        { value: 'karnal', name: 'Karnal' },
        { value: 'sonipat', name: 'Sonipat' },
        { value: 'panchkula', name: 'Panchkula' },
        { value: 'kurukshetra', name: 'Kurukshetra' },
        { value: 'sirsa', name: 'Sirsa' }
      ],
      'rajasthan': [
        { value: 'jaipur', name: 'Jaipur' },
        { value: 'udaipur', name: 'Udaipur' },
        { value: 'jodhpur', name: 'Jodhpur' },
        { value: 'kota', name: 'Kota' },
        { value: 'bikaner', name: 'Bikaner' },
        { value: 'ajmer', name: 'Ajmer' },
        { value: 'alwar', name: 'Alwar' },
        { value: 'bharatpur', name: 'Bharatpur' },
        { value: 'churu', name: 'Churu' },
        { value: 'sikar', name: 'Sikar' }
      ],
      'uttar-pradesh': [
        { value: 'lucknow', name: 'Lucknow' },
        { value: 'kanpur', name: 'Kanpur' },
        { value: 'ghaziabad', name: 'Ghaziabad' },
        { value: 'agra', name: 'Agra' },
        { value: 'meerut', name: 'Meerut' },
        { value: 'varanasi', name: 'Varanasi' },
        { value: 'allahabad', name: 'Allahabad' },
        { value: 'bareilly', name: 'Bareilly' },
        { value: 'aligarh', name: 'Aligarh' },
        { value: 'moradabad', name: 'Moradabad' },
        { value: 'saharanpur', name: 'Saharanpur' },
        { value: 'gorakhpur', name: 'Gorakhpur' }
      ],
      'bihar': [
        { value: 'patna', name: 'Patna' },
        { value: 'gaya', name: 'Gaya' },
        { value: 'bhagalpur', name: 'Bhagalpur' },
        { value: 'muzaffarpur', name: 'Muzaffarpur' },
        { value: 'darbhanga', name: 'Darbhanga' },
        { value: 'purnia', name: 'Purnia' },
        { value: 'arrah', name: 'Arrah' },
        { value: 'begusarai', name: 'Begusarai' }
      ],
      'west-bengal': [
        { value: 'kolkata', name: 'Kolkata' },
        { value: 'howrah', name: 'Howrah' },
        { value: 'durgapur', name: 'Durgapur' },
        { value: 'asansol', name: 'Asansol' },
        { value: 'siliguri', name: 'Siliguri' },
        { value: 'malda', name: 'Malda' },
        { value: 'krishnanagar', name: 'Krishnanagar' },
        { value: 'barrackpur', name: 'Barrackpur' }
      ],
      'madhya-pradesh': [
        { value: 'bhopal', name: 'Bhopal' },
        { value: 'indore', name: 'Indore' },
        { value: 'jabalpur', name: 'Jabalpur' },
        { value: 'gwalior', name: 'Gwalior' },
        { value: 'ujjain', name: 'Ujjain' },
        { value: 'sagar', name: 'Sagar' },
        { value: 'dewas', name: 'Dewas' },
        { value: 'satna', name: 'Satna' }
      ],
      'maharashtra': [
        { value: 'mumbai', name: 'Mumbai' },
        { value: 'pune', name: 'Pune' },
        { value: 'nagpur', name: 'Nagpur' },
        { value: 'nashik', name: 'Nashik' },
        { value: 'aurangabad', name: 'Aurangabad' },
        { value: 'solapur', name: 'Solapur' },
        { value: 'kolhapur', name: 'Kolhapur' },
        { value: 'sangli', name: 'Sangli' },
        { value: 'ahmednagar', name: 'Ahmednagar' },
        { value: 'latur', name: 'Latur' }
      ],
      'karnataka': [
        { value: 'bangalore', name: 'Bangalore' },
        { value: 'mysore', name: 'Mysore' },
        { value: 'hubli', name: 'Hubli' },
        { value: 'mangalore', name: 'Mangalore' },
        { value: 'belgaum', name: 'Belgaum' },
        { value: 'gulbarga', name: 'Gulbarga' },
        { value: 'davanagere', name: 'Davanagere' },
        { value: 'bellary', name: 'Bellary' }
      ],
      'andhra-pradesh': [
        { value: 'visakhapatnam', name: 'Visakhapatnam' },
        { value: 'vijayawada', name: 'Vijayawada' },
        { value: 'guntur', name: 'Guntur' },
        { value: 'nellore', name: 'Nellore' },
        { value: 'kurnool', name: 'Kurnool' },
        { value: 'rajahmundry', name: 'Rajahmundry' },
        { value: 'tirupati', name: 'Tirupati' },
        { value: 'kakinada', name: 'Kakinada' }
      ],
      'telangana': [
        { value: 'hyderabad', name: 'Hyderabad' },
        { value: 'warangal', name: 'Warangal' },
        { value: 'nizamabad', name: 'Nizamabad' },
        { value: 'khammam', name: 'Khammam' },
        { value: 'karimnagar', name: 'Karimnagar' },
        { value: 'ramagundam', name: 'Ramagundam' },
        { value: 'mahbubnagar', name: 'Mahbubnagar' },
        { value: 'nalgonda', name: 'Nalgonda' }
      ],
      'tamil-nadu': [
        { value: 'chennai', name: 'Chennai' },
        { value: 'coimbatore', name: 'Coimbatore' },
        { value: 'madurai', name: 'Madurai' },
        { value: 'tiruchirappalli', name: 'Tiruchirappalli' },
        { value: 'salem', name: 'Salem' },
        { value: 'tirunelveli', name: 'Tirunelveli' },
        { value: 'erode', name: 'Erode' },
        { value: 'vellore', name: 'Vellore' }
      ],
      'kerala': [
        { value: 'kochi', name: 'Kochi' },
        { value: 'thiruvananthapuram', name: 'Thiruvananthapuram' },
        { value: 'kozhikode', name: 'Kozhikode' },
        { value: 'thrissur', name: 'Thrissur' },
        { value: 'kollam', name: 'Kollam' },
        { value: 'palakkad', name: 'Palakkad' },
        { value: 'alappuzha', name: 'Alappuzha' },
        { value: 'malappuram', name: 'Malappuram' }
      ],
      'gujarat': [
        { value: 'ahmedabad', name: 'Ahmedabad' },
        { value: 'surat', name: 'Surat' },
        { value: 'vadodara', name: 'Vadodara' },
        { value: 'rajkot', name: 'Rajkot' },
        { value: 'bhavnagar', name: 'Bhavnagar' },
        { value: 'jamnagar', name: 'Jamnagar' },
        { value: 'junagadh', name: 'Junagadh' },
        { value: 'gandhinagar', name: 'Gandhinagar' }
      ],
      'odisha': [
        { value: 'bhubaneswar', name: 'Bhubaneswar' },
        { value: 'cuttack', name: 'Cuttack' },
        { value: 'rourkela', name: 'Rourkela' },
        { value: 'berhampur', name: 'Berhampur' },
        { value: 'sambalpur', name: 'Sambalpur' },
        { value: 'puri', name: 'Puri' },
        { value: 'balasore', name: 'Balasore' },
        { value: 'bhadrak', name: 'Bhadrak' }
      ]
    };
    
    return districtMap[state] || [];
  }
  
  handleSearch() {
    this.applyFilters();
  }
  
  clearSearchInput() {
    this.searchInput.value = '';
    this.clearSearch.style.display = 'none';
    this.applyFilters();
  }
  
  applyFilters() {
    const searchTerm = this.searchInput.value.toLowerCase().trim();
    const categoryFilter = this.categoryFilter.value;
    const stateFilter = this.stateFilter.value;
    const districtFilter = this.districtFilter.value;
    
    let visibleCount = 0;
    
    this.dealerCards.forEach(card => {
      const name = card.dataset.name.toLowerCase();
      const location = card.dataset.location.toLowerCase();
      const category = card.dataset.category;
      const state = card.dataset.state ? card.dataset.state.toLowerCase() : 'punjab';
      const district = card.dataset.district ? card.dataset.district.toLowerCase() : location;
      const address = card.querySelector('.address').textContent.toLowerCase();
      const services = card.querySelector('.dealer-services span').textContent.toLowerCase();
      
      // Search filter
      const matchesSearch = !searchTerm || 
        name.includes(searchTerm) || 
        location.includes(searchTerm) || 
        address.includes(searchTerm) || 
        services.includes(searchTerm);
      
      // Category filter
      const matchesCategory = categoryFilter === 'all' || category === categoryFilter;
      
      // State filter
      const matchesState = stateFilter === 'all' || state.includes(stateFilter.replace('-', ' '));
      
      // District filter
      const matchesDistrict = districtFilter === 'all' || 
        district.includes(districtFilter) || 
        location.includes(districtFilter);
      
      const isVisible = matchesSearch && matchesCategory && matchesState && matchesDistrict;
      
      if (isVisible) {
        card.style.display = 'block';
        card.classList.remove('filtered-out');
        card.classList.add('filtered-in');
        visibleCount++;
      } else {
        card.classList.add('filtered-out');
        card.classList.remove('filtered-in');
        setTimeout(() => {
          if (card.classList.contains('filtered-out')) {
            card.style.display = 'none';
          }
        }, 300);
      }
    });
    
    // Show/hide sections based on visible cards
    this.sections.forEach(section => {
      const visibleCards = section.querySelectorAll('.dealer-card[style*="block"], .dealer-card:not([style*="none"])');
      const hasVisibleCards = Array.from(visibleCards).some(card => 
        !card.classList.contains('filtered-out')
      );
      section.style.display = hasVisibleCards ? 'block' : 'none';
    });
    
    // Update results count
    this.updateResultsCount(visibleCount);
    
    // Show/hide no results message
    this.noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    
    // Apply sorting after filtering
    this.applySorting();
  }
  
  applySorting() {
    const sortBy = this.sortBy.value;
    const visibleCards = Array.from(this.dealerCards).filter(card => 
      card.style.display !== 'none' && !card.classList.contains('filtered-out')
    );
    
    // Group cards by their parent sections
    const cardsBySection = new Map();
    visibleCards.forEach(card => {
      const section = card.closest('.section');
      if (!cardsBySection.has(section)) {
        cardsBySection.set(section, []);
      }
      cardsBySection.get(section).push(card);
    });
    
    // Sort cards within each section
    cardsBySection.forEach((cards, section) => {
      const sortedCards = this.sortCards(cards, sortBy);
      const grid = section.querySelector('.dealer-grid');
      
      // Re-append sorted cards
      sortedCards.forEach(card => {
        grid.appendChild(card);
      });
    });
  }
  
  sortCards(cards, sortBy) {
    return cards.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.dataset.name.localeCompare(b.dataset.name);
        case 'name-desc':
          return b.dataset.name.localeCompare(a.dataset.name);
        case 'location':
          return a.dataset.location.localeCompare(b.dataset.location);
        default:
          return 0;
      }
    });
  }
  
  updateResultsCount(count = null) {
    if (count === null) {
      count = Array.from(this.dealerCards).filter(card => 
        card.style.display !== 'none' && !card.classList.contains('filtered-out')
      ).length;
    }
    this.resultsCount.textContent = count;
  }
  
  resetAllFilters() {
    this.searchInput.value = '';
    this.categoryFilter.value = 'all';
    this.stateFilter.value = 'all';
    this.districtFilter.value = 'all';
    this.sortBy.value = 'name';
    this.clearSearch.style.display = 'none';
    
    // Reset district dropdown state
    this.districtFilter.disabled = true;
    this.districtFilter.innerHTML = '<option value="all">Select State First</option>';
    
    this.applyFilters();
  }
}

// Dealer details data
const dealerDetails = {
  gurukirpa: {
    name: "M/S Gurukirpa Agro Centre",
    phone: "+919XXXXXXX45",
    address: "Kohara, Sahnewal Road, Village Jandiale, Ludhiana",
    services: ["Pesticides & Insecticides", "Fertilizers", "Seeds", "Agricultural Chemicals"],
    hours: "Mon-Sat: 9:00 AM - 7:00 PM",
    established: "2010",
    specialization: "Organic and chemical pest control solutions"
  },
  hicon: {
    name: "M/S Hicon Pest Control",
    phone: "+919XXXXXXX00",
    address: "SCO 4, 2nd Floor, New Shopping Centre, Ghumar Mandi, Ludhiana",
    services: ["Professional Pest Control", "Spraying Equipment", "Consultation Services"],
    hours: "Mon-Fri: 10:00 AM - 6:00 PM",
    established: "2015",
    specialization: "Commercial and residential pest management"
  },
  singla: {
    name: "Singla Tractors",
    phone: "Contact via location",
    address: "Malout Road, Near 132 KVA Sub Station, Abohar, Fazilka",
    services: ["Tractor Sales", "Leasing Services", "Maintenance & Repair", "Spare Parts"],
    hours: "Mon-Sat: 8:00 AM - 8:00 PM",
    established: "2005",
    specialization: "New and used tractor sales with financing options"
  },
  gurkirpa: {
    name: "GURKIRPA AUTOS",
    phone: "Contact via location",
    address: "M.K. Bypass Road, Dhuri, Sangrur",
    services: ["Auto Parts", "Tractor Accessories", "Repair Services"],
    hours: "Mon-Sat: 9:00 AM - 7:00 PM",
    established: "2012",
    specialization: "Genuine parts and accessories for all tractor brands"
  },
  majha: {
    name: "Majha Agro Traders",
    phone: "+91-9855562888",
    address: "Ground Floor, Ajnala, Amritsar Road, Bhakha Hari Singh, Amritsar - 143102",
    services: ["Agricultural Trading", "Equipment Supply", "Bulk Orders", "Export Services"],
    hours: "Mon-Sat: 8:00 AM - 6:00 PM",
    established: "2008",
    specialization: "Large-scale agricultural equipment and commodity trading"
  },
  sonalika: {
    name: "Sonalika Samrat Combine Harvester",
    phone: "+91-9587886664",
    address: "Available through Sonalika dealers across Punjab",
    services: ["Combine Harvesters", "Seasonal Leasing", "Operator Training", "Maintenance"],
    hours: "Seasonal availability",
    established: "2018",
    specialization: "High-efficiency combine harvesters for wheat and rice"
  },
  kartar: {
    name: "Kartar Agro Industries Pvt. Ltd.",
    phone: "Contact via location",
    address: "Industrial Area, Ludhiana",
    services: ["Professional Harvesting Equipment", "Custom Solutions", "Technical Support"],
    hours: "Mon-Fri: 9:00 AM - 6:00 PM",
    established: "2000",
    specialization: "Industrial-grade harvesting and processing equipment"
  },
  bhajan: {
    name: "Bhajan Singh & Bros",
    phone: "+91-9884395093",
    address: "1913/36, Bhagwan Chowk, Janta Nagar, Gill Road, Ludhiana - 141003",
    services: ["Agricultural Tools", "Hand Tools", "Spare Parts", "Hardware"],
    hours: "Mon-Sat: 9:00 AM - 8:00 PM",
    established: "1995",
    specialization: "Traditional and modern agricultural hand tools"
  },
  gpn: {
    name: "GPN Machine Tools",
    phone: "Contact via location",
    address: "2436/2, Gali No-16, Dashmesh Nagar, Gill Road, Ludhiana - 141003",
    services: ["Machine Tools", "Equipment Repair", "Custom Fabrication", "Welding Services"],
    hours: "Mon-Sat: 8:00 AM - 7:00 PM",
    established: "2007",
    specialization: "Precision machine tools and custom agricultural equipment"
  },
  jrs: {
    name: "JRS Farmparts",
    phone: "+91-9779701222",
    address: "C-87, Phase 5, Focal Point, Ludhiana - 141010",
    services: ["Farm Parts", "Replacement Components", "Hydraulic Parts", "Engine Parts"],
    hours: "Mon-Sat: 9:00 AM - 7:00 PM",
    established: "2013",
    specialization: "Genuine replacement parts for all major tractor brands"
  }
};

// Show dealer details modal
function showDealerDetails(dealerId) {
  const dealer = dealerDetails[dealerId];
  if (!dealer) return;
  
  const modal = document.getElementById('dealerModal');
  const modalName = document.getElementById('modalDealerName');
  const modalBody = document.getElementById('modalBody');
  
  modalName.textContent = dealer.name;
  
  modalBody.innerHTML = `
    <div class="dealer-detail-section">
      <h4><i class="fas fa-map-marker-alt"></i> Location</h4>
      <p>${dealer.address}</p>
    </div>
    
    <div class="dealer-detail-section">
      <h4><i class="fas fa-phone"></i> Contact</h4>
      <p>${dealer.phone.startsWith('+') ? `<a href="tel:${dealer.phone}">${dealer.phone}</a>` : dealer.phone}</p>
    </div>
    
    <div class="dealer-detail-section">
      <h4><i class="fas fa-cogs"></i> Services</h4>
      <ul class="services-list">
        ${dealer.services.map(service => `<li><i class="fas fa-check"></i> ${service}</li>`).join('')}
      </ul>
    </div>
    
    <div class="dealer-detail-section">
      <h4><i class="fas fa-clock"></i> Business Hours</h4>
      <p>${dealer.hours}</p>
    </div>
    
    <div class="dealer-detail-section">
      <h4><i class="fas fa-calendar"></i> Established</h4>
      <p>${dealer.established}</p>
    </div>
    
    <div class="dealer-detail-section">
      <h4><i class="fas fa-star"></i> Specialization</h4>
      <p>${dealer.specialization}</p>
    </div>
    
    <div class="modal-actions">
      ${dealer.phone.startsWith('+') ? 
        `<a href="tel:${dealer.phone}" class="modal-btn primary">
          <i class="fas fa-phone"></i> Call Now
        </a>` : 
        `<a href="https://maps.google.com/?q=${encodeURIComponent(dealer.address)}" target="_blank" class="modal-btn primary">
          <i class="fas fa-map-marker-alt"></i> Get Directions
        </a>`
      }
      <button class="modal-btn secondary" onclick="closeDealerModal()">
        <i class="fas fa-times"></i> Close
      </button>
    </div>
  `;
  
  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

// Close dealer details modal
function closeDealerModal() {
  const modal = document.getElementById('dealerModal');
  modal.style.display = 'none';
  document.body.style.overflow = 'auto';
}

// Reset all filters (global function)
function resetAllFilters() {
  if (window.dealerFilter) {
    window.dealerFilter.resetAllFilters();
  }
}

// Simple particle system for background
function createParticleSystem() {
  const canvas = document.getElementById("particles-js");
  if (!canvas) return;
  
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const particles = [];
  const particleCount = window.innerWidth < 768 ? 30 : 50;
  
  // Create particles
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 2 + 1,
      opacity: Math.random() * 0.5 + 0.2
    });
  }
  
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
      particle.x += particle.vx;
      particle.y += particle.vy;
      
      // Wrap around edges
      if (particle.x < 0) particle.x = canvas.width;
      if (particle.x > canvas.width) particle.x = 0;
      if (particle.y < 0) particle.y = canvas.height;
      if (particle.y > canvas.height) particle.y = 0;
      
      // Draw particle
      ctx.save();
      ctx.globalAlpha = particle.opacity;
      ctx.fillStyle = '#4caf50';
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
    
    requestAnimationFrame(animate);
  }
  
  animate();
  
  // Handle resize
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
}

// Legacy search function for compatibility
function initializeSearch() {
  const searchInput = document.getElementById("searchInput");
  const dealerCards = document.querySelectorAll(".dealer-card");

  searchInput.addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase();

    dealerCards.forEach((card) => {
      const text = card.textContent.toLowerCase();

      if (text.includes(searchTerm)) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });
}

// Initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Initialize enhanced filter system
  window.dealerFilter = new DealerFilter();
  
  // Initialize particle system
  createParticleSystem();

  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    const modal = document.getElementById('dealerModal');
    if (e.target === modal) {
      closeDealerModal();
    }
  });
  
  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDealerModal();
    }
  });

  // Add intersection observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe all sections
  document.querySelectorAll(".section").forEach((section) => {
    section.style.opacity = "0";
    section.style.transform = "translateY(30px)";
    section.style.transition = "all 0.6s cubic-bezier(0.4, 0, 0.2, 1)";
    observer.observe(section);
  });

  // Add hover effects to dealer cards
  document.querySelectorAll(".dealer-card").forEach((card) => {
    card.addEventListener("mouseenter", () => {
      if (!card.classList.contains('filtered-out')) {
        card.style.transform = "translateY(-8px) scale(1.02)";
      }
    });

    card.addEventListener("mouseleave", () => {
      if (!card.classList.contains('filtered-out')) {
        card.style.transform = "translateY(0) scale(1)";
      }
    });
  });

  // Add loading animation completion
  setTimeout(() => {
    document.body.style.opacity = "1";
  }, 100);
});

// Add touch support for mobile hover effects
document.addEventListener("touchstart", function () {}, {
  passive: true,
});

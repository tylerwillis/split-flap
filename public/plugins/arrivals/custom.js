sf.display.ImageDrum = function() {
  return [
    ' ', 'Housing', 'Service', 'Item', 'Event', 'Job', 
    'Resource', 'Transport', 'Storage', 'Education', 'Financial'
  ];
};

// Ensure the full character set is available for text fields
sf.display.AlphabetDrum = sf.display.FullDrum;

sf.plugins.arrivals = {
  dataType: 'json',

  url: function(options) {
    return 'api/arrivals';
  },

  formatData: function(response) {
    return response.data;
  }
};

// Periodically retrigger animation every 60 seconds
setInterval(() => {
  // Force animation by directly manipulating DOM elements
  // First, collect all the character elements
  const charElements = $('.row .full span');
  
  // Store original classes for restoration
  const originalClasses = [];
  charElements.each(function() {
    originalClasses.push($(this).attr('class'));
  });
  
  // Change all elements to spaces temporarily
  charElements.fadeOut(50, function() {
    $(this).removeClass().addClass('csp');
  }).fadeIn(50);
  
  // After a brief delay, restore original characters with animation
  setTimeout(() => {
    charElements.each(function(index) {
      $(this).fadeOut(50, function() {
        $(this).removeClass().addClass(originalClasses[index] || 'csp');
      }).fadeIn(50);
    });
  }, 300);
}, 60000);

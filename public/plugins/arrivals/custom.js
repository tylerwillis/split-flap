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

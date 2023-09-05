$(document).ready(function() {
    var apiResponse;
    // Get references to HTML elements
    var searchInput = $('.search-bar');
    var searchButton = $('.search-button');
    var clearButton = $('.clear-button');
    var resultsContainer = $('.results-container');
  
    searchInput.on('dragover', handleDragOver);
    searchInput.on('drop', handleDrop);
  
    // Function to handle drag over event
    function handleDragOver(event) {
      event.preventDefault();
    }
  
    // Function to handle drop event
    function handleDrop(event) {
      event.preventDefault();
      var imageFile = event.originalEvent.dataTransfer.files[0];
      
      if (imageFile && imageFile.type.startsWith('image/')) {
        var reader = new FileReader();
        
        reader.onload = function(event) {
          var imageDataURL = event.target.result;
          searchInput.val(imageDataURL);
        };
        
        reader.readAsDataURL(imageFile);
      }
    }
  
    // Add event listeners
    searchButton.on('click', handleSearch);
    clearButton.on('click', clearResults);
  
    // Function to handle the search button click event
    function handleSearch() {
      var userInput = searchInput.val().trim();
    
      if (isImageInput(userInput)) {
        // User provided an image input
        makeImageAPICall(userInput);
      } else {
        // User provided a text input
        makeTextAPICall(userInput);
      }
    }
    
    // Function to check if the input is an image
    function isImageInput(input) {
      // Check if the input starts with "data:image" indicating a data URL
      return input.startsWith('data:image');
    }
    
    // Function to make API call for image input
    function makeImageAPICall(imageDataURL) {
        // Construct the API endpoint URL
    var apiUrl = 'https://demo.fiz-karlsruhe.de/iconclass/multimodal/api/similarity';
    var requestData = JSON.stringify({file_base64: imageDataURL.split(",")[1]});
     // Make the API call using $.ajax()
    $.ajax({
         url: apiUrl,
         type: 'POST',
         data:requestData,
         contentType:"application/json",
         success: function(data) {
         apiResponse = data;
         // Handle successful API response
         displayResults(apiResponse.filenames, apiResponse.ics, apiResponse.labels)
         },
         error: function(xhr, status, error) {
         // Handle API error
         console.error('API error:', error);
         }
     });
     }
    // Function to make API call for text input
    function makeTextAPICall(textInput) {
       // Construct the API endpoint URL
    var apiUrl = 'https://demo.fiz-karlsruhe.de/iconclass/multimodal/api/similarity_text';

    q=encodeURIComponent(textInput)
    // Make the API call using $.ajax()
    $.ajax({
        url: apiUrl,
        method: 'GET',
        data: {q:q},
        dataType: 'json',
        success: function(data) {
        apiResponse = data;
        // Handle successful API response
        displayResults(apiResponse.filenames, apiResponse.ics, apiResponse.labels)
        },
        error: function(xhr, status, error) {
        // Handle API error
        console.error('API error:', error);
        }
    });
    }
    
    // Clear results function
    function clearResults() {
      resultsContainer.html('');
    }
    
    // Display results function
    function displayResults(URIs, data, labels) {
      console.log(labels)
      // Clear previous results
      clearResults();
      
      // Create and append the URIs list
      var URIsList = $('<ul>').addClass('results-list1');
      $.each(URIs, function(index, URI) {
        var img = $('<img>').attr("src", "https://iconclass.org/iiif/2/"+URI+"/full/200,/0/default.jpg");
        img.on("click", function() {
          selectNotations(URI)
        });
        var listItem = $('<li>').append(img);
        URIsList.append(listItem);
      });
      
      resultsContainer.append(URIsList);
      
      // Create and append the strings list
      var stringsList = $('<ul>').addClass('results-list2');

      var strings = createUniqueStringList(data)
      $.each(strings, function(index, string) {
        console.log(labels[string])
        var text = [string, labels[string]].join(" ")
        var listItem = $("<li>").append($('<a>').attr({href:"https://www.iconclass.org/"+string, target:"_blank"}).text(text));
        stringsList.append(listItem);
      });
      
      resultsContainer.append(stringsList);
    }


    function createUniqueStringList(data) {
      var stringFrequencyMap = {};
    
      // Iterate through the input data
      $.each(data, function(index, list) {
        // Iterate through each list
        $.each(list, function(index, item) {
          // Increment the frequency count for each string
          stringFrequencyMap[item] = (stringFrequencyMap[item] || 0) + 1;
        });
      });
    
      // Convert the map to an array of [string, frequency] pairs
      var stringFrequencyArray = $.map(stringFrequencyMap, function(frequency, string) {
        return { string: string, frequency: frequency };
      });
    
      // Sort the array by frequency in descending order
      stringFrequencyArray.sort(function(a, b) {
        return b.frequency - a.frequency;
      });
    
      // Create the list of unique strings sorted by frequency
      var uniqueStringList = [];
      $.each(stringFrequencyArray, function(index, pair) {
        uniqueStringList.push(pair.string);
      });
    
      return uniqueStringList;
    }

    

    function selectNotations(URI) {
      var filenames = apiResponse.filenames
      $.each(filenames, function(index, filename) {
        if (filename==URI) {
          var notations = apiResponse.ics[index];
          var labels = apiResponse.labels
          // Get all elements with the specific class
          var element = $('.results-list2').eq(0);
          element.empty()
          $.each(notations, function(index, notation) {
            var text = [notation, labels[notation]].join(" ")
            var listItem = $("<li>").append($('<a>').attr({href:"https://www.iconclass.org/"+notation, target:"_blank"}).text(text));
            element.append(listItem);
          });
        }
      });
      $('html, body').animate({ scrollTop: 50 }, 'slow');
    }




  });
  

  
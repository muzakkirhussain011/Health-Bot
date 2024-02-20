// Function to add user message to the conversation
function addUserMessage(message) {
    var userMessageDiv = document.getElementById('userMessage');
  
    // Create a new card element for the user message
    var card = document.createElement('div');
    card.classList.add('card', 'flex-fill', 'mb-2');
  
    // Set the card content with the user message
    card.innerHTML = `
      <div class="card-header">
          <h5 class="mb-0">&nbsp;<img class="rounded-circle" src="static/img/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector%20(Custom).jpg" width="39" height="34">&nbsp;You</h5>
      </div>
      <div class="card-body">
          <p class="card-text">${message}</p>
      </div>
    `;
  
    // Append the new card to the userMessage div
    userMessageDiv.appendChild(card);
  
    // Scroll the userMessage div to the bottom
    userMessageDiv.scrollTop = userMessageDiv.scrollHeight;
  }
  
  // Function to add bot message to the conversation
  function addBotMessage(message) {
    var userMessageDiv = document.getElementById('userMessage');
  
    // Create a new card element for the bot message
    var card = document.createElement('div');
    card.classList.add('card', 'flex-fill', 'mb-2');
  
    // Set the card content with the bot message
    card.innerHTML = `
      <div class="card-header">
          <h5 class="mb-0">&nbsp;<img class="rounded-circle" src="static/img/My%20project%20(1).png" width="39" height="34">&nbsp;HealthBot</h5>
      </div>
      <div class="card-body">
          <p class="card-text">${message}</p>
      </div>
    `;
  
    // Append the new card to the userMessage div
    userMessageDiv.appendChild(card);
  
    // Scroll the userMessage div to the bottom
    userMessageDiv.scrollTop = userMessageDiv.scrollHeight;
  }
  

// Function to handle user input
function handleUserInput(event) {
    // Get the user input element
    var userInput = document.getElementById('userInput');

    // Get the value of the user input
    var message = userInput.value;

    // If the user pressed the Enter key and the input is not empty
    if (event.key === 'Enter' && message.trim() !== '') {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Send the user message
        sendMessage(message);

        // Clear the user input
        userInput.value = '';
    }
}

// Function to handle send button click
function handleSendButtonClick() {
    // Get the user input element
    var userInput = document.getElementById('userInput');

    // Get the value of the user input
    var message = userInput.value;

    // If the input is not empty
    if (message.trim() !== '') {
        // Send the user message
        sendMessage(message);

        // Clear the user input
        userInput.value = '';
    }
}

// Function to send the user message and receive bot response
function sendMessage(message) {
    // Add the user message to the conversation
    addUserMessage(message);

    // Make an AJAX request to the Django app to get the bot reply
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/bot_reply/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Parse the response JSON
            var response = JSON.parse(xhr.responseText);
            
            // Get the bot reply from the response
            var botReply = response.message;
            
            // Add the bot reply to the conversation
            addBotMessage(botReply);
        }
    };
    xhr.send('message=' + encodeURIComponent(message));
}

// Function to reset the chat
function resetChat() {
    // Clear the userMessage div
    var userMessageDiv = document.getElementById('userMessage');
    userMessageDiv.innerHTML = '';

    // Scroll to the top of the userMessage div
    userMessageDiv.scrollTop = 0;
}

// Function to reset the app
function resetApp() {
    // Make an AJAX request to the reset_app endpoint
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/reset_app/');
    xhr.onload = function () {
      if (xhr.status === 200) {
        // App reset successful, clear the conversation
        var userMessageDiv = document.getElementById('userMessage');
        userMessageDiv.innerHTML = '';
      }
    };
    xhr.send();
  }
  
  // Function to handle repeatButton click event
  function handleRepeatButtonClick() {
    // Call the resetApp function to reset the app
    resetApp();
  }
  // Function to handle repeatButton click event

  // Attach the event listener to the repeatButton
  document.getElementById('repeatButton').addEventListener('click', handleRepeatButtonClick);
  

// Attach the event listener to the repeatButton
document.getElementById('repeatButton').addEventListener('click', handleRepeatButtonClick);


// Attach event listeners to the user input element and send button
var userInput = document.getElementById('userInput');
userInput.addEventListener('keyup', handleUserInput);

var sendButton = document.getElementById('sendButton');
sendButton.addEventListener('click', handleSendButtonClick);

// Attach the event listener to the repeatButton
document.getElementById('repeatButton').addEventListener('click', handleRepeatButtonClick);

// Scroll the userMessage div to the latest message
window.addEventListener('load', function() {
    var userMessageDiv = document.getElementById('userMessage');
    userMessageDiv.scrollTop = userMessageDiv.scrollHeight;
});

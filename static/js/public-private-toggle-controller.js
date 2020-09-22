function toggleController(){
    /* A script to allow the user to toggle between public/private curriculum settings.
     * Each click on the button sends an AJAX call to the backend to update the db */

    // Grab the button element
    const button = document.getElementById('btn-public-toggle');
    // Grab the inner text element (displays 'public' or 'private')
    const text = document.getElementById('public-toggle-text');

    // Add an event listener to the button
    if (button){
        button.addEventListener('click', event => {
            // Allow user to click on button or text content
            if (event.target.id === 'btn-public-toggle' || 'public-toggle-text'){
                // Toggle states
                if (text.className === 'public')
                    setPrivateState(button, text);
                else if (text.className === 'private')
                    setPublicState(button, text);
                else
                    console.log("Error: Text element has neither public or private class!")
                ajaxToggleState(button);
            }
        })
    }
};

function setPrivateState(button, text){
    // Change the text element class to 'private'
    text.className = 'private'
    // Change the glyphicon to slashed eye
    const icon = button.firstElementChild
    icon.className = 'far fa-eye-slash'
    // Change the button background to danger
    button.classList = "btn btn-sm btn-danger dashboard-options-btn"
    // Change the textContent to 'private'
    text.textContent = 'private'
}

function setPublicState(button, text){
    // Change the text element class to 'public'
    text.className = 'public'
    // Change the glyphicon to eye
    const icon = button.firstElementChild
    icon.className = 'far fa-eye'
    // Change the button background to success
    button.classList = "btn btn-sm btn-success dashboard-options-btn"
    // Change the textContent to 'public'
    text.textContent = 'public'
}

function ajaxToggleState(target){
    // Get the url endpoint for the view call (on the button element)
    const updateUrl = target.getAttribute('update-url');
    $.ajax({
        url: updateUrl,
        type: "GET",
        success: function(data){
            console.log('Curriculum updated successfully!')
            console.log(data);
        },
        error: function(xhr, errorMsg, error){
            console.log(xhr.status, xhr.responseText, errorMsg)
        }
    });
};

toggleController();

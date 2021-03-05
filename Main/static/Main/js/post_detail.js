const commentForm = document.forms["comment-form"];
const commentContainer = document.querySelector("#comments > div");


// Create an comment element to add after the request accapted by the server
function appendNewComment(comment){
    // create username and photo based on user is auhtenticated or anonymous
    let commentProfilePhoto;
    let commentUsername;

    if(IS_AUTHENTICATED){
        commentProfilePhoto = `<img src="${PROFILE_PHOTO_URL}" alt="" class="comment-profile-photo">`
        commentUsername = USERNAME;
    }else{
        commentProfilePhoto = `<img src="${BASE_URL}/static/Main/img/anonymous.svg" alt="" class="comment-profile-photo">`
        commentUsername = comment.anonymous_name;
    }

    // create actual element
    let commentElement =`
    <div class="comment">
        ${commentProfilePhoto}

        <div>
            <h3 class="comment-username">${commentUsername}</h3>
            <p class="comment-date">${new Date(Date.now()).toDateString()} <span class="reply-to-comment">Reply</span></p>
            <p class="comment-content">${ comment.content }</p>
        </div>
    
    </div>`;
    commentContainer.innerHTML += commentElement;
}


function sendCommentRequest(post_data){
    const crsf_token = document.cookie.split("=")[1];

    let form = new URLSearchParams();
    form.append("anonymous_name", post_data.anonymous_name);
    form.append("content", post_data.content);
    form.append("csrfmiddlewaretoken", crsf_token);
    
    // the host accepts making comment from same url
    fetch(location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": document.cookie,
        },
        body: form,
    })
    .then(async function(response){
        //let text = await response.text();
        if(response.status === 200){
            appendNewComment(post_data); // add comment to layout
            // clear form inputs
            commentForm.name.value = "";
            commentForm.content.value = "";
        }else{
            console.log("Server error while sending comment", `Status: ${response.status}`);
        }
    });
}


// Make Comment request to the server
commentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    let name = event.target.name.value ? event.target.name.value : null;
    let comment = event.target.content.value;

    // Check if fields are fullfilled
    if(!IS_AUTHENTICATED && name === null){
        let error = document.createElement("p");
        error.className = "error";
        error.innerText = "You are not logged in, give your name to be able to make anonymous comment";
        // delete previous error
        if(event.target.name.nextSibling.className === "error"){
            event.target.name.nextSibling.remove();
        }
        event.target.insertBefore(error, event.target.name.nextSibling);
        return;
    }else{
        if(event.target.name.nextSibling.className === "error"){
            event.target.name.nextSibling.remove();
        }
    }
    
    if(!comment){
        let error = document.createElement("p");
        error.className = "error";
        error.innerText = "You have to write something";
        // delete previous error
        if(event.target.content.nextSibling.className === "error"){
            event.target.content.nextSibling.remove();
        }
        event.target.insertBefore(error, event.target.content.nextSibling);
        return;
    }else{
        if(event.target.content.nextSibling.className === "error"){
            event.target.content.nextSibling.remove();
        }
    }

    post_data = {
        anonymous_name: name,
        content: comment,
        slug: POST_SLUG,
    };

    // new comment is added to the layout in this function if the reponse successfull
    sendCommentRequest(post_data); 
});
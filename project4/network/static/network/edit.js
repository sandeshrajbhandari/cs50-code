document
  .querySelectorAll(".editBtn")
  .forEach((edit) => edit.addEventListener("click", editPost));

function editPost(e) {
  let postDiv = e.target.parentNode;
  let postId = postDiv.dataset.postid;
  let postContentDiv = postDiv.querySelector(".postContent");
  let initPostContent = postDiv.querySelector(".postContent").innerHTML;
  console.log("clickChck " + initPostContent);
  let csrfToken = postDiv.querySelector('[name="csrfmiddlewaretoken"]').value;
  console.log(csrfToken);
  let editForm = `
  <form method="put">
    <textarea class="form-control postText" name="newPostText">${initPostContent}</textarea>
    <input class="btn btn-primary submitEdit" type="submit" value="Submit Post" />
  </form>
`;
  postContentDiv.innerHTML = editForm;

  postContentDiv
    .querySelector(".submitEdit")
    .addEventListener("click", submitPost);

  function submitPost(e) {
    e.preventDefault();
    console.log(postDiv.querySelector(".postText").value);
    fetch("/", {
      method: "PUT",
      body: JSON.stringify({
        newPostText: postDiv.querySelector(".postText").value,
        postId: postId,
      }),
      headers: {
        "X-CSRFToken": csrfToken,
      },
    }).then((response) => {
      postContentDiv.innerHTML = postDiv.querySelector(".postText").value;
      console.log(response);
    });
  }
}


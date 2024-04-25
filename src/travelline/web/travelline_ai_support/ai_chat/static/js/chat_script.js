const user_username = JSON.parse(
  document.getElementById("user_username").textContent
);
document.querySelector("#submit").onclick = function (e) {
  const messageInputDom = document.querySelector("#input");
  const message = messageInputDom.value;
  if (message.replace(/\s+/g, "") != "") {
    const inputDom = document.querySelector("#input-group");
    inputDom.className += " disabled-div";
    chatSocket.send(
      JSON.stringify({
        message: message,
        username: user_username,
        from_ai: false,
      })
    );
  }
  messageInputDom.value = "";
};

const boxName = JSON.parse(document.getElementById("room-name").textContent);
// Create a WebSocket in JavaScript.
const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/" + boxName + "/"
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  if (data.from_ai) {
    const inputDom = document.querySelector("#input-group");
    inputDom.className = inputDom.className.replace(" disabled-div", "");
  }
  let g = document.createElement("div");
  if (data.from_ai) g.className = "chat-message-left pb-4";
  else g.className = "chat-message-right pb-4";

  let avatar = document.createElement("div");
  let avatar_img = document.createElement("img");
  avatar_img.className = "rounded-circle mr-1";
  if (data.from_ai)
    avatar_img.setAttribute(
      "src",
      "https://www.svgrepo.com/show/242153/operator-user.svg"
    );
  else
    avatar_img.setAttribute(
      "src",
      "https://www.svgrepo.com/show/452030/avatar-default.svg"
    );
  avatar_img.setAttribute("alt", "AI");
  avatar_img.setAttribute("width", 40);
  avatar_img.setAttribute("height", 40);

  avatar_time = document.createElement("div");
  avatar_time.className = "text-muted small text-nowrap mr-1 mt-1 text-center";

  let currentdate = new Date();
  let minutes = currentdate.getMinutes().toString();
  let hours = currentdate.getHours().toString();
  if (minutes.length == 1) minutes = "0" + minutes;
  if (hours.length == 1) hours = "0" + hours;
  avatar_time_text = document.createTextNode(hours + ":" + minutes);
  avatar_time.appendChild(avatar_time_text);

  avatar.appendChild(avatar_img);
  avatar.appendChild(avatar_time);

  g.appendChild(avatar);

  let message = document.createElement("span");
  let message_name = document.createElement("div");
  if (data.from_ai) {
    message.className =
      "flex-shrink-1 rounded py-2 px-3 mr-3 chat-message-wrap-left";
    message_name.className = "font-weight-bold mb-1 chat-message-nickname-left";
  } else {
    message.className =
      "flex-shrink-1 rounded py-2 px-3 mr-3 chat-message-wrap-right";
    message_name.className =
      "font-weight-bold mb-1 chat-message-nickname-right";
  }
  let message_name_text = document.createTextNode(data.username);
  message_name.appendChild(message_name_text);
  let message_text = document.createTextNode(data.message);

  message.appendChild(message_name);
  message.appendChild(message_text);

  g.appendChild(message);

  const query = document.querySelector("#chat-text");
  query.appendChild(g);
  query.scrollTop = query.scrollHeight;
};

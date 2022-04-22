<div id = "container">
<div id = "aside">
<center>

<div>
  {{outcome}}
</div>

  <div>
    <form action = "/addFriend" method = "post">
      <input name="friend" type="search" placeholder="Search for friends here...">
    </form>
  </div>
  </center>
  <ul id ="friendList">
      % for file in data:

        <li class="friend">
          <img src = "img/blankProfile.png"/>
          <div class ='Friend_name'>
          {{file}}
          </div>
          <form  onsubmit = "newChat(this)" action = "/addFriend" method = "post">
            <button  value = {{file}} type = "submit" name = "chatWith" > Message</button>
            </form>
        </li>
      % end
    </ul>
  </div>


  <div id = "main">
  <center>
    <h3> {{friend}} </h3>
    </center>

  <div id ="chatWindow">
    <ul id = "messages"> 
        </ul> 
       <script>
          var secrett = getCookie("secret"); 
          function getCookie(cname) {
            let name = cname + "=";
            let decodedCookie = decodeURIComponent(document.cookie);
            let ca = decodedCookie.split(';');
            for(let i = 0; i <ca.length; i++) {
              let c = ca[i];
              while (c.charAt(0) == ' ') {
                  c = c.substring(1);
              }
              if (c.indexOf(name) == 0) {
              return c.substring(name.length, c.length);
              }
            }
            return "";
          }
          function base64StringToArrayBuffer(b64str) {
            var byteStr = window.atob(b64str)
            var bytes = new Uint8Array(byteStr.length)
            for (var i = 0; i < byteStr.length; i++) {
              bytes[i] = byteStr.charCodeAt(i)
            }
            return bytes.buffer
          }
          function str2ab(str) {
            const buf = new ArrayBuffer(str.length);
            const bufView = new Uint8Array(buf);
            for (let i = 0, strLen = str.length; i < strLen; i++) {
              bufView[i] = str.charCodeAt(i);
            }
              return buf;
          }
          async function importKey(secret) {
              return await crypto.subtle.importKey(
                  'raw',
                  new TextEncoder().encode(secret),
                  { name: 'HMAC', hash: 'SHA-256' },
                  false,
                  ['sign', 'verify'],
              )
          }
          async function importSessionKey() {
              const secret = getCookie("secret"); 
              var key = await crypto.subtle.importKey(
                      "raw",
                      base64StringToArrayBuffer(secret),
                      { name: "AES-GCM" },
                      true,
                      ['encrypt', 'decrypt']
              );
              return key;
          }
          async function verifySignature(message, signature, secret) {
               const key = await importKey(secret);
               const sigBuf = Uint8Array.from(atob(signature), c => c.charCodeAt(0));
               return await crypto.subtle.verify(
                   'HMAC',
                    key,
                    sigBuf,
                    new TextEncoder().encode(message),
               );
          }
          async function msgdecryption(ciphertext, iv) {
              var sessionKey = await importSessionKey()
              alert("import the key")
              let decrypted = await window.crypto.subtle.decrypt(
                  {
                    name: "AES-GCM",
                    iv
                  },
                  sessionKey,
                  ciphertext
              );
              let decMsg = new TextDecoder("utf-8").decode(decrypted);
              console.log("AHHHHHHH: ", decMsg)
              return decMsg;
          }
          async function test() {
            for (let i = 0; i < ${messages}.length; i++) {
              if(${messages}[i].sender != "Server") {

                let CTime = base64StringToArrayBuffer(${messages}[i].msgtime)
             
                let iv = base64StringToArrayBuffer(${messages}[i].iv)
           
                let Cmsg = base64StringToArrayBuffer(${messages}[i].msg)
                let sender = ${messages}[i].sender
                let user = getCookie("user")
                console.log("UUUUUUUU: ", user)
                let friend = getCookie("currentChat")
                let decryptedT = await msgdecryption(CTime, iv)
                let decTime = decryptedT.split(",")[0];

                let decryptedM = await msgdecryption(Cmsg, iv)
                let decMsg = decryptedM.split(",")[0];

                let msgS = decryptedM.split(",")[1]
                let timeS = decryptedT.split(",")[1]

                vM = await verifySignature(decMsg, msgS, secrett)
                vT = await verifySignature(decTime, timeS, secrett)
                
                console.log("HMACCCCCCC ", vM)
                console.log("TIMMMMMMMMME", decTime)
                if(vM && vT) {
                  if(sender == user) {
                      let div = document.createElement('li')
                      div.className = "your_messages"
                      div.innerHTML="[" + decTime + "] " + "You: " + decMsg
                      document.querySelector("#messages").append(div)
                  } else {
                      let div = document.createElement('li')
                      div.className = "friend_messages"
                      div.innerHTML="[" + decTime + "] " + friend + ": " + decMsg
                      document.querySelector("#messages").append(div)
                  }
                } 
              } else {
                  let div = document.createElement('li')
                  div.className = "friend_messages"
                  div.innerHTML= ${messages}[i].msg
                  document.querySelector("#messages").append(div)
              }
            }
             
          }
          test()
           
        </script>

  </div>
  % if friend != "":
  <div id = "typing">
    <form action = "/sendMessage" method = "post">
    <center>
      <input style ="width: 70%"name="message" type="text" placeholder="Type here..." id="messageInput">
      <input onclick="msgencryption()" value="Send" type ="submit" </text>
    </center>
  </div>
  %end
  </div>

</div>

 <script src="js/script_message.js">
</script>